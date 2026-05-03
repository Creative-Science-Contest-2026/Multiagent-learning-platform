from __future__ import annotations

import pytest

try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
except Exception:  # pragma: no cover
    FastAPI = None
    TestClient = None

from deeptutor.services.auth.schemas import AuthenticatedUser

pytestmark = pytest.mark.skipif(FastAPI is None or TestClient is None, reason="fastapi not installed")


def _build_admin_app(tmp_path, monkeypatch: pytest.MonkeyPatch) -> FastAPI:
    from deeptutor.api.routers import admin_users
    from deeptutor.services.db.postgres import clear_auth_database_caches
    from deeptutor.services.auth.service import AuthService

    database_url = f"sqlite+pysqlite:///{tmp_path / 'admin-users.db'}"
    monkeypatch.setenv("DEEPTUTOR_AUTH_DATABASE_URL", database_url)
    clear_auth_database_caches()

    service = AuthService()
    service.create_user(
        email="admin@example.com",
        display_name="System Admin",
        role="admin",
        password="StrongPass123!",
    )

    app = FastAPI()
    app.include_router(admin_users.router, prefix="/api/v1/admin")
    app.dependency_overrides[admin_users.require_admin] = lambda: AuthenticatedUser(
        id="admin-user-id",
        email="admin@example.com",
        display_name="System Admin",
        role="admin",
    )
    return app


def test_admin_users_list_requires_admin_dependency(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    with TestClient(_build_admin_app(tmp_path, monkeypatch)) as client:
        response = client.get("/api/v1/admin/users")

    assert response.status_code == 200


def test_admin_can_create_teacher_accounts(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    with TestClient(_build_admin_app(tmp_path, monkeypatch)) as client:
        create_response = client.post(
            "/api/v1/admin/users",
            json={
                "display_name": "Teacher Two",
                "email": "teacher2@example.com",
                "password": "StrongPass123!",
                "role": "teacher",
            },
        )
        list_response = client.get("/api/v1/admin/users")

    assert create_response.status_code == 201
    assert create_response.json()["user"]["email"] == "teacher2@example.com"
    users = list_response.json()["users"]
    assert any(user["email"] == "teacher2@example.com" and user["role"] == "teacher" for user in users)


def test_admin_can_update_user_role_and_status(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    with TestClient(_build_admin_app(tmp_path, monkeypatch)) as client:
        create_response = client.post(
            "/api/v1/admin/users",
            json={
                "display_name": "Teacher Two",
                "email": "teacher2@example.com",
                "password": "StrongPass123!",
                "role": "teacher",
            },
        )
        user_id = create_response.json()["user"]["id"]

        update_response = client.patch(
            f"/api/v1/admin/users/{user_id}",
            json={
                "role": "student",
                "status": "suspended",
            },
        )
        list_response = client.get("/api/v1/admin/users")

    assert update_response.status_code == 200
    assert update_response.json()["user"]["role"] == "student"
    assert update_response.json()["user"]["status"] == "suspended"
    users = list_response.json()["users"]
    assert any(user["id"] == user_id and user["role"] == "student" and user["status"] == "suspended" for user in users)


def test_admin_cannot_suspend_or_demote_self(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    with TestClient(_build_admin_app(tmp_path, monkeypatch)) as client:
        suspend_response = client.patch(
            "/api/v1/admin/users/admin-user-id",
            json={"status": "suspended"},
        )
        demote_response = client.patch(
            "/api/v1/admin/users/admin-user-id",
            json={"role": "teacher"},
        )

    assert suspend_response.status_code == 400
    assert demote_response.status_code == 400
