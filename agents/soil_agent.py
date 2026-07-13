"""
agents/soil_agent.py

Evaluates soil health from nutrient readings and generates improvement
recommendations using IBM Granite, augmented by RAG knowledge.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from agents.base_agent import BaseAgent
from utils.logger import logger


# Optimal ranges (ICAR guidelines)
_OPTIMAL = {
    "ph":         (6.0, 7.5),
    "nitrogen":   (280, 560),   # kg/ha
    "phosphorus": (20,  40),    # kg/ha
    "potassium":  (140, 280),   # kg/ha
}


def _score_param(value: float, low: float, high: float) -> float:
    """Return 0–1 score: 1.0 if within range, lower if outside."""
    if low <= value <= high:
        return 1.0
    dist = min(abs(value - low), abs(value - high))
    span = high - low
    return max(0.0, 1.0 - dist / span)


class SoilAgent(BaseAgent):
    """Soil health evaluator and recommendations generator."""

    async def analyze(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return await self.run(**params)

    async def run(
        self,
        message: str = "",
        location: Optional[str] = None,
        language: str = "en",
        ph: float = 6.5,
        nitrogen: float = 280,
        phosphorus: float = 25,
        potassium: float = 200,
        organic_matter: Optional[float] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        # ── Compute health score ───────────────────────────────
        scores = [
            _score_param(ph,         *_OPTIMAL["ph"]),
            _score_param(nitrogen,   *_OPTIMAL["nitrogen"]),
            _score_param(phosphorus, *_OPTIMAL["phosphorus"]),
            _score_param(potassium,  *_OPTIMAL["potassium"]),
        ]
        health_score = round(sum(scores) / len(scores) * 100, 1)
        status = (
            "Excellent" if health_score >= 85 else
            "Good"      if health_score >= 65 else
            "Fair"      if health_score >= 45 else
            "Poor"
        )

        # ── Rule-based quick recommendations ──────────────────
        recs: List[str] = []
        if ph < 6.0:
            recs.append("Apply agricultural lime to raise soil pH.")
        elif ph > 7.5:
            recs.append("Apply elemental sulfur or acidifying fertilizer to lower pH.")
        if nitrogen < _OPTIMAL["nitrogen"][0]:
            recs.append("Add urea or compost to improve nitrogen levels.")
        if phosphorus < _OPTIMAL["phosphorus"][0]:
            recs.append("Apply single superphosphate (SSP) for phosphorus deficiency.")
        if potassium < _OPTIMAL["potassium"][0]:
            recs.append("Apply muriate of potash (MOP) to improve potassium.")
        if not recs:
            recs.append("Soil nutrients are in good balance. Maintain with organic matter additions.")

        # ── Granite explanation ─────────────────────────────────
        prompt = (
            f"You are AgriSense AI, an expert soil scientist.\n\n"
            f"Soil test results:\n"
            f"  pH={ph}, N={nitrogen} kg/ha, P={phosphorus} kg/ha, K={potassium} kg/ha"
            + (f", Organic Matter={organic_matter}%" if organic_matter else "") + "\n"
            f"  Overall health score: {health_score}/100 ({status})\n\n"
            f"In 3-4 sentences, explain what these results mean for the farmer and the most "
            f"important corrective action they should take first.\n\nExplanation:"
        )
        explanation = self.generate(prompt)

        return {
            "health_score":    health_score,
            "status":          status,
            "recommendations": recs,
            "explanation":     explanation,
            "answer":          f"Soil Health: **{status}** ({health_score}/100)\n\n{explanation}",
            "sources":         ["ICAR Soil Health Guidelines", "IBM Granite"],
        }
