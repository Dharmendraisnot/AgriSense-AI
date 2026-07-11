"""
backend/routes/chat.py
Main chat endpoint – delegates to the Coordinator Agent.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from backend.models.schemas import ChatRequest, ChatResponse
from agents.coordinator_agent import CoordinatorAgent

router = APIRouter()
_coordinator = CoordinatorAgent()


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Accept a natural-language farming question and return an AI-generated answer.
    The Coordinator Agent decides which specialist agent handles the query.
    """
    try:
        result = await _coordinator.process(
            message=request.message,
            location=request.location,
            language=request.language,
        )
        return ChatResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
