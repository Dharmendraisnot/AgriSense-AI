"""
backend/routes/crop.py
Crop recommendation endpoint.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from backend.models.schemas import CropRequest, CropResponse
from agents.crop_agent import CropAgent

router = APIRouter()
_agent = CropAgent()


@router.post("/recommend", response_model=CropResponse)
async def recommend_crop(request: CropRequest) -> CropResponse:
    """Return the best crop to grow given soil and climate parameters."""
    try:
        result = await _agent.recommend(request.model_dump())
        return CropResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
