import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import app.services.auth_service as auth_service
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)


def test_hash_is_not_the_plaintext_password():
    assert hash_password("mypassword123") != "mypassword123"


def test_verify_accepts_correct_password():
    hashed = hash_password("mypassword123")
    assert verify_password("mypassword123", hashed) is True


def test_verify_rejects_wrong_password():
    hashed = hash_password("mypassword123")
    assert verify_password("wrongpassword", hashed) is False


def test_same_password_hashes_differently_each_time():
    # bcrypt adds a random salt, so two hashes of the same password differ
    assert hash_password("mypassword123") != hash_password("mypassword123")


def test_token_round_trip_keeps_the_subject():
    token = create_access_token({"sub": "42"})
    payload = decode_access_token(token)
    assert payload["sub"] == "42"


def test_expired_token_is_rejected(monkeypatch):
    # Make new tokens expire one minute in the past
    monkeypatch.setattr(auth_service, "ACCESS_TOKEN_EXPIRE_MINUTES", -1)
    token = create_access_token({"sub": "42"})

    with pytest.raises(JWTError):
        decode_access_token(token)


def test_token_signed_with_wrong_key_is_rejected():
    forged = jwt.encode(
        {"sub": "42", "exp": datetime.now(timezone.utc) + timedelta(minutes=5)},
        "not-the-real-secret",
        algorithm=auth_service.ALGORITHM,
    )

    with pytest.raises(JWTError):
        decode_access_token(forged)