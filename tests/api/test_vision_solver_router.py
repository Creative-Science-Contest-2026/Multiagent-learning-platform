from __future__ import annotations

import importlib

import pytest
from fastapi import HTTPException

from deeptutor.services.auth.schemas import AuthenticatedUser

pytest.importorskip("fastapi")

FastAPI = pytest.importorskip("fastapi").FastAPI
TestClient = pytest.importorskip("fastapi.testclient").TestClient
vision_solver_module = importlib.import_module("deeptutor.api.routers.vision_solver")


def _build_app() -> FastAPI:
    app = FastAPI()
    app.include_router(vision_solver_module.router, prefix="/api/v1")
    return app


def _user(user_id: str = "teacher-1") -> AuthenticatedUser:
    return AuthenticatedUser(
        id=user_id,
        email=f"{user_id}@example.com",
        display_name=f"User {user_id}",
        role="teacher",
    )


def test_vision_analyze_requires_authentication() -> None:
    with TestClient(_build_app()) as client:
        response = client.post("/api/v1/vision/analyze", json={"question": "hi"})

    assert response.status_code == 401


def test_vision_websocket_requires_authenticated_cookie(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        vision_solver_module,
        "get_current_user_from_websocket",
        lambda _ws: (_ for _ in ()).throw(HTTPException(status_code=401, detail="Authentication required")),
    )

    with TestClient(_build_app()) as client:
        with pytest.raises(Exception):
            with client.websocket_connect("/api/v1/vision/solve"):
                pass


def test_vision_analyze_uses_authenticated_user_override(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeAgent:
        def __init__(self, **kwargs):
            pass

        async def process(self, **kwargs):
            return {"has_image": False, "final_ggb_commands": [], "bbox_output": {}}

    async def _fake_resolve_image_input(**kwargs):
        return None

    monkeypatch.setattr(vision_solver_module, "resolve_image_input", _fake_resolve_image_input)
    monkeypatch.setattr(vision_solver_module, "get_llm_config", lambda: type("Cfg", (), {"api_key": "", "base_url": ""})())
    monkeypatch.setattr(vision_solver_module, "VisionSolverAgent", FakeAgent)
    app = _build_app()
    app.dependency_overrides[vision_solver_module.get_current_user] = lambda: _user()

    with TestClient(app) as client:
        response = client.post("/api/v1/vision/analyze", json={"question": "hi"})

    assert response.status_code == 200
