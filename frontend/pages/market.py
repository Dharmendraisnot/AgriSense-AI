"""
frontend/pages/market.py
Live Mandi Prices page.
"""
from __future__ import annotations

import asyncio
import streamlit as st


_COMMODITIES = [
    "Wheat", "Rice", "Maize", "Soybean", "Mustard", "Groundnut",
    "Cotton", "Sugarcane", "Potato", "Onion", "Tomato",
]
_STATES = [
    "All India", "Andhra Pradesh", "Bihar", "Gujarat", "Haryana",
    "Karnataka", "Madhya Pradesh", "Maharashtra", "Punjab",
    "Rajasthan", "Tamil Nadu", "Telangana", "Uttar Pradesh", "West Bengal",
]


def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def render() -> None:
    st.markdown("""
    <div class="page-header">
        <h1>📈 Live Mandi Prices</h1>
        <p>Real-time commodity prices from Agmarknet (data.gov.in) with market advisory.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("market_form"):
        c1, c2 = st.columns(2)
        commodity = c1.selectbox("🌾 Commodity", _COMMODITIES)
        state     = c2.selectbox("📍 State", _STATES)
        submitted = st.form_submit_button("📊 Get Live Prices", use_container_width=True)

    if submitted:
        state_val = None if state == "All India" else state
        with st.spinner(f"Fetching {commodity} prices…"):
            try:
                from agents.market_agent import MarketAgent
                agent  = MarketAgent()
                result = _run(agent.get_prices({
                    "commodity": commodity, "state": state_val,
                }))

                col1, col2, col3 = st.columns(3)
                col1.metric("📉 Minimum Price", f"₹{result['min_price']:,.0f}", help="Per Quintal")
                col2.metric("📈 Maximum Price", f"₹{result['max_price']:,.0f}", help="Per Quintal")
                col3.metric("⚖️ Modal Price",   f"₹{result['modal_price']:,.0f}", help="Per Quintal")

                st.markdown(f"""
                <div class="agri-card" style="margin-top:12px;">
                    <strong>Market:</strong> {result['market']}, {result['state']}&nbsp;&nbsp;
                    <strong>Date:</strong> {result['date']}&nbsp;&nbsp;
                    <strong>Unit:</strong> {result.get('unit','Quintal')}
                </div>
                """, unsafe_allow_html=True)

                if result.get("answer"):
                    st.markdown("#### 💡 Market Advisory")
                    st.info(result["answer"])

                with st.expander("🔍 Sources"):
                    st.write(result.get("sources", []))

            except Exception as exc:
                st.error(f"Price fetch error: {exc}")
