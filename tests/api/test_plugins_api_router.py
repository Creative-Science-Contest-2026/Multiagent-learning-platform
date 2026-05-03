from __future__ import annotations

import importlib

import pytest

from deeptutor.services.auth.schemas import AuthenticatedUser

pytest.importorskip("fastapi")

FastAPI = pytest.importorskip("fastapi").FastAPI
TestClient = pytest.importorskip("fastapi.testclient").TestClient
plugins_module = importlib.import_module("deeptutor.api.routers.plugins_api")


def _build_app() -> FastAPI:
    app = FastAPI()
    app.include_router(plugins_module.router, prefix="/api/v1/plugins")
    return app


def _user(user_id: str = "admin-1", role: str = "admin") -> AuthenticatedUser:
    return AuthenticatedUser(
        id=user_id,
        email=f"{user_id}@example.com",
        display_name=f"User {user_id}",
        role=role,
    )


def test_plugins_routes_require_authentication() -> None:
    with TestClient(_build_app()) as client:
        response = client.get("/api/v1/plugins/list")

    assert response.status_code == 401


def test_plugins_routes_are_admin_only() -> None:
    app = _build_app()
    app.dependency_overrides[plugins_module.get_current_user] = lambda: _user(role="teacher")

    with TestClient(app) as client:
        response = client.get("/api/v1/plugins/list")

    assert response.status_code == 403
