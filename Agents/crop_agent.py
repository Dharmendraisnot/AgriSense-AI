"""
agents/crop_agent.py

Recommends the most suitable crop using an ML classifier trained on the
Crop Recommendation Dataset, then explains the decision using IBM Granite.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from agents.base_agent import BaseAgent
from utils.logger import logger

# Lazy sklearn imports to keep startup fast
_MODEL_PATH = Path(__file__).parent.parent / "datasets" / "crop" / "crop_model.joblib"
_LABEL_PATH = Path(__file__).parent.parent / "datasets" / "crop" / "crop_labels.json"


class CropAgent(BaseAgent):
    """ML-based crop recommendation with Granite-powered explanation."""

    def __init__(self) -> None:
        super().__init__()
        self._clf = None
        self._labels: List[str] = []

    def _load_model(self):
        """Lazily load the trained scikit-learn model."""
        if self._clf is not None:
            return
        try:
            import joblib
            self._clf = joblib.load(_MODEL_PATH)
            if _LABEL_PATH.exists():
                self._labels = json.loads(_LABEL_PATH.read_text())
            logger.info("CropAgent: ML model loaded.")
        except FileNotFoundError:
            logger.warning("CropAgent: model file not found – will use rule-based fallback.")

    def _rule_based_recommend(self, params: Dict[str, Any]) -> str:
        """Simple rule-based fallback when the ML model is not yet trained."""
        ph = params.get("ph", 7.0)
        rainfall = params.get("rainfall", 100)
        temp = params.get("temperature", 25)

        if rainfall > 200 and temp > 25:
            return "Rice"
        if ph < 6.5 and rainfall < 100:
            return "Maize"
        if temp > 30 and rainfall < 60:
            return "Cotton"
        return "Wheat"

    async def recommend(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return await self.run(**params)

    async def run(
        self,
        message: str = "",
        location: Optional[str] = None,
        language: str = "en",
        nitrogen: float = 50,
        phosphorus: float = 50,
        potassium: float = 50,
        temperature: float = 25,
        humidity: float = 60,
        ph: float = 6.5,
        rainfall: float = 100,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        self._load_model()

        params = dict(
            nitrogen=nitrogen, phosphorus=phosphorus, potassium=potassium,
            temperature=temperature, humidity=humidity, ph=ph, rainfall=rainfall
        )

        # ── ML prediction ──────────────────────────────────────
        top_crops: List[Dict[str, Any]] = []
        if self._clf is not None:
            import numpy as np
            X = [[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]]
            proba = self._clf.predict_proba(X)[0]
            top_idx = proba.argsort()[::-1][:3]
            recommended_crop = self._labels[self._clf.predict(X)[0]] if self._labels else str(self._clf.predict(X)[0])
            top_crops = [
                {"crop": self._labels[i] if self._labels else str(i), "probability": round(float(proba[i]), 3)}
                for i in top_idx
            ]
            confidence = float(proba[top_idx[0]])
        else:
            recommended_crop = self._rule_based_recommend(params)
            confidence = 0.75
            top_crops = [{"crop": recommended_crop, "probability": confidence}]

        # ── Granite explanation ─────────────────────────────────
        prompt = (
            f"You are AgriSense AI, an expert agronomist.\n\n"
            f"Soil and climate conditions:\n"
            f"  N={nitrogen}, P={phosphorus}, K={potassium} kg/ha\n"
            f"  Temperature={temperature}°C, Humidity={humidity}%, pH={ph}, Rainfall={rainfall}mm\n\n"
            f"The AI model recommends growing: {recommended_crop}\n\n"
            f"Explain in 3-4 sentences why {recommended_crop} is the best choice for these conditions, "
            f"including what soil amendments (if any) the farmer should make.\n\nExplanation:"
        )
        explanation = self.generate(prompt)

        return {
            "recommended_crop": recommended_crop,
            "confidence":       confidence,
            "top_crops":        top_crops,
            "explanation":      explanation,
            "answer":           f"Recommended crop: **{recommended_crop}**\n\n{explanation}",
            "sources":          ["Crop Recommendation Dataset", "IBM Granite"],
        }
