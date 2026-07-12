"""
agents/market_agent.py

Retrieves live mandi prices from the Agmarknet API (data.gov.in)
and provides a market context advisory using IBM Granite.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from agents.base_agent import BaseAgent
from config.settings import get_settings
from utils.logger import logger


class MarketAgent(BaseAgent):
    """Fetches live commodity prices and generates a selling advisory."""

    async def get_prices(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return await self.run(**params)

    async def run(
        self,
        message: str = "",
        location: Optional[str] = None,
        language: str = "en",
        commodity: str = "Wheat",
        state: Optional[str] = None,
        district: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        commodity = commodity or message
        price_data = await self._fetch_prices(commodity, state, district)

        prompt = (
            f"You are AgriSense AI, an agricultural market expert.\n\n"
            f"Current mandi price data for {commodity}:\n"
            f"  Market: {price_data['market']}, {price_data['state']}\n"
            f"  Min Price: Rs.{price_data['min_price']}/quintal\n"
            f"  Max Price: Rs.{price_data['max_price']}/quintal\n"
            f"  Modal Price: Rs.{price_data['modal_price']}/quintal\n"
            f"  Date: {price_data['date']}\n\n"
            f"In 2-3 sentences, advise the farmer on whether this is a good time to sell "
            f"{commodity} and what price range they should expect.\n\nAdvisory:"
        )
        advisory = self.generate(prompt)
        price_data["answer"] = advisory
        price_data["sources"] = ["Agmarknet API (data.gov.in)", "IBM Granite"]
        return price_data

    async def _fetch_prices(
        self, commodity: str, state: Optional[str], district: Optional[str]
    ) -> Dict[str, Any]:
        """Fetch live prices from Agmarknet API."""
        settings = get_settings()
        if not settings.agmarknet_api_key:
            logger.warning("Agmarknet API key not set – returning mock data.")
            return self._mock_prices(commodity, state)

        params: Dict[str, Any] = {
            "api-key":    settings.agmarknet_api_key,
            "format":     "json",
            "filters[commodity]": commodity,
            "limit": 1,
        }
        if state:
            params["filters[state]"] = state
        if district:
            params["filters[district]"] = district

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(settings.agmarknet_base_url, params=params)
                resp.raise_for_status()
                data = resp.json()
            record = data["records"][0]
            return {
                "commodity":   record.get("commodity", commodity),
                "state":       record.get("state", state or "India"),
                "market":      record.get("market", "N/A"),
                "min_price":   float(record.get("min_price", 0)),
                "max_price":   float(record.get("max_price", 0)),
                "modal_price": float(record.get("modal_price", 0)),
                "unit":        "Quintal",
                "date":        record.get("arrival_date", "N/A"),
            }
        except Exception as exc:
            logger.error(f"Agmarknet API error: {exc} – returning mock data.")
            return self._mock_prices(commodity, state)

    @staticmethod
    def _mock_prices(commodity: str, state: Optional[str]) -> Dict[str, Any]:
        return {
            "commodity":   commodity,
            "state":       state or "India",
            "market":      "Sample Market",
            "min_price":   2000.0,
            "max_price":   2500.0,
            "modal_price": 2200.0,
            "unit":        "Quintal",
            "date":        "N/A (mock data – configure AGMARKNET_API_KEY)",
        }
