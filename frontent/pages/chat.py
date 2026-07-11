"""
frontend/pages/chat.py
AI Chat interface – routes messages through the Coordinator Agent.
"""
from __future__ import annotations

import asyncio
from typing import List, Dict

import streamlit as st


def _call_backend(message: str, location: str) -> Dict:
    """Call the FastAPI backend /api/chat endpoint via HTTP."""
    import httpx
    try:
        with httpx.Client(timeout=60) as client:
            resp = client.post(
                "http://localhost:8000/api/chat/",
                json={"message": message, "location": location or None},
            )
            resp.raise_for_status()
            return resp.json()
    except Exception as exc:
        # Graceful in-process fallback (no backend running)
        return _in_process_fallback(message, location, str(exc))


def _in_process_fallback(message: str, location: str, err: str) -> Dict:
    """Run the coordinator agent directly when the backend is not available."""
    try:
        from agents.coordinator_agent import CoordinatorAgent
        coordinator = CoordinatorAgent()
        result = asyncio.run(coordinator.process(message=message, location=location or None))
        return result
    except Exception as exc2:
        return {
            "answer":     f"⚠️ Could not connect to backend: {err}\nDirect call error: {exc2}",
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

    # ── Session state ────────────────────────────────────────
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
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state["chat_history"]:
            if msg["role"] == "user":
                st.markdown(
                    f'<div class="user-bubble">👨‍🌾 <strong>You:</strong> {msg["content"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                agent = msg.get("agent_used", "AI Agent")
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
            response = _call_backend(user_input.strip(), location)

        st.session_state["chat_history"].append({
            "role":       "assistant",
            "content":    response.get("answer", "Sorry, I could not generate a response."),
            "agent_used": response.get("agent_used", "AI Agent"),
            "sources":    response.get("sources", []),
        })
        st.rerun()

    # ── Clear history ────────────────────────────────────────
    if st.session_state["chat_history"]:
        if st.button("🗑️ Clear Chat History"):
            st.session_state["chat_history"] = []
            st.rerun()
