"""
tests/unit/test_agents.py
Unit tests for all AgriSense AI agents.
Tests run without real API keys using mocked watsonx responses.
"""
from __future__ import annotations

import asyncio
from unittest.mock import MagicMock, patch

import pytest


# ── Coordinator Agent ──────────────────────────────────────────────────────────

class TestCoordinatorAgent:
    def test_intent_weather(self):
        from agents.coordinator_agent import CoordinatorAgent
        agent = CoordinatorAgent()
        assert agent._classify_intent("What is the weather in Mumbai?") == "weather"

    def test_intent_crop(self):
        from agents.coordinator_agent import CoordinatorAgent
        agent = CoordinatorAgent()
        assert agent._classify_intent("Which crop should I grow this season?") == "crop"

    def test_intent_soil(self):
        from agents.coordinator_agent import CoordinatorAgent
        agent = CoordinatorAgent()
        assert agent._classify_intent("My soil ph is 5.5 what should I do?") == "soil"

    def test_intent_pest(self):
        from agents.coordinator_agent import CoordinatorAgent
        agent = CoordinatorAgent()
        assert agent._classify_intent("My wheat has a disease with yellow spots") == "pest"

    def test_intent_market(self):
        from agents.coordinator_agent import CoordinatorAgent
        agent = CoordinatorAgent()
        assert agent._classify_intent("What is the mandi price for wheat today?") == "market"

    def test_intent_fallback(self):
        from agents.coordinator_agent import CoordinatorAgent
        agent = CoordinatorAgent()
        assert agent._classify_intent("Hello, how are you?") == "rag"


# ── Soil Agent ─────────────────────────────────────────────────────────────────

class TestSoilAgent:
    def test_score_optimal(self):
        from agents.soil_agent import _score_param
        assert _score_param(7.0, 6.0, 7.5) == 1.0

    def test_score_below(self):
        from agents.soil_agent import _score_param
        score = _score_param(3.0, 6.0, 7.5)
        assert 0.0 <= score < 1.0

    @patch("agents.base_agent.BaseAgent.generate", return_value="Good soil.")
    def test_soil_analysis(self, mock_gen):
        from agents.soil_agent import SoilAgent
        agent  = SoilAgent()
        result = asyncio.run(agent.analyze({
            "ph": 6.5, "nitrogen": 300, "phosphorus": 30, "potassium": 200
        }))
        assert "health_score" in result
        assert result["health_score"] > 0
        assert result["status"] in ("Excellent", "Good", "Fair", "Poor")


# ── Crop Agent ─────────────────────────────────────────────────────────────────

class TestCropAgent:
    @patch("agents.base_agent.BaseAgent.generate", return_value="Great choice.")
    def test_rule_based_fallback(self, mock_gen):
        from agents.crop_agent import CropAgent
        agent  = CropAgent()
        # Model file won't exist in CI, rule-based fallback kicks in
        result = asyncio.run(agent.recommend({
            "nitrogen": 50, "phosphorus": 50, "potassium": 50,
            "temperature": 30, "humidity": 70, "ph": 6.5, "rainfall": 250,
        }))
        assert "recommended_crop" in result
        assert isinstance(result["confidence"], float)


# ── Weather Agent ──────────────────────────────────────────────────────────────

class TestWeatherAgent:
    @patch("agents.base_agent.BaseAgent.generate", return_value="Stay hydrated.")
    def test_mock_weather(self, mock_gen):
        from agents.weather_agent import WeatherAgent
        agent  = WeatherAgent()
        result = asyncio.run(agent.get_weather_advisory("TestCity"))
        assert "temperature" in result
        assert "farming_advisory" in result


# ── Market Agent ───────────────────────────────────────────────────────────────

class TestMarketAgent:
    @patch("agents.base_agent.BaseAgent.generate", return_value="Good time to sell.")
    def test_mock_prices(self, mock_gen):
        from agents.market_agent import MarketAgent
        agent  = MarketAgent()
        result = asyncio.run(agent.get_prices({"commodity": "Wheat"}))
        assert "modal_price" in result
        assert result["commodity"] == "Wheat"
