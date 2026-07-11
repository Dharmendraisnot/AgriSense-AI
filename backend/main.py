"""
backend/main.py
FastAPI application entry-point for AgriSense AI.
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import get_settings
from backend.routes import chat, crop, weather, soil, pest, market

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Agentic AI-Powered Smart Farming Advisor – IBM SkillsBuild",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(chat.router,    prefix="/api/chat",    tags=["Chat"])
app.include_router(crop.router,    prefix="/api/crop",    tags=["Crop Recommendation"])
app.include_router(weather.router, prefix="/api/weather", tags=["Weather"])
app.include_router(soil.router,    prefix="/api/soil",    tags=["Soil Health"])
app.include_router(pest.router,    prefix="/api/pest",    tags=["Pest & Disease"])
app.include_router(market.router,  prefix="/api/market",  tags=["Market Prices"])


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "app": settings.app_name}


@app.get("/api/health", tags=["Health"])
async def health():
    return {"status": "healthy", "version": "1.0.0"}
