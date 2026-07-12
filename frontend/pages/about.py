"""
frontend/pages/about.py
About Project page.
"""
from __future__ import annotations

import streamlit as st


def render() -> None:
    st.markdown("""
    <div class="page-header">
        <h1>ℹ️ About AgriSense AI</h1>
        <p>IBM SkillsBuild Final Internship Project</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="agri-card">
        <h3 style="color:#1b5e20;margin:0 0 8px;">🎯 Project Objective</h3>
        <p>
        AgriSense AI is a production-ready, agentic AI-powered web application that helps
        small-scale farmers make better agricultural decisions. It combines IBM watsonx.ai
        (Granite models), Retrieval-Augmented Generation (RAG) with ChromaDB, real-time APIs,
        and a Langflow-orchestrated multi-agent system to deliver localized, accurate, and
        explainable farming recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Architecture diagram ──────────────────────────────────
    st.markdown("### 🏗️ Architecture")
    st.code("""
User Query
    │
    ▼
Streamlit UI  ──►  FastAPI Backend
                         │
                    Coordinator Agent
                    (keyword + LLM routing)
                         │
           ┌─────────────┼──────────────┐─────────────┐
           ▼             ▼              ▼             ▼         ▼
     Weather         Crop          Soil          Pest       Market
      Agent         Agent         Agent         Agent       Agent
           │             │              │             │         │
           └─────────────┴──────────────┴─────────────┴─────────┘
                                   │
                         RAG Agent (ChromaDB)
                                   │
                         IBM watsonx.ai (Granite)
                                   │
                         Explainable Answer
    """, language="")

    # ── Agent table ───────────────────────────────────────────
    st.markdown("### 🤖 AI Agents")
    agents = {
        "🌦️ Weather Agent":        "Fetches real-time weather from OpenWeatherMap and generates crop impact advisories.",
        "🌾 Crop Agent":           "ML classifier (scikit-learn) trained on Crop Recommendation Dataset + Granite explanation.",
        "🧪 Soil Agent":           "Scores soil health using ICAR guidelines and generates amendment recommendations.",
        "🐛 Pest & Disease Agent": "Identifies pests from symptoms using PlantVillage RAG context and IBM Granite.",
        "📈 Market Agent":         "Fetches live mandi prices from Agmarknet API and provides selling advisory.",
        "📚 RAG Agent":            "Semantic retrieval over ICAR/FAO/MoA documents + IBM Granite answer generation.",
        "🧠 Coordinator Agent":    "Routes user queries to the correct specialist agent via keyword + LLM classification.",
    }
    for name, desc in agents.items():
        st.markdown(f"**{name}** – {desc}")

    # ── Tech Stack ────────────────────────────────────────────
    st.markdown("### ⚙️ Technology Stack")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **AI & ML**
        - IBM Granite 13B Chat v2
        - IBM watsonx.ai
        - scikit-learn
        - sentence-transformers
        """)
    with col2:
        st.markdown("""
        **Backend & Data**
        - FastAPI (Python 3.11)
        - ChromaDB (Vector DB)
        - Pydantic v2
        - Pandas / NumPy
        """)
    with col3:
        st.markdown("""
        **APIs & Tools**
        - OpenWeatherMap
        - Agmarknet (data.gov.in)
        - Langflow
        - Streamlit
        """)

    st.divider()
    st.caption("Built with ❤️ for IBM SkillsBuild Internship Program · AgriSense AI v1.0")
