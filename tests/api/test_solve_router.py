from __future__ import annotations

import importlib
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from deeptutor.services.auth.schemas import AuthenticatedUser

pytest.importorskip("fastapi")

FastAPI = pytest.importorskip("fastapi").FastAPI
TestClient = pytest.importorskip("fastapi.testclient").TestClient
DeepSolveCapability = importlib.import_module("deeptutor.capabilities.deep_solve").DeepSolveCapability


class _DummyLogInterceptor:
    def __init__(self, *_args, **_kwargs) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> bool:
        return False


def _import_solve_module(monkeypatch: pytest.MonkeyPatch, tmp_path):
    config_path = tmp_path / "main.yaml"
    config_path.write_text("system:\n  language: en\npaths: {}\nlogging: {}\n", encoding="utf-8")
    monkeypatch.setattr(
        "deeptutor.services.config.loader.resolve_config_path",
        lambda _config_file, _project_root=None: (config_path, config_path.parent),
    )
    module = importlib.import_module("deeptutor.api.routers.solve")
    return importlib.reload(module)


def _build_app(solve_module) -> FastAPI:
    app = FastAPI()
    app.include_router(solve_module.router, prefix="/api/v1")
    return app


def _teacher_user() -> AuthenticatedUser:
    return AuthenticatedUser(
        id="teacher-1",
        email="teacher@example.com",
        display_name="Teacher One",
        role="teacher",
    )


def test_solve_router_uses_explicit_default_tools(monkeypatch, tmp_path) -> None:
    solve_module = _import_solve_module(monkeypatch, tmp_path)
    captured: dict[str, object] = {}

    class FakeMainSolver:
        def __init__(self, **kwargs) -> None:
            captured["init"] = kwargs
            self.logger = SimpleNamespace(logger=SimpleNamespace(), display_manager=None)
            self.token_tracker = None

        async def ainit(self) -> None:
            captured["ainit"] = True

        async def solve(self, *_args, **_kwargs):
            return {"final_answer": "done", "output_dir": str(tmp_path / "solve"), "metadata": {}}

    monkeypatch.setattr("deeptutor.api.routers.solve.MainSolver", FakeMainSolver)
    monkeypatch.setattr("deeptutor.api.routers.solve.LogInterceptor", _DummyLogInterceptor)
    monkeypatch.setattr(
        "deeptutor.api.routers.solve.get_llm_config",
        lambda: SimpleNamespace(api_key="k", base_url="u", api_version="v1"),
    )
    monkeypatch.setattr(
        "deeptutor.api.routers.solve.get_path_service",
        lambda: SimpleNamespace(get_solve_dir=lambda: Path(tmp_path)),
    )
    monkeypatch.setattr("deeptutor.api.routers.solve.get_ui_language", lambda default="en": default)
    monkeypatch.setattr("deeptutor.api.routers.solve.get_current_user_from_websocket", lambda _ws: _teacher_user())

    app = _build_app(solve_module)

    with TestClient(app) as client:
        with client.websocket_connect("/api/v1/solve") as websocket:
            websocket.send_json({"question": "Solve x^2=4"})
            messages = [websocket.receive_json() for _ in range(4)]

    assert [message["type"] for message in messages] == ["session", "task_id", "status", "result"]
    assert captured["init"]["enabled_tools"] == list(DeepSolveCapability.manifest.tools_used)
    assert captured["init"]["kb_name"] == "ai-textbook"
    assert captured["init"]["disable_planner_retrieve"] is False


def test_solve_router_respects_disabled_tools(monkeypatch, tmp_path) -> None:
    solve_module = _import_solve_module(monkeypatch, tmp_path)
    captured: dict[str, object] = {}

    class FakeMainSolver:
        def __init__(self, **kwargs) -> None:
            captured["init"] = kwargs
            self.logger = SimpleNamespace(logger=SimpleNamespace(), display_manager=None)
            self.token_tracker = None

        async def ainit(self) -> None:
            captured["ainit"] = True

        async def solve(self, *_args, **_kwargs):
            return {"final_answer": "done", "output_dir": str(tmp_path / "solve"), "metadata": {}}

    monkeypatch.setattr("deeptutor.api.routers.solve.MainSolver", FakeMainSolver)
    monkeypatch.setattr("deeptutor.api.routers.solve.LogInterceptor", _DummyLogInterceptor)
    monkeypatch.setattr(
        "deeptutor.api.routers.solve.get_llm_config",
        lambda: SimpleNamespace(api_key="k", base_url="u", api_version="v1"),
    )
    monkeypatch.setattr(
        "deeptutor.api.routers.solve.get_path_service",
        lambda: SimpleNamespace(get_solve_dir=lambda: Path(tmp_path)),
    )
    monkeypatch.setattr("deeptutor.api.routers.solve.get_ui_language", lambda default="en": default)
    monkeypatch.setattr("deeptutor.api.routers.solve.get_current_user_from_websocket", lambda _ws: _teacher_user())

    app = _build_app(solve_module)

    with TestClient(app) as client:
        with client.websocket_connect("/api/v1/solve") as websocket:
            websocket.send_json(
                {
                    "question": "Solve x^2=4",
                    "tools": [],
                    "kb_name": "algebra",
                }
            )
            messages = [websocket.receive_json() for _ in range(4)]

    assert [message["type"] for message in messages] == ["session", "task_id", "status", "result"]
    assert captured["init"]["enabled_tools"] == []
    assert captured["init"]["kb_name"] is None
    assert captured["init"]["disable_planner_retrieve"] is True


def test_solve_router_requires_authenticated_cookie(monkeypatch, tmp_path) -> None:
    solve_module = _import_solve_module(monkeypatch, tmp_path)
    monkeypatch.setattr(
        solve_module,
        "get_current_user_from_websocket",
        lambda _ws: (_ for _ in ()).throw(HTTPException(status_code=401, detail="Authentication required")),
    )

    with TestClient(_build_app(solve_module)) as client:
        with pytest.raises(Exception):
            with client.websocket_connect("/api/v1/solve"):
                pass


def test_solve_rest_routes_are_owner_scoped(monkeypatch, tmp_path) -> None:
    solve_module = _import_solve_module(monkeypatch, tmp_path)
    class FakeManager:
        def list_sessions(self, limit=20, include_messages=False, owner_user_id=None):
            assert limit == 5
            assert include_messages is False
            assert owner_user_id == "teacher-1"
            return [{"session_id": "solve_1", "title": "Owned solve"}]

        def get_session(self, session_id: str, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            if session_id == "missing":
                return None
            return {"session_id": session_id, "title": "Owned solve", "messages": []}

        def delete_session(self, session_id: str, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return session_id == "solve_1"

    monkeypatch.setattr(solve_module, "solver_session_manager", FakeManager())

    app = _build_app(solve_module)
    app.dependency_overrides[solve_module.get_current_user] = _teacher_user

    with TestClient(app) as client:
        list_response = client.get("/api/v1/solve/sessions", params={"limit": 5})
        get_response = client.get("/api/v1/solve/sessions/solve_1")
        missing_response = client.get("/api/v1/solve/sessions/missing")
        delete_response = client.delete("/api/v1/solve/sessions/solve_1")

    assert list_response.status_code == 200
    assert list_response.json()[0]["session_id"] == "solve_1"
    assert get_response.status_code == 200
    assert missing_response.status_code == 404
    assert delete_response.status_code == 200
