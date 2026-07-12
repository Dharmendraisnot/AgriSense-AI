"""
config/settings.py
Centralised settings loader using pydantic-settings.
All configuration values are read from environment variables (or config/.env).

NOTE: lru_cache is intentionally NOT used here so that Streamlit Cloud secrets
pushed into os.environ by app.py are always picked up on first agent call.
"""
from __future__ import annotations

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Application-wide settings loaded from environment / .env file."""

    model_config = SettingsConfigDict(
        # env_file is optional — missing file is silently ignored on Cloud
        env_file=str(BASE_DIR / "config" / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ──────────────────────────────────────────────────
    app_name: str = "AgriSense AI"
    app_env:  str = "development"
    log_level: str = "INFO"

    # ── IBM watsonx.ai ───────────────────────────────────────
    watsonx_api_key:    str = ""
    watsonx_project_id: str = ""
    watsonx_url:        str = "https://eu-de.ml.cloud.ibm.com"
    watsonx_model_id:   str = "ibm/granite-4-h-small"

    # ── Weather API ──────────────────────────────────────────
    openweather_api_key:  str = ""
    openweather_base_url: str = "https://api.openweathermap.org/data/2.5"

    # ── Market Price API ─────────────────────────────────────
    agmarknet_api_key:  str = ""
    agmarknet_base_url: str = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

    # ── ChromaDB ─────────────────────────────────────────────
    chroma_persist_directory: str = "/tmp/chroma_db"
    chroma_collection_name:   str = "agrisense_knowledge_base"

    # ── Embedding ────────────────────────────────────────────
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # ── FastAPI ──────────────────────────────────────────────
    backend_host:   str  = "0.0.0.0"
    backend_port:   int  = 8000
    backend_reload: bool = False


def get_settings() -> Settings:
    """Return a fresh Settings instance (reads os.environ at call time)."""
    return Settings()
