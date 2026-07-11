"""
frontend/pages/soil.py
Soil Health Analysis page.
"""
from __future__ import annotations

import asyncio
import streamlit as st


_BADGE = {
    "Excellent": "badge-excellent",
    "Good":      "badge-good",
    "Fair":      "badge-fair",
    "Poor":      "badge-poor",
}


def render() -> None:
    st.markdown("""
    <div class="page-header">
        <h1>🧪 Soil Health Analysis</h1>
        <p>Enter your soil test results to get a health score and improvement recommendations.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("soil_form"):
        c1, c2 = st.columns(2)
        ph          = c1.slider("Soil pH",          min_value=0.0, max_value=14.0, value=6.5,  step=0.1)
        organic_mat = c2.number_input("Organic Matter (%)", min_value=0.0, max_value=15.0, value=2.5, step=0.1)

        c3, c4, c5 = st.columns(3)
        nitrogen   = c3.number_input("Nitrogen (kg/ha)",   min_value=0.0, max_value=1000.0, value=280.0, step=5.0)
        phosphorus = c4.number_input("Phosphorus (kg/ha)", min_value=0.0, max_value=200.0,  value=25.0,  step=1.0)
        potassium  = c5.number_input("Potassium (kg/ha)",  min_value=0.0, max_value=600.0,  value=200.0, step=5.0)

        location = st.text_input("📍 Location (optional)", value=st.session_state.get("location", ""))
        submitted = st.form_submit_button("🔬 Analyse Soil Health", use_container_width=True)

    if submitted:
        with st.spinner("Analysing soil health…"):
            try:
                from agents.soil_agent import SoilAgent
                agent = SoilAgent()
                result = asyncio.run(agent.analyze({
                    "ph": ph, "nitrogen": nitrogen,
                    "phosphorus": phosphorus, "potassium": potassium,
                    "organic_matter": organic_mat, "location": location or None,
                }))

                score  = result["health_score"]
                status = result["status"]
                badge_cls = _BADGE.get(status, "badge-fair")

                st.markdown(f"""
                <div class="agri-card">
                    <h3 style="margin:0 0 4px;color:#1b5e20;">Soil Health Score</h3>
                    <span style="font-size:2.5rem;font-weight:700;color:#2e7d32;">{score}</span>
                    <span style="font-size:1rem;color:#555;">/100</span>&nbsp;&nbsp;
                    <span class="{badge_cls}">{status}</span>
                </div>
                """, unsafe_allow_html=True)

                st.progress(score / 100)

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 📝 Explanation")
                    st.write(result.get("explanation", ""))
                with col2:
                    st.markdown("#### ✅ Recommendations")
                    for rec in result.get("recommendations", []):
                        st.markdown(f"• {rec}")

                with st.expander("🔍 Sources"):
                    st.write(result.get("sources", []))

            except Exception as exc:
                st.error(f"Analysis error: {exc}")
