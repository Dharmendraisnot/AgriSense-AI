"""
backend/models/schemas.py
Pydantic request / response models for all API routes.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ── Chat ──────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="User's farming question")
    location: Optional[str] = Field(None, description="Farmer's location (city or state)")
    language: Optional[str] = Field("en", description="Response language code")

class ChatResponse(BaseModel):
    answer: str
    agent_used: str
    sources: List[str] = []
    confidence: Optional[float] = None


# ── Crop Recommendation ───────────────────────────────────────────────────────

class CropRequest(BaseModel):
    nitrogen: float = Field(..., ge=0, description="Nitrogen content in soil (kg/ha)")
    phosphorus: float = Field(..., ge=0, description="Phosphorus content in soil (kg/ha)")
    potassium: float = Field(..., ge=0, description="Potassium content in soil (kg/ha)")
    temperature: float = Field(..., description="Average temperature (°C)")
    humidity: float = Field(..., ge=0, le=100, description="Relative humidity (%)")
    ph: float = Field(..., ge=0, le=14, description="Soil pH")
    rainfall: float = Field(..., ge=0, description="Annual rainfall (mm)")

class CropResponse(BaseModel):
    recommended_crop: str
    confidence: float
    top_crops: List[Dict[str, Any]] = []
    explanation: str


# ── Weather ───────────────────────────────────────────────────────────────────

class WeatherRequest(BaseModel):
    location: str = Field(..., min_length=2, description="City or district name")

class WeatherResponse(BaseModel):
    location: str
    temperature: float
    humidity: float
    description: str
    wind_speed: float
    farming_advisory: str


# ── Soil Health ───────────────────────────────────────────────────────────────

class SoilRequest(BaseModel):
    ph: float = Field(..., ge=0, le=14)
    nitrogen: float = Field(..., ge=0)
    phosphorus: float = Field(..., ge=0)
    potassium: float = Field(..., ge=0)
    organic_matter: Optional[float] = Field(None, ge=0)
    location: Optional[str] = None

class SoilResponse(BaseModel):
    health_score: float
    status: str                # "Excellent", "Good", "Fair", "Poor"
    recommendations: List[str]
    explanation: str


# ── Pest & Disease ────────────────────────────────────────────────────────────

class PestRequest(BaseModel):
    crop: str = Field(..., description="Crop name")
    symptoms: str = Field(..., description="Observed symptoms on the crop")
    location: Optional[str] = None

class PestResponse(BaseModel):
    pest_or_disease: str
    severity: str              # "Low", "Medium", "High"
    treatment: List[str]
    prevention: List[str]
    explanation: str


# ── Market Prices ─────────────────────────────────────────────────────────────

class MarketRequest(BaseModel):
    commodity: str = Field(..., description="Commodity / crop name")
    state: Optional[str] = None
    district: Optional[str] = None

class MarketResponse(BaseModel):
    commodity: str
    state: str
    market: str
    min_price: float
    max_price: float
    modal_price: float
    unit: str = "Quintal"
    date: str
