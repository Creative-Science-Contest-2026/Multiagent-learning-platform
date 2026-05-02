from __future__ import annotations

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
