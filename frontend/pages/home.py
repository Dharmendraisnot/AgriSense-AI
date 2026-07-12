"""
frontend/pages/home.py
AgriSense AI – Home / Dashboard page.
"""
from __future__ import annotations

import streamlit as st


def render() -> None:
    # ── Header ──────────────────────────────────────────────
    st.markdown("""
    <div class="page-header">
        <h1>🌾 AgriSense AI</h1>
        <p>Agentic AI-Powered Smart Farming Advisor · Powered by IBM Granite & watsonx.ai</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Hero Banner ──────────────────────────────────────────
    st.markdown("""
    <div class="agri-card" style="background:linear-gradient(135deg,#e8f5e9,#f1f8e9);border-color:#66bb6a;">
        <h2 style="color:#1b5e20;margin:0 0 8px;">Welcome, Farmer! 🙏</h2>
        <p style="color:#2e7d32;margin:0;">
            Ask any farming question in plain language. AgriSense AI will route your query
            to the right AI agent — whether it's about crops, soil, weather, pests, or market prices.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Feature Cards ────────────────────────────────────────
    st.markdown("### What AgriSense AI Can Do For You")
    cols = st.columns(3)

    features = [
        ("🤖", "AI Chat Advisor",      "Ask any farming question in natural language. Get instant, explainable answers."),
        ("🌾", "Crop Recommendation",  "Get the best crop suggestion based on your soil nutrients and local climate."),
        ("🌦️", "Weather Advisory",     "Real-time weather data with crop impact analysis for your location."),
        ("🧪", "Soil Health Analysis", "Enter soil test values and get actionable remediation recommendations."),
        ("🐛", "Pest & Disease Guide", "Describe your crop symptoms and identify pests with treatment plans."),
        ("📈", "Live Mandi Prices",    "Check real-time commodity prices from Agmarknet before you sell."),
    ]

    for i, (icon, title, desc) in enumerate(features):
        col = cols[i % 3]
        with col:
            st.markdown(f"""
            <div class="metric-tile" style="text-align:left;margin-bottom:12px;">
                <div style="font-size:2rem;margin-bottom:8px;">{icon}</div>
                <strong style="color:#1b5e20;">{title}</strong>
                <p style="color:#555;font-size:0.87rem;margin:6px 0 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ── Quick Start ──────────────────────────────────────────
    st.markdown("### 🚀 Quick Start")
    st.info(
        "👈 Use the **sidebar** to navigate between tools, or go to **AI Chat** to start a "
        "conversation with your AgriSense advisor."
    )

    # ── Technology Stack ─────────────────────────────────────
    with st.expander("⚙️ Technology Stack"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**AI & Models**\n- IBM Granite 13B Chat\n- IBM watsonx.ai\n- sentence-transformers")
        with col2:
            st.markdown("**Backend & RAG**\n- FastAPI (Python)\n- ChromaDB Vector DB\n- Langflow Orchestration")
        with col3:
            st.markdown("**Data & APIs**\n- OpenWeatherMap\n- Agmarknet (data.gov.in)\n- ICAR / FAO / MoA Docs")

    st.caption("🏅 IBM SkillsBuild Internship Final Project · AgriSense AI v1.0")
