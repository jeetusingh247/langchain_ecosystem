import pytest
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def test_schema():
    response = client.get("/schema")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_create_session():
    response = client.post("/session/create")
    assert response.status_code == 200
    assert "session_id" in response.json()

def test_query_missing_question():
    response = client.post("/query", json={})
    assert response.status_code == 400
    assert "Missing 'question'" in str(response.json())

def test_query_invalid_sql(monkeypatch):
    # Patch the agent to return unsafe SQL
    from app.agent import langchain_agent
    monkeypatch.setattr(langchain_agent, "generate_sql", lambda prompt: "DROP TABLE users;")
    response = client.post("/query", json={"question": "delete all users"})
    assert response.status_code == 400
    assert "Unsafe or non-SELECT SQL" in str(response.json())
