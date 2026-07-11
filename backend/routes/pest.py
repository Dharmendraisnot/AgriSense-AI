"""
backend/routes/pest.py
Pest & disease identification endpoint.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from backend.models.schemas import PestRequest, PestResponse
from agents.pest_agent import PestAgent

router = APIRouter()
_agent = PestAgent()


@router.post("/identify", response_model=PestResponse)
async def identify_pest(request: PestRequest) -> PestResponse:
    """Identify pest/disease from crop name and symptoms."""
    try:
        result = await _agent.identify(request.model_dump())
        return PestResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
