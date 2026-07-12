"""
agents/weather_agent.py

Fetches real-time weather from OpenWeatherMap and generates a farming advisory
using IBM Granite via RAG-augmented prompting.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from agents.base_agent import BaseAgent
from config.settings import get_settings
from utils.logger import logger


class WeatherAgent(BaseAgent):
    """Fetches weather data and returns a crop-impact advisory."""

    async def get_weather_advisory(self, location: str) -> Dict[str, Any]:
        return await self.run(message=location, location=location)

    async def run(
        self,
        message: str = "",
        location: Optional[str] = None,
        language: str = "en",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        loc = location or self._extract_location(message) or message
        weather_data = await self._fetch_weather(loc)

        prompt = self._build_prompt(loc, weather_data)
        advisory = self.generate(prompt)

        return {
            "location":         weather_data.get("name", loc),
            "temperature":      weather_data.get("main", {}).get("temp", 0),
            "humidity":         weather_data.get("main", {}).get("humidity", 0),
            "description":      weather_data.get("weather", [{}])[0].get("description", ""),
            "wind_speed":       weather_data.get("wind", {}).get("speed", 0),
            "farming_advisory": advisory,
            "answer":           advisory,
            "sources":          ["OpenWeatherMap API", "IBM Granite"],
        }

    async def _fetch_weather(self, location: str) -> Dict[str, Any]:
        """Call OpenWeatherMap current weather API."""
        settings = get_settings()
        if not settings.openweather_api_key or settings.openweather_api_key.startswith("your_"):
            logger.warning("OpenWeather API key not set – returning mock data.")
            return self._mock_weather(location)

        url = f"{settings.openweather_base_url}/weather"
        params = {
            "q":     location,
            "appid": settings.openweather_api_key,
            "units": "metric",
        }
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                return resp.json()
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 401:
                logger.warning(
                    "OpenWeather API key returned 401 – key may still be activating "
                    "(OpenWeatherMap keys can take up to 30 min after registration). "
                    "Returning mock data."
                )
            else:
                logger.error(f"OpenWeather API error {exc.response.status_code}: {exc}")
            return self._mock_weather(location)
        except Exception as exc:
            logger.error(f"OpenWeather request failed: {exc}")
            return self._mock_weather(location)

    @staticmethod
    def _extract_location(message: str) -> Optional[str]:
        """
        Best-effort extraction of a place name from a free-text message.
        Handles patterns like "weather in Mumbai", "forecast for Pune", etc.
        Returns None if no location can be found.
        """
        import re
        patterns = [
            r"\bin\s+([A-Za-z][A-Za-z\s,]+?)(?:\s+today|\s+tomorrow|\s+this|\?|$)",
            r"\bfor\s+([A-Za-z][A-Za-z\s,]+?)(?:\s+today|\s+tomorrow|\s+this|\?|$)",
            r"\bat\s+([A-Za-z][A-Za-z\s,]+?)(?:\s+today|\s+tomorrow|\s+this|\?|$)",
        ]
        for pat in patterns:
            m = re.search(pat, message, re.IGNORECASE)
            if m:
                loc = m.group(1).strip().rstrip(",")
                if 2 <= len(loc) <= 50:
                    return loc
        return None

    @staticmethod
    def _mock_weather(location: str) -> Dict[str, Any]:
        return {
            "name": location,
            "main": {"temp": 28.5, "humidity": 65},
            "weather": [{"description": "partly cloudy"}],
            "wind": {"speed": 3.2},
        }

    @staticmethod
    def _build_prompt(location: str, data: Dict[str, Any]) -> str:
        temp      = data.get("main", {}).get("temp", "N/A")
        humidity  = data.get("main", {}).get("humidity", "N/A")
        desc      = data.get("weather", [{}])[0].get("description", "N/A")
        wind      = data.get("wind", {}).get("speed", "N/A")
        return (
            f"You are AgriSense AI, an expert agricultural advisor.\n\n"
            f"Current weather in {location}:\n"
            f"  - Temperature : {temp}°C\n"
            f"  - Humidity    : {humidity}%\n"
            f"  - Condition   : {desc}\n"
            f"  - Wind Speed  : {wind} m/s\n\n"
            f"Based on this weather, provide a concise farming advisory covering:\n"
            f"1. Crop irrigation needs\n"
            f"2. Pest/disease risk\n"
            f"3. Harvesting or sowing advice\n"
            f"4. Any weather precautions the farmer should take.\n\n"
            f"Advisory:"
        )
