"""
utils/helpers.py
Miscellaneous helper functions shared across the project.
"""
from __future__ import annotations

import re
from typing import Any


def clean_text(text: str) -> str:
    """Strip extra whitespace and normalize newlines."""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def truncate_text(text: str, max_chars: int = 500) -> str:
    """Truncate text to *max_chars* with an ellipsis."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "…"


def format_currency(amount: float, currency: str = "₹") -> str:
    """Format a numeric amount as a currency string."""
    return f"{currency}{amount:,.2f}"


def safe_get(d: dict, *keys: str, default: Any = None) -> Any:
    """Safely traverse nested dicts without raising KeyError."""
    for key in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(key, default)
    return d
