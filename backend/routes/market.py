"""
backend/routes/market.py
Live mandi / market price endpoint.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from backend.models.schemas import MarketRequest, MarketResponse
from agents.market_agent import MarketAgent

router = APIRouter()
_agent = MarketAgent()


@router.post("/prices", response_model=MarketResponse)
async def get_market_prices(request: MarketRequest) -> MarketResponse:
    """Fetch live mandi prices for a commodity."""
    try:
        result = await _agent.get_prices(request.model_dump())
        return MarketResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
