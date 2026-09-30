from fastapi.testclient import TestClient
from app.main import app
import app.api.chat as chat_module

client = TestClient(app)


def test_generation_failure_is_saved_and_shows_in_history(monkeypatch):
    monkeypatch.setattr(chat_module, "check_clarification_needed", lambda q, s: {"needs_clarification": False, "question": None})
    monkeypatch.setattr(chat_module, "generate_sql", lambda q, s: None)

    response = client.post("/api/chat", json={"session_id": None, "message": "anything"})
    data = response.json()

    assert data["status"] == "failed"
    session_id = data["session_id"]

    history_response = client.get(f"/api/history?session_id={session_id}")
    history_data = history_response.json()

    assert history_data["total"] == 1
    assert history_data["items"][0]["status"] == "failed"


def test_unsafe_sql_is_saved_and_shows_in_history(monkeypatch):
    monkeypatch.setattr(chat_module, "check_clarification_needed", lambda q, s: {"needs_clarification": False, "question": None})
    monkeypatch.setattr(chat_module, "generate_sql", lambda q, s: "DROP TABLE customers;")

    response = client.post("/api/chat", json={"session_id": None, "message": "anything"})
    data = response.json()

    assert data["status"] == "failed"
    session_id = data["session_id"]

    history_response = client.get(f"/api/history?session_id={session_id}")
    history_data = history_response.json()

    assert history_data["total"] == 1
    assert history_data["items"][0]["status"] == "failed"