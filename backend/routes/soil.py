"""
backend/routes/soil.py
Soil health analysis endpoint.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from backend.models.schemas import SoilRequest, SoilResponse
from agents.soil_agent import SoilAgent

router = APIRouter()
_agent = SoilAgent()


@router.post("/analyze", response_model=SoilResponse)
async def analyze_soil(request: SoilRequest) -> SoilResponse:
    """Analyze soil health parameters and return recommendations."""
    try:
        result = await _agent.analyze(request.model_dump())
        return SoilResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
