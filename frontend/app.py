"""
frontend/app.py
AgriSense AI – Streamlit multi-page application entry-point.

Run with:
    streamlit run frontend/app.py
"""
from __future__ import annotations

import os
import sys
import importlib
from pathlib import Path

# ── sys.path setup ────────────────────────────────────────────────────────────
# _here  = the folder that contains this file (named "frontend" locally,
#           but "frontent" on Streamlit Cloud due to a repo typo).
# _root  = the repo root one level above.
_here = Path(__file__).resolve().parent      # …/frontend  OR  …/frontent
_root = _here.parent                         # …/agrisense-ai
for _p in (_root, _here):
    _s = str(_p)
    if _s not in sys.path:
        sys.path.insert(0, _s)

# _pkg is the actual folder name on disk ("frontend" or "frontent").
_pkg = _here.name

# ── Apply nest_asyncio once so asyncio.new_event_loop() works inside Streamlit
import nest_asyncio
nest_asyncio.apply()

import streamlit as st

# ── Push Streamlit secrets → os.environ (for pydantic-settings) ──────────────
try:
    for _k, _v in st.secrets.items():
        os.environ[_k.upper()] = str(_v)
except Exception:
    pass   # No secrets configured yet (local dev)

# ── Page configuration (must be the FIRST Streamlit call) ────────────────────
st.set_page_config(
    page_title="AgriSense AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/your-username/agrisense-ai",
        "About": "AgriSense AI – IBM SkillsBuild Internship Project",
    },
)

# ── Import components (once, cached in sys.modules) ───────────────────────────
_sidebar_mod = importlib.import_module(f"{_pkg}.components.sidebar")
_styles_mod  = importlib.import_module(f"{_pkg}.components.styles")
render_sidebar = _sidebar_mod.render_sidebar
inject_css     = _styles_mod.inject_css

inject_css()
page = render_sidebar()

# ── Dynamic page routing ──────────────────────────────────────────────────────
_PAGE_MAP = {
    "Home":                "home",
    "AI Chat":             "chat",
    "Crop Recommendation": "crop",
    "Weather":             "weather",
    "Soil Analysis":       "soil",
    "Pest & Disease":      "pest",
    "Market Prices":       "market",
    "About":               "about",
}
_mod_name = _PAGE_MAP.get(page, "home")
_page_mod = importlib.import_module(f"{_pkg}.pages.{_mod_name}")
_page_mod.render()
