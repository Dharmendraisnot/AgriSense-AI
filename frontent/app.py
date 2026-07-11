"""
frontend/app.py
AgriSense AI – Streamlit multi-page application entry-point.

Run with:
    streamlit run frontend/app.py
"""
import os
import streamlit as st

# Push Streamlit secrets into environment variables
# so pydantic-settings can read them
for key, value in st.secrets.items():
    os.environ[key.upper()] = str(value)
from __future__ import annotations

import sys
from pathlib import Path

# Ensure the project root is on sys.path so all imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

# ── Page configuration (must be first Streamlit call) ────────────────────────
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

from frontend.components.sidebar import render_sidebar
from frontend.components.styles import inject_css

# Inject global CSS
inject_css()

# Render sidebar navigation
page = render_sidebar()

# ── Dynamic page routing ──────────────────────────────────────────────────────
if page == "Home":
    from frontend.pages.home import render
elif page == "AI Chat":
    from frontend.pages.chat import render
elif page == "Crop Recommendation":
    from frontend.pages.crop import render
elif page == "Weather":
    from frontend.pages.weather import render
elif page == "Soil Analysis":
    from frontend.pages.soil import render
elif page == "Pest & Disease":
    from frontend.pages.pest import render
elif page == "Market Prices":
    from frontend.pages.market import render
elif page == "About":
    from frontend.pages.about import render
else:
    from frontend.pages.home import render

render()
