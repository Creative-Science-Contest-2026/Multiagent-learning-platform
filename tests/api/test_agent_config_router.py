from __future__ import annotations

import importlib

import pytest

from deeptutor.services.auth.schemas import AuthenticatedUser

pytest.importorskip("fastapi")

FastAPI = pytest.importorskip("fastapi").FastAPI
TestClient = pytest.importorskip("fastapi.testclient").TestClient
agent_config_module = importlib.import_module("deeptutor.api.routers.agent_config")


def _build_app() -> FastAPI:
    app = FastAPI()
    app.include_router(agent_config_module.router, prefix="/api/v1/agent-config")
    return app


def _user() -> AuthenticatedUser:
    return AuthenticatedUser(
        id="teacher-1",
        email="teacher-1@example.com",
        display_name="Teacher One",
        role="teacher",
    )


def test_agent_config_routes_require_authentication() -> None:
    with TestClient(_build_app()) as client:
        response = client.get("/api/v1/agent-config/agents")

    assert response.status_code == 401


def test_agent_config_routes_return_data_for_authenticated_user() -> None:
    app = _build_app()
    app.dependency_overrides[agent_config_module.get_current_user] = _user

    with TestClient(app) as client:
        response = client.get("/api/v1/agent-config/agents")

    assert response.status_code == 200
    assert "solve" in response.json()
