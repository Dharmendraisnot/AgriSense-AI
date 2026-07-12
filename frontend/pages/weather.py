"""
frontend/pages/weather.py
Weather Information & Farming Advisory page.
"""
from __future__ import annotations

import asyncio
import streamlit as st


def render() -> None:
    st.markdown("""
    <div class="page-header">
        <h1>🌦️ Weather & Farming Advisory</h1>
        <p>Real-time weather data with personalised farming recommendations.</p>
    </div>
    """, unsafe_allow_html=True)

    location = st.text_input(
        "📍 Enter your location",
        value=st.session_state.get("location", ""),
        placeholder="e.g. Nagpur, Maharashtra",
    )

    if st.button("🔍 Get Weather & Advisory", use_container_width=True, disabled=not location):
        with st.spinner(f"Fetching weather for {location}…"):
            try:
                from agents.weather_agent import WeatherAgent
                agent = WeatherAgent()
                result = asyncio.run(agent.get_weather_advisory(location))

                # ── Metrics row ──
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("🌡️ Temperature", f"{result['temperature']}°C")
                col2.metric("💧 Humidity",    f"{result['humidity']}%")
                col3.metric("🌬️ Wind Speed",  f"{result['wind_speed']} m/s")
                col4.metric("☁️ Condition",   result["description"].title())

                st.divider()
                st.markdown("#### 🌾 Farming Advisory")
                st.markdown(
                    f'<div class="agri-card">{result["farming_advisory"]}</div>',
                    unsafe_allow_html=True,
                )

                with st.expander("🔍 Sources"):
                    st.write(result.get("sources", []))

            except Exception as exc:
                st.error(f"Could not fetch weather: {exc}")

    elif not location:
        st.info("👆 Enter a location to get the weather forecast and farming advisory.")
