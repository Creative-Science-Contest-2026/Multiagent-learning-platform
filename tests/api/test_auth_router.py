from __future__ import annotations

from email.message import EmailMessage
from urllib.parse import parse_qs, urlparse

import pytest

try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
except Exception:  # pragma: no cover
    FastAPI = None
    TestClient = None

pytestmark = pytest.mark.skipif(FastAPI is None or TestClient is None, reason="fastapi not installed")


def _build_app(tmp_path, monkeypatch: pytest.MonkeyPatch) -> FastAPI:
    from deeptutor.api.routers import auth
    from deeptutor.services.db.postgres import clear_auth_database_caches

    database_url = f"sqlite+pysqlite:///{tmp_path / 'auth-router.db'}"
    monkeypatch.setenv("DEEPTUTOR_AUTH_DATABASE_URL", database_url)
    monkeypatch.setenv("DEEPTUTOR_GOOGLE_CLIENT_ID", "google-client-id")
    monkeypatch.setenv("DEEPTUTOR_GOOGLE_CLIENT_SECRET", "google-client-secret")
    monkeypatch.setenv("DEEPTUTOR_GOOGLE_REDIRECT_URI", "http://localhost:8001/api/v1/auth/google/callback")
    clear_auth_database_caches()

    app = FastAPI()
    app.include_router(auth.router, prefix="/api/v1/auth")
    return app


def test_signup_rejects_admin_role_from_public_flow(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    with TestClient(_build_app(tmp_path, monkeypatch)) as client:
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "display_name": "Root Attempt",
                "email": "root@example.com",
                "password": "StrongPass123!",
                "role": "admin",
            },
        )

    assert response.status_code == 400


def test_signup_sets_session_cookie_for_teacher(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    with TestClient(_build_app(tmp_path, monkeypatch)) as client:
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "display_name": "Teacher One",
                "email": "teacher@example.com",
                "password": "StrongPass123!",
                "role": "teacher",
            },
        )

    assert response.status_code == 200
    assert response.json()["user"]["role"] == "teacher"
    assert "deeptutor_session=" in response.headers.get("set-cookie", "")


def test_signup_can_issue_secure_cookie_when_configured(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DEEPTUTOR_AUTH_COOKIE_SECURE", "1")
    monkeypatch.setenv("DEEPTUTOR_AUTH_COOKIE_SAMESITE", "strict")
    monkeypatch.setenv("DEEPTUTOR_AUTH_COOKIE_MAX_AGE_SECONDS", "7200")

    with TestClient(_build_app(tmp_path, monkeypatch)) as client:
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "display_name": "Teacher Two",
                "email": "teacher2@example.com",
                "password": "StrongPass123!",
                "role": "teacher",
            },
        )

    assert response.status_code == 200
    set_cookie = response.headers.get("set-cookie", "")
    assert "Secure" in set_cookie
    assert "SameSite=strict" in set_cookie
    assert "Max-Age=7200" in set_cookie


def test_login_returns_current_user_payload(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    with TestClient(_build_app(tmp_path, monkeypatch)) as client:
        signup_response = client.post(
            "/api/v1/auth/signup",
            json={
                "display_name": "Student One",
                "email": "student@example.com",
                "password": "StrongPass123!",
                "role": "student",
            },
        )
        assert signup_response.status_code == 200
        client.cookies.clear()

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "student@example.com",
                "password": "StrongPass123!",
            },
        )
        me_response = client.get("/api/v1/auth/me")

    assert login_response.status_code == 200
    assert login_response.json()["user"]["role"] == "student"
    assert me_response.status_code == 200
    assert me_response.json()["user"]["email"] == "student@example.com"


