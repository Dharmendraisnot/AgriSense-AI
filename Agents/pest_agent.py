"""
agents/pest_agent.py

Identifies pests and diseases from crop + symptom description using RAG
retrieval over the PlantVillage knowledge base and IBM Granite generation.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from agents.base_agent import BaseAgent
from utils.logger import logger


class PestAgent(BaseAgent):
    """Identifies pests/diseases and recommends treatment + prevention."""

    async def identify(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return await self.run(**params)

    async def run(
        self,
        message: str = "",
        location: Optional[str] = None,
        language: str = "en",
        crop: str = "unknown",
        symptoms: str = "",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        # Use message as symptoms if dedicated field is empty
        symptoms = symptoms or message

        # ── Try RAG retrieval first ────────────────────────────
        rag_context = self._retrieve_rag_context(crop, symptoms)

        # ── Build prompt ───────────────────────────────────────
        prompt = (
            f"You are AgriSense AI, a plant pathology expert.\n\n"
            f"A farmer reports the following about their {crop} crop:\n"
            f"  Symptoms: {symptoms}\n"
            + (f"\nRelevant knowledge base context:\n{rag_context}\n" if rag_context else "")
            + f"\nProvide:\n"
            f"1. Most likely pest or disease name\n"
            f"2. Severity (Low / Medium / High)\n"
            f"3. Three treatment options\n"
            f"4. Two prevention measures\n"
            f"5. Brief explanation\n\n"
            f"Answer in a structured, farmer-friendly way.\n\nResponse:"
        )
        raw = self.generate(prompt)

        # ── Parse structured response ──────────────────────────
        pest_name, severity, treatments, preventions = self._parse_response(raw, crop)

        return {
            "pest_or_disease": pest_name,
            "severity":        severity,
            "treatment":       treatments,
            "prevention":      preventions,
            "explanation":     raw,
            "answer":          raw,
            "sources":         ["PlantVillage Dataset", "RAG Knowledge Base", "IBM Granite"],
        }

    @staticmethod
    def _retrieve_rag_context(crop: str, symptoms: str) -> str:
        """Attempt RAG retrieval; returns empty string if not yet set up."""
        try:
            from rag.retriever import Retriever
            retriever = Retriever()
            docs = retriever.retrieve(f"{crop} {symptoms}", k=3)
            return "\n".join(d.page_content for d in docs)
        except Exception as exc:
            logger.debug(f"RAG retrieval skipped: {exc}")
            return ""

    @staticmethod
    def _parse_response(raw: str, crop: str):
        """Best-effort parsing – returns defaults if extraction fails."""
        lines = raw.split("\n")
        pest_name  = f"Unknown pest on {crop}"
        severity   = "Medium"
        treatments: List[str] = []
        preventions: List[str] = []

        for line in lines:
            ll = line.lower()
            if "pest" in ll or "disease" in ll or "name" in ll:
                pest_name = line.strip(" -1234567890.:").strip() or pest_name
            if "high" in ll:
                severity = "High"
            elif "low" in ll:
                severity = "Low"
            if "treatment" in ll or "apply" in ll or "spray" in ll or "fungicide" in ll:
                treatments.append(line.strip(" -•"))
            if "prevent" in ll or "avoid" in ll or "rotate" in ll:
                preventions.append(line.strip(" -•"))

        treatments  = (treatments  or ["Consult local agricultural extension officer"])[:3]
        preventions = (preventions or ["Practice crop rotation"])[:2]
        return pest_name, severity, treatments, preventions
