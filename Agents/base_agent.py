"""
agents/base_agent.py
Abstract base class every agent inherits from.
Provides shared watsonx.ai client initialisation and a common `generate` method.

All ibm_watsonx_ai / torch imports are DEFERRED to first use inside `_get_model()`.
This means:
  - Unit tests that mock `generate()` never trigger the torch DLL load.
  - Application startup is faster when credentials are not yet configured.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from config.settings import get_settings
from utils.logger import logger

settings = get_settings()


class BaseAgent(ABC):
    """Base class for all AgriSense AI agents."""

    def __init__(self) -> None:
        self._model: Optional[Any] = None   # ibm_watsonx_ai.ModelInference, lazily loaded

    def _get_model(self) -> Any:
        """Lazily initialise and return the IBM Granite ModelInference client."""
        if self._model is None:
            # Deferred imports – only executed when a real API call is needed
            from ibm_watsonx_ai import Credentials                          # noqa: PLC0415
            from ibm_watsonx_ai.foundation_models import ModelInference     # noqa: PLC0415
            from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams  # noqa: PLC0415

            default_params = {
                GenParams.MAX_NEW_TOKENS:      512,
                GenParams.MIN_NEW_TOKENS:      10,
                GenParams.TEMPERATURE:         0.7,
                GenParams.TOP_P:               0.9,
                GenParams.REPETITION_PENALTY:  1.1,
            }
            credentials = Credentials(
                url=settings.watsonx_url,
                api_key=settings.watsonx_api_key,
            )
            self._model = ModelInference(
                model_id=settings.watsonx_model_id,
                credentials=credentials,
                project_id=settings.watsonx_project_id,
                params=default_params,
            )
            logger.info(f"{self.__class__.__name__} initialised model {settings.watsonx_model_id}")
        return self._model

    def generate(self, prompt: str) -> str:
        """
        Call IBM Granite and return the generated text.
        Falls back to a placeholder string if credentials are not configured,
        so the UI stays functional during development without API keys.
        """
        if not settings.watsonx_api_key:
            logger.warning("watsonx_api_key not set – returning placeholder response.")
            return (
                "[IBM Granite response – configure WATSONX_API_KEY in config/.env to enable]\n\n"
                "Based on agricultural best practices, here is general guidance for your query."
            )
        try:
            model = self._get_model()
            response = model.generate_text(prompt=prompt)
            return response
        except Exception as exc:
            logger.error(f"Granite generation error: {exc}")
            raise

    @abstractmethod
    async def run(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Each agent must implement its primary action."""
        ...
