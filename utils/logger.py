"""
utils/logger.py
Centralised Loguru logger used across the entire application.
Writes to stdout only on Streamlit Cloud (no filesystem log file).
"""
from __future__ import annotations

import os
import sys
from loguru import logger

# Remove the default Loguru handler
logger.remove()

# Always log to stdout
logger.add(
    sys.stdout,
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} – {message}",
    colorize=False,
)

# Only write a log file if the logs/ directory is writable (local dev)
_log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
try:
    os.makedirs(_log_dir, exist_ok=True)
    _test_file = os.path.join(_log_dir, ".write_test")
    with open(_test_file, "w") as _f:
        _f.write("")
    os.remove(_test_file)
    logger.add(
        os.path.join(_log_dir, "agrisense_{time:YYYY-MM-DD}.log"),
        level="DEBUG",
        rotation="1 day",
        retention="7 days",
        compression="zip",
        enqueue=True,
    )
except Exception:
    pass  # Read-only filesystem (Streamlit Cloud) — stdout only
