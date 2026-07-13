"""
frontend/components/styles.py
Injects global CSS into the Streamlit app.
"""
from __future__ import annotations

import streamlit as st


_CSS = """
<style>
/* ── Global ───────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
}

/* ── Sidebar ──────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a3a1a 0%, #0d240d 100%);
}
[data-testid="stSidebar"] * { color: #e8f5e9 !important; }
[data-testid="stSidebar"] .stButton > button {
    background: transparent;
    border: 1px solid #4caf5055;
    border-radius: 8px;
    color: #a5d6a7 !important;
    text-align: left;
    transition: background 0.2s;
    margin-bottom: 2px;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #4caf5022;
    border-color: #4caf50;
    color: #ffffff !important;
}

/* ── Global Contrast Fix ──────────────── */
/* Forces dark text color and overrides Streamlit's dark-mode white injection */
.agri-card, .agent-bubble, .user-bubble, .metric-tile,
.agri-card *, .agent-bubble *, .user-bubble *, .metric-tile * {
    color: #1a1a1a !important;
}

/* Reset headings inside cards so they keep their unique green accent accents */
.agri-card h3, .metric-tile h3 {
    color: #1b5e20 !important;
}

/* ── Cards ────────────────────────────── */
.agri-card {
    background: #f1f8e9;
    border: 1px solid #c5e1a5;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
}

/* ── Metric tiles ─────────────────────── */
.metric-tile {
    background: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}
.metric-tile h3 { margin: 0; font-size: 1.6rem; color: #2e7d32; }
.metric-tile p  { margin: 4px 0 0; color: #555 !important; font-size: 0.85rem; }

/* ── Chat bubbles ─────────────────────── */
.user-bubble {
    background: #e8f5e9;
    border-radius: 16px 16px 4px 16px;
    padding: 10px 16px;
    margin: 6px 0;
    max-width: 80%;
    margin-left: auto;
    border: 1px solid #a5d6a7;
}
.agent-bubble {
    background: #f3f4f6;
    border-radius: 16px 16px 16px 4px;
    padding: 10px 16px;
    margin: 6px 0;
    max-width: 85%;
    border: 1px solid #d1d5db;
}

/* ── Page header ──────────────────────── */
.page-header {
    padding: 12px 0 4px;
    border-bottom: 2px solid #4caf50;
    margin-bottom: 24px;
}
.page-header h1 { margin: 0; color: #1b5e20; }
.page-header p  { margin: 4px 0 0; color: #555; }

/* ── Status badges ────────────────────── */
.badge-excellent { color: #1b5e20 !important; background:#c8e6c9; padding:2px 10px; border-radius:20px; font-size:.8rem; }
.badge-good      { color: #33691e !important; background:#dcedc8; padding:2px 10px; border-radius:20px; font-size:.8rem; }
.badge-fair      { color: #e65100 !important; background:#ffe0b2; padding:2px 10px; border-radius:20px; font-size:.8rem; }
.badge-poor      { color: #b71c1c !important; background:#ffcdd2; padding:2px 10px; border-radius:20px; font-size:.8rem; }
</style>
"""


def inject_css() -> None:
    """Inject the global stylesheet."""
    st.markdown(_CSS, unsafe_allow_html=True)
