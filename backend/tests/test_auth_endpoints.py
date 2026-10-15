import uuid
from fastapi.testclient import TestClient
from app.main import app
import app.api.chat as chat_module

client = TestClient(app)

PASSWORD = "testpassword123"


def _unique_email() -> str:
    return f"test_{uuid.uuid4().hex}@example.com"


def _register(email: str):
    return client.post("/api/auth/register", json={"email": email, "password": PASSWORD})


def _auth_headers(email: str) -> dict:
    token = _register(email).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_register_returns_a_token():
    response = _register(_unique_email())
    data = response.json()

    assert response.status_code == 200
    assert data["token_type"] == "bearer"
    assert data["access_token"]


def test_registering_the_same_email_twice_returns_400():
    email = _unique_email()
    _register(email)

    response = _register(email)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_with_correct_password_returns_a_token():
    email = _unique_email()
    _register(email)

    response = client.post("/api/auth/login", json={"email": email, "password": PASSWORD})

    assert response.status_code == 200
    assert response.json()["access_token"]


def test_login_with_wrong_password_returns_401():
    email = _unique_email()
    _register(email)

    response = client.post("/api/auth/login", json={"email": email, "password": "wrongpassword"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_with_unknown_email_gives_the_same_error_as_wrong_password():
    # Same message for both cases, so an attacker can't tell which emails are registered
    response = client.post("/api/auth/login", json={"email": _unique_email(), "password": PASSWORD})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_register_rejects_an_invalid_email_format():
    response = client.post("/api/auth/register", json={"email": "not-an-email", "password": PASSWORD})

    assert response.status_code == 422


def test_chat_requires_a_token():
    response = client.post("/api/chat", json={"session_id": None, "message": "anything"})

    assert response.status_code == 401


def test_history_rejects_a_garbage_token():
    response = client.get(
        "/api/history?session_id=1",
        headers={"Authorization": "Bearer this.is.not.a.real.token"},
    )

    assert response.status_code == 401


def test_user_cannot_read_another_users_session(monkeypatch):
    # Skip the LLM so the test is fast and predictable
    monkeypatch.setattr(chat_module, "check_clarification_needed", lambda q, s: {"needs_clarification": False, "question": None})
    monkeypatch.setattr(chat_module, "generate_sql", lambda q, s: None)

    owner_headers = _auth_headers(_unique_email())
    other_headers = _auth_headers(_unique_email())

    chat_response = client.post(
        "/api/chat",
        json={"session_id": None, "message": "anything"},
        headers=owner_headers,
    )
    session_id = chat_response.json()["session_id"]

    # The owner can read their own session
    owner_history = client.get(f"/api/history?session_id={session_id}", headers=owner_headers)
    assert owner_history.status_code == 200

    # A different user gets a 404, as if the session didn't exist
    other_history = client.get(f"/api/history?session_id={session_id}", headers=other_headers)
    assert other_history.status_code == 404


def test_register_rejects_a_password_longer_than_72_bytes():
    response = client.post("/api/auth/register", json={"email": _unique_email(), "password": "a" * 73})

    assert response.status_code == 422


def test_register_counts_bytes_not_characters():
    # 40 two-byte characters is only 40 characters long, but 80 bytes
    response = client.post("/api/auth/register", json={"email": _unique_email(), "password": "é" * 40})

    assert response.status_code == 422


def test_register_rejects_a_password_shorter_than_8_characters():
    response = client.post("/api/auth/register", json={"email": _unique_email(), "password": "short"})

    assert response.status_code == 422


def test_login_rejects_a_password_longer_than_72_bytes():
    response = client.post("/api/auth/login", json={"email": _unique_email(), "password": "a" * 73})

    assert response.status_code == 422


def test_register_accepts_a_password_of_exactly_72_bytes():
    response = client.post("/api/auth/register", json={"email": _unique_email(), "password": "a" * 72})

    assert response.status_code == 200
    assert response.json()["access_token"]