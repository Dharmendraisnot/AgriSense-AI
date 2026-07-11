"""
backend/routes/weather.py
Weather information endpoint.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from backend.models.schemas import WeatherRequest, WeatherResponse
from agents.weather_agent import WeatherAgent

router = APIRouter()
_agent = WeatherAgent()


@router.post("/", response_model=WeatherResponse)
async def get_weather(request: WeatherRequest) -> WeatherResponse:
    """Fetch current weather and return a farming advisory."""
    try:
        result = await _agent.get_weather_advisory(request.location)
        return WeatherResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
