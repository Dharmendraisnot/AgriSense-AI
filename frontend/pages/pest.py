"""
frontend/pages/pest.py
Pest & Disease Identification page.
"""
from __future__ import annotations

import asyncio
import streamlit as st

_SEVERITY_COLORS = {"Low": "#43a047", "Medium": "#fb8c00", "High": "#e53935"}


def render() -> None:
    st.markdown("""
    <div class="page-header">
        <h1>🐛 Pest & Disease Identification</h1>
        <p>Describe your crop symptoms and get an AI-powered diagnosis with treatment plan.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("pest_form"):
        crop = st.selectbox(
            "🌱 Crop Name",
            ["Wheat", "Rice", "Maize", "Tomato", "Cotton", "Sugarcane",
             "Potato", "Soybean", "Groundnut", "Mustard", "Other"],
        )
        if crop == "Other":
            crop = st.text_input("Specify crop")

        symptoms = st.text_area(
            "🔍 Describe the symptoms",
            placeholder="e.g. Yellow spots on leaves, white powder on stems, wilting of young plants…",
            height=120,
        )
        location = st.text_input("📍 Location (optional)", value=st.session_state.get("location", ""))
        submitted = st.form_submit_button("🔎 Identify Pest / Disease", use_container_width=True)

    if submitted and symptoms.strip():
        with st.spinner("Analysing symptoms…"):
            try:
                from agents.pest_agent import PestAgent
                agent = PestAgent()
                result = asyncio.run(agent.identify({
                    "crop": crop, "symptoms": symptoms, "location": location or None,
                }))

                severity = result.get("severity", "Medium")
                color    = _SEVERITY_COLORS.get(severity, "#fb8c00")
                pest     = result.get("pest_or_disease", "Unknown")

                st.markdown(f"""
                <div class="agri-card">
                    <h3 style="margin:0 0 4px;color:#1b5e20;">Identified: {pest}</h3>
                    <span style="color:{color};font-weight:600;">⚠ Severity: {severity}</span>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 💊 Treatment Options")
                    for t in result.get("treatment", []):
                        st.markdown(f"• {t}")
                with col2:
                    st.markdown("#### 🛡️ Prevention Measures")
                    for p in result.get("prevention", []):
                        st.markdown(f"• {p}")

                st.markdown("#### 📝 Detailed Explanation")
                st.write(result.get("explanation", ""))

                with st.expander("🔍 Sources"):
                    st.write(result.get("sources", []))

            except Exception as exc:
                st.error(f"Identification error: {exc}")
    elif submitted:
        st.warning("Please describe the symptoms before submitting.")
