"""
tests/integration/test_api.py
Integration tests for the FastAPI backend.
Requires the backend to be running or uses TestClient.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock


@pytest.fixture(scope="module")
def client():
    from backend.main import app
    return TestClient(app)


def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


def test_root(client):
    resp = client.get("/")
    assert resp.status_code == 200


@patch("agents.coordinator_agent.CoordinatorAgent.process", new_callable=AsyncMock,
       return_value={"answer": "Test answer", "agent_used": "Test Agent", "sources": []})
def test_chat_endpoint(mock_process, client):
    resp = client.post("/api/chat/", json={"message": "What crop should I grow?"})
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
