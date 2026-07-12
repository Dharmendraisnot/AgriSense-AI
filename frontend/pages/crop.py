"""
frontend/pages/crop.py
Crop Recommendation page.
"""
from __future__ import annotations

import asyncio
import streamlit as st


def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def render() -> None:
    st.markdown("""
    <div class="page-header">
        <h1>🌾 Crop Recommendation</h1>
        <p>Enter your soil parameters and local conditions to get the best crop suggestion.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("crop_form"):
        st.markdown("#### 🧪 Soil Nutrients (kg/ha)")
        c1, c2, c3 = st.columns(3)
        nitrogen    = c1.number_input("Nitrogen (N)",    min_value=0.0, max_value=200.0, value=50.0,  step=1.0)
        phosphorus  = c2.number_input("Phosphorus (P)",  min_value=0.0, max_value=200.0, value=50.0,  step=1.0)
        potassium   = c3.number_input("Potassium (K)",   min_value=0.0, max_value=300.0, value=50.0,  step=1.0)

        st.markdown("#### 🌡️ Climate Conditions")
        c4, c5, c6, c7 = st.columns(4)
        temperature = c4.number_input("Temperature (°C)", min_value=-10.0, max_value=55.0,  value=25.0,  step=0.5)
        humidity    = c5.number_input("Humidity (%)",     min_value=0.0,   max_value=100.0, value=60.0,  step=1.0)
        ph          = c6.number_input("Soil pH",          min_value=0.0,   max_value=14.0,  value=6.5,   step=0.1)
        rainfall    = c7.number_input("Rainfall (mm)",    min_value=0.0,   max_value=500.0, value=100.0, step=5.0)

        submitted = st.form_submit_button("🌱 Recommend Crop", use_container_width=True)

    if submitted:
        with st.spinner("Analysing your conditions…"):
            try:
                from agents.crop_agent import CropAgent
                agent = CropAgent()
                result = _run(agent.recommend({
                    "nitrogen": nitrogen, "phosphorus": phosphorus, "potassium": potassium,
                    "temperature": temperature, "humidity": humidity, "ph": ph, "rainfall": rainfall,
                }))

                st.success(f"✅ Recommended Crop: **{result['recommended_crop']}**")

                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown("#### 📝 Explanation")
                    st.markdown(result.get("explanation", ""))
                with col2:
                    st.markdown("#### 📊 Confidence")
                    st.progress(float(result.get("confidence", 0.75)))
                    st.caption(f"{float(result.get('confidence', 0.75)) * 100:.0f}%")

                    if result.get("top_crops"):
                        st.markdown("**Top Alternatives:**")
                        for item in result["top_crops"][1:]:
                            st.write(f"• {item['crop']} ({item['probability']*100:.0f}%)")

                with st.expander("🔍 Sources"):
                    st.write(result.get("sources", []))

            except Exception as exc:
                st.error(f"Error: {exc}")
