"""
frontend/pages/chat.py
AI Chat interface – routes messages through the Coordinator Agent directly
(no FastAPI backend required on Streamlit Cloud).
"""
from __future__ import annotations

import asyncio
import nest_asyncio
from typing import List, Dict

import streamlit as st

# Allow asyncio.run() inside Streamlit's already-running event loop
nest_asyncio.apply()


def _call_agent(message: str, location: str) -> Dict:
    """Run the Coordinator Agent in-process (works on Streamlit Cloud)."""
    try:
        from agents.coordinator_agent import CoordinatorAgent
        coordinator = CoordinatorAgent()
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(
            coordinator.process(message=message, location=location or None)
        )
        loop.close()
        return result
    except Exception as exc:
        return {
            "answer":     f"⚠️ Agent error: {exc}",
            "agent_used": "Error",
            "sources":    [],
        }


def render() -> None:
    st.markdown("""
    <div class="page-header">
        <h1>🤖 AI Chat Advisor</h1>
        <p>Ask anything about farming – crop selection, soil, weather, pests, or market prices.</p>
    </div>
    """, unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"]: List[Dict] = []

    location = st.session_state.get("location", "")

    # ── Example prompts ──────────────────────────────────────
    st.markdown("**💡 Try these example questions:**")
    examples = [
        "Which crop should I grow in Punjab this winter?",
        "What fertilizer should I use for wheat?",
        "What is today's price of rice in Delhi?",
        "My tomato leaves are turning yellow – what disease is this?",
        "What is the weather forecast for Pune today?",
    ]
    ex_cols = st.columns(len(examples))
    for col, ex in zip(ex_cols, examples):
        with col:
            if st.button(ex, key=f"ex_{ex[:20]}", use_container_width=True):
                st.session_state["pending_message"] = ex

    st.divider()

    # ── Chat display ─────────────────────────────────────────
    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="user-bubble">👨‍🌾 <strong>You:</strong> {msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            agent   = msg.get("agent_used", "AI Agent")
            sources = ", ".join(msg.get("sources", []))
            st.markdown(
                f'<div class="agent-bubble">🌾 <strong>{agent}:</strong><br>{msg["content"]}'
                + (f'<br><small style="color:#888">Sources: {sources}</small>' if sources else "")
                + "</div>",
                unsafe_allow_html=True,
            )

    # ── Input ────────────────────────────────────────────────
    pending = st.session_state.pop("pending_message", "")
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Your question",
            value=pending,
            placeholder="e.g. What crop should I grow this Rabi season?",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("Send 📤", use_container_width=True)

    if submitted and user_input.strip():
        st.session_state["chat_history"].append({"role": "user", "content": user_input})

        with st.spinner("🧠 AgriSense is thinking…"):
            response = _call_agent(user_input.strip(), location)

        st.session_state["chat_history"].append({
            "role":       "assistant",
            "content":    response.get("answer", "Sorry, I could not generate a response."),
            "agent_used": response.get("agent_used", "AI Agent"),
            "sources":    response.get("sources", []),
        })
        st.rerun()

    if st.session_state["chat_history"]:
        if st.button("🗑️ Clear Chat History"):
            st.session_state["chat_history"] = []
            st.rerun()
