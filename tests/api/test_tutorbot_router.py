from __future__ import annotations

import importlib
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from deeptutor.services.auth.schemas import AuthenticatedUser

pytest.importorskip("fastapi")

FastAPI = pytest.importorskip("fastapi").FastAPI
TestClient = pytest.importorskip("fastapi.testclient").TestClient
tutorbot_module = importlib.import_module("deeptutor.api.routers.tutorbot")


def _build_app() -> FastAPI:
    app = FastAPI()
    app.include_router(tutorbot_module.router, prefix="/api/v1/tutorbot")
    return app


def _teacher_user(user_id: str = "teacher-1", role: str = "teacher") -> AuthenticatedUser:
    return AuthenticatedUser(
        id=user_id,
        email=f"{user_id}@example.com",
        display_name=f"Teacher {user_id}",
        role=role,
    )


def test_tutorbot_routes_require_authentication() -> None:
    with TestClient(_build_app()) as client:
        response = client.get("/api/v1/tutorbot")

    assert response.status_code == 401


def test_tutorbot_teacher_only_sees_owned_bots(monkeypatch) -> None:
    class FakeManager:
        def list_bots(self):
            return [
                {"bot_id": "owned", "owner_user_id": "teacher-1"},
                {"bot_id": "foreign", "owner_user_id": "teacher-2"},
            ]

    monkeypatch.setattr(tutorbot_module, "get_tutorbot_manager", lambda: FakeManager())
    app = _build_app()
    app.dependency_overrides[tutorbot_module.get_current_user] = lambda: _teacher_user()

    with TestClient(app) as client:
        response = client.get("/api/v1/tutorbot")

    assert response.status_code == 200
    assert [entry["bot_id"] for entry in response.json()] == ["owned"]


@pytest.mark.asyncio
async def test_tutorbot_create_injects_owner_metadata(monkeypatch) -> None:
    captured = {}

    class FakeManager:
        async def start_bot(self, bot_id, config):
            captured["bot_id"] = bot_id
            captured["config"] = config
            return SimpleNamespace(to_dict=lambda: {"bot_id": bot_id, "owner_user_id": config.owner_user_id})

    monkeypatch.setattr(tutorbot_module, "get_tutorbot_manager", lambda: FakeManager())
    app = _build_app()
    app.dependency_overrides[tutorbot_module.get_current_user] = lambda: _teacher_user()

    with TestClient(app) as client:
        response = client.post("/api/v1/tutorbot", json={"bot_id": "owned", "name": "Owned"})

    assert response.status_code == 200
    assert captured["bot_id"] == "owned"
    assert captured["config"].owner_user_id == "teacher-1"
    assert captured["config"].owner_email == "teacher-1@example.com"


def test_tutorbot_websocket_requires_authenticated_cookie(monkeypatch) -> None:
    monkeypatch.setattr(
        tutorbot_module,
        "get_current_user_from_websocket",
        lambda _ws: (_ for _ in ()).throw(HTTPException(status_code=401, detail="Authentication required")),
    )

    with TestClient(_build_app()) as client:
        with pytest.raises(Exception):
            with client.websocket_connect("/api/v1/tutorbot/owned/ws"):
                pass
