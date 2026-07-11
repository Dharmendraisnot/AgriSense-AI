"""
utils/logger.py
Centralised Loguru logger used across the entire application.
"""
from __future__ import annotations

import sys
from loguru import logger
from config.settings import get_settings

settings = get_settings()

# Remove default handler and add a nicely formatted one
logger.remove()
logger.add(
    sys.stdout,
    level=settings.log_level,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> – <level>{message}</level>",
    colorize=True,
)
logger.add(
    "logs/agrisense_{time:YYYY-MM-DD}.log",
    level="DEBUG",
    rotation="1 day",
    retention="7 days",
    compression="zip",
    enqueue=True,
)
