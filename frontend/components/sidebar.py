"""
frontend/components/sidebar.py
Renders the sidebar navigation and returns the selected page name.
"""
from __future__ import annotations

import streamlit as st

_PAGES = [
    ("🏠", "Home"),
    ("🤖", "AI Chat"),
    ("🌾", "Crop Recommendation"),
    ("🌦️", "Weather"),
    ("🧪", "Soil Analysis"),
    ("🐛", "Pest & Disease"),
    ("📈", "Market Prices"),
    ("ℹ️", "About"),
]


def render_sidebar() -> str:
    """Render the sidebar and return the selected page name."""
    with st.sidebar:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/5/51/IBM_logo.svg",
            width=80,
        )
        st.markdown("## 🌾 AgriSense AI")
        st.caption("IBM SkillsBuild · Smart Farming Advisor")
        st.divider()

        # Initialise key once so Streamlit never raises KeyError
        if "location_input" not in st.session_state:
            st.session_state["location_input"] = st.session_state.get("location", "")

        st.text_input(
            "📍 Your Location",
            placeholder="e.g. Pune, Maharashtra",
            key="location_input",
        )
        # Keep the shared "location" alias in sync
        st.session_state["location"] = st.session_state["location_input"]

        st.divider()
        st.markdown("**Navigate**")

        # Build buttons for each page
        if "page" not in st.session_state:
            st.session_state["page"] = "Home"

        for icon, name in _PAGES:
            if st.button(f"{icon} {name}", use_container_width=True, key=f"nav_{name}"):
                st.session_state["page"] = name

        st.divider()
        st.caption("Powered by IBM Granite · ChromaDB · Streamlit")

    return str(st.session_state.get("page", "Home"))
