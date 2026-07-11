"""
agents/coordinator_agent.py

The Coordinator Agent is the central router of AgriSense AI.
It classifies the user's intent and delegates to the correct specialist agent.
"""
from __future__ import annotations

import re
from typing import Any, Dict, Optional

from agents.base_agent import BaseAgent
from utils.logger import logger


# Intent → agent mapping
_INTENT_MAP = {
    "weather":  ["weather", "rain", "temperature", "forecast", "climate", "humidity", "monsoon"],
    "crop":     ["crop", "grow", "plant", "cultivate", "sow", "seed", "which crop", "season"],
    "soil":     ["soil", "ph", "nitrogen", "phosphorus", "potassium", "fertility", "nutrient"],
    "pest":     ["pest", "disease", "insect", "fungus", "blight", "wilt", "rot", "symptom"],
    "market":   ["price", "mandi", "market", "rate", "sell", "cost", "rupee", "kgrate"],
    "rag":      [],   # fallback — knowledge retrieval
}


class CoordinatorAgent(BaseAgent):
    """
    Routes incoming user queries to the appropriate specialist agent.
    Uses keyword matching + IBM Granite for ambiguous cases.
    """

    def _classify_intent(self, message: str) -> str:
        """Return the best-matching intent label for *message*."""
        lowered = message.lower()
        scores: Dict[str, int] = {intent: 0 for intent in _INTENT_MAP}
        for intent, keywords in _INTENT_MAP.items():
            for kw in keywords:
                if kw in lowered:
                    scores[intent] += 1

        best_intent = max(scores, key=lambda k: scores[k])
        if scores[best_intent] == 0:
            best_intent = "rag"   # no keyword matched → use RAG knowledge base

        logger.info(f"CoordinatorAgent classified intent as '{best_intent}' for: {message[:80]}")
        return best_intent

    async def process(
        self,
        message: str,
        location: Optional[str] = None,
        language: str = "en",
    ) -> Dict[str, Any]:
        """Classify intent, delegate to specialist, return response dict."""
        # Lazy imports to avoid circular dependencies
        from agents.weather_agent import WeatherAgent
        from agents.crop_agent import CropAgent
        from agents.soil_agent import SoilAgent
        from agents.pest_agent import PestAgent
        from agents.market_agent import MarketAgent
        from agents.rag_agent import RAGAgent

        intent = self._classify_intent(message)

        dispatch = {
            "weather": WeatherAgent(),
            "crop":    CropAgent(),
            "soil":    SoilAgent(),
            "pest":    PestAgent(),
            "market":  MarketAgent(),
            "rag":     RAGAgent(),
        }

        agent = dispatch[intent]
        result = await agent.run(message=message, location=location, language=language)
        result["agent_used"] = intent.replace("_", " ").title() + " Agent"
        return result

    async def run(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return await self.process(**kwargs)