def test_me_requires_valid_session_cookie(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    with TestClient(_build_app(tmp_path, monkeypatch)) as client:
        response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_google_start_redirects_to_provider(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    with TestClient(_build_app(tmp_path, monkeypatch)) as client:
        response = client.get("/api/v1/auth/google/start?role=teacher", follow_redirects=False)

    assert response.status_code in {302, 307}
    assert "accounts.google.com" in response.headers["location"]


def test_google_start_preserves_safe_next_path_in_state(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    with TestClient(_build_app(tmp_path, monkeypatch)) as client:
        response = client.get(
            "/api/v1/auth/google/start?role=teacher&next=%2Fdashboard",
            follow_redirects=False,
        )

    assert response.status_code in {302, 307}
    query = parse_qs(urlparse(response.headers["location"]).query)
    assert '"role":"teacher"' in query["state"][0]
    assert '"next":"/dashboard"' in query["state"][0]


def test_google_callback_redirects_to_requested_next_path_for_teacher(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from deeptutor.services.auth.google_oauth import GoogleIdentity

    async def _fake_exchange(_code: str, _settings) -> GoogleIdentity:
        return GoogleIdentity(
            subject="google-subject-1",
            email="teacher@example.com",
            name="Teacher One",
        )

    monkeypatch.setattr(
        "deeptutor.api.routers.auth.exchange_google_code_for_identity",
        _fake_exchange,
    )

    with TestClient(_build_app(tmp_path, monkeypatch)) as client:
        response = client.get(
            '/api/v1/auth/google/callback?code=abc123&state={"role":"teacher","next":"/dashboard"}',
            follow_redirects=False,
        )

    assert response.status_code in {302, 307}
    assert response.headers["location"] == "/dashboard"
    assert "deeptutor_session=" in response.headers.get("set-cookie", "")


def test_forgot_password_is_generic_and_reset_token_changes_password(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with TestClient(_build_app(tmp_path, monkeypatch)) as client:
        signup_response = client.post(
            "/api/v1/auth/signup",
            json={
                "display_name": "Teacher One",
                "email": "teacher@example.com",
                "password": "StrongPass123!",
                "role": "teacher",
            },
        )
        assert signup_response.status_code == 200
        client.cookies.clear()

        forgot_response = client.post(
            "/api/v1/auth/forgot-password",
            json={"email": "teacher@example.com"},
        )

        assert forgot_response.status_code == 200
        payload = forgot_response.json()
        assert payload["ok"] is True
        assert payload["debug_token"]

        reset_response = client.post(
            "/api/v1/auth/reset-password",
            json={
                "token": payload["debug_token"],
                "password": "EvenStronger456!",
            },
        )
        assert reset_response.status_code == 200

        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "teacher@example.com",
                "password": "EvenStronger456!",
            },
        )

    assert login_response.status_code == 200
    assert login_response.json()["user"]["email"] == "teacher@example.com"


def test_send_verification_requires_auth_and_verify_email_marks_user_verified(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with TestClient(_build_app(tmp_path, monkeypatch)) as client:
        unauthenticated = client.post("/api/v1/auth/send-verification")
        assert unauthenticated.status_code == 401

        signup_response = client.post(
            "/api/v1/auth/signup",
            json={
                "display_name": "Student One",
                "email": "student@example.com",
                "password": "StrongPass123!",
                "role": "student",
            },
        )
        assert signup_response.status_code == 200

        send_response = client.post("/api/v1/auth/send-verification")
        assert send_response.status_code == 200
        payload = send_response.json()
        assert payload["ok"] is True
        assert payload["debug_token"]

        verify_response = client.post(
            "/api/v1/auth/verify-email",
            json={"token": payload["debug_token"]},
        )
        assert verify_response.status_code == 200

        me_response = client.get("/api/v1/auth/me")

    assert me_response.status_code == 200
    assert me_response.json()["user"]["email"] == "student@example.com"
    assert me_response.json()["user"]["email_verified_at"] is not None


def test_forgot_password_sends_email_when_smtp_is_configured(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sent_messages: list[EmailMessage] = []

    def _capture_send(_settings, message: EmailMessage) -> None:
        sent_messages.append(message)

    monkeypatch.setenv("DEEPTUTOR_AUTH_DEBUG_TOKENS", "0")
    monkeypatch.setenv("DEEPTUTOR_AUTH_SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("DEEPTUTOR_AUTH_FROM_ADDRESS", "noreply@example.com")
    monkeypatch.setenv("DEEPTUTOR_PUBLIC_APP_URL", "https://app.example.com")
    monkeypatch.setattr("deeptutor.api.routers.auth.send_auth_email", _capture_send)

    with TestClient(_build_app(tmp_path, monkeypatch)) as client:
        signup_response = client.post(
            "/api/v1/auth/signup",
            json={
                "display_name": "Teacher One",
                "email": "teacher@example.com",
                "password": "StrongPass123!",
                "role": "teacher",
            },
        )
        assert signup_response.status_code == 200
        client.cookies.clear()

        forgot_response = client.post(
            "/api/v1/auth/forgot-password",
            json={"email": "teacher@example.com"},
        )

    assert forgot_response.status_code == 200
    assert forgot_response.json() == {"ok": True}
    assert len(sent_messages) == 1
    assert sent_messages[0]["To"] == "teacher@example.com"
    assert "https://app.example.com/reset-password?token=" in sent_messages[0].get_content()


def test_send_verification_sends_email_when_smtp_is_configured(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sent_messages: list[EmailMessage] = []

    def _capture_send(_settings, message: EmailMessage) -> None:
        sent_messages.append(message)

    monkeypatch.setenv("DEEPTUTOR_AUTH_DEBUG_TOKENS", "0")
    monkeypatch.setenv("DEEPTUTOR_AUTH_SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("DEEPTUTOR_AUTH_FROM_ADDRESS", "noreply@example.com")
    monkeypatch.setenv("DEEPTUTOR_PUBLIC_APP_URL", "https://app.example.com")
    monkeypatch.setattr("deeptutor.api.routers.auth.send_auth_email", _capture_send)

    with TestClient(_build_app(tmp_path, monkeypatch)) as client:
        signup_response = client.post(
            "/api/v1/auth/signup",
            json={
                "display_name": "Student One",
                "email": "student@example.com",
                "password": "StrongPass123!",
                "role": "student",
            },
        )
        assert signup_response.status_code == 200

        send_response = client.post("/api/v1/auth/send-verification")

    assert send_response.status_code == 200
    assert send_response.json() == {"ok": True}
    assert len(sent_messages) == 1
    assert sent_messages[0]["To"] == "student@example.com"
    assert "https://app.example.com/verify-email?token=" in sent_messages[0].get_content()


def test_suspended_user_cannot_login_or_use_existing_session(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from deeptutor.services.auth.service import AuthService

    with TestClient(_build_app(tmp_path, monkeypatch)) as client:
        signup_response = client.post(
            "/api/v1/auth/signup",
            json={
                "display_name": "Teacher One",
                "email": "teacher@example.com",
                "password": "StrongPass123!",
                "role": "teacher",
            },
        )
        assert signup_response.status_code == 200
        user_id = signup_response.json()["user"]["id"]

        service = AuthService()
        updated_user = service.update_user_by_admin(user_id=user_id, status="suspended")
        assert updated_user is not None

        me_response = client.get("/api/v1/auth/me")
        client.cookies.clear()
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "teacher@example.com",
                "password": "StrongPass123!",
            },
        )

    assert me_response.status_code == 401
    assert login_response.status_code == 401


def test_google_callback_rejects_suspended_user(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from deeptutor.services.auth.google_oauth import GoogleIdentity
    from deeptutor.services.auth.service import AuthService

    async def _fake_exchange(_code: str, _settings) -> GoogleIdentity:
        return GoogleIdentity(
            subject="google-subject-suspended",
            email="teacher@example.com",
            name="Teacher One",
        )

    monkeypatch.setattr(
        "deeptutor.api.routers.auth.exchange_google_code_for_identity",
        _fake_exchange,
    )

    with TestClient(_build_app(tmp_path, monkeypatch)) as client:
        signup_response = client.post(
            "/api/v1/auth/signup",
            json={
                "display_name": "Teacher One",
                "email": "teacher@example.com",
                "password": "StrongPass123!",
                "role": "teacher",
            },
        )
        assert signup_response.status_code == 200
        user_id = signup_response.json()["user"]["id"]
        service = AuthService()
        updated_user = service.update_user_by_admin(user_id=user_id, status="suspended")
        assert updated_user is not None

        response = client.get(
            '/api/v1/auth/google/callback?code=abc123&state={"role":"teacher"}',
            follow_redirects=False,
        )

    assert response.status_code == 403
