from __future__ import annotations

import base64
import importlib
from pathlib import Path
import sys
import types

import pytest
from fastapi import HTTPException
from starlette.websockets import WebSocketDisconnect

from deeptutor.services.auth.schemas import AuthenticatedUser

FastAPI = pytest.importorskip("fastapi").FastAPI
TestClient = pytest.importorskip("fastapi.testclient").TestClient


@pytest.fixture(autouse=True)
def _cleanup_question_router_module():
    yield
    sys.modules.pop("deeptutor.api.routers.question", None)


class _DummyLogger:
    def addHandler(self, *_args, **_kwargs) -> None:
        pass

    def debug(self, *_args, **_kwargs) -> None:
        pass

    def error(self, *_args, **_kwargs) -> None:
        pass

    def exception(self, *_args, **_kwargs) -> None:
        pass

    def info(self, *_args, **_kwargs) -> None:
        pass

    def success(self, *_args, **_kwargs) -> None:
        pass

    def warning(self, *_args, **_kwargs) -> None:
        pass

    def removeHandler(self, *_args, **_kwargs) -> None:
        pass


class _DummyLogInterceptor:
    def __init__(self, *_args, **_kwargs) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> None:
        return None


def _package(name: str) -> types.ModuleType:
    module = types.ModuleType(name)
    module.__path__ = []
    return module


def _load_question_router_module(monkeypatch: pytest.MonkeyPatch):
    sys.modules.pop("deeptutor.api.routers.question", None)

    fake_agents = _package("deeptutor.agents")
    fake_agents_question = types.ModuleType("deeptutor.agents.question")
    fake_agents_question.AgentCoordinator = object
    fake_agents.question = fake_agents_question
    monkeypatch.setitem(sys.modules, "deeptutor.agents", fake_agents)
    monkeypatch.setitem(sys.modules, "deeptutor.agents.question", fake_agents_question)

    fake_logging = _package("deeptutor.logging")
    fake_logging.get_logger = lambda *_args, **_kwargs: _DummyLogger()
    fake_logging_handlers = types.ModuleType("deeptutor.logging.handlers")
    fake_logging_handlers.JSONFileHandler = object
    fake_logging_handlers.LogInterceptor = _DummyLogInterceptor
    fake_logging_handlers.WebSocketLogHandler = object
    fake_logging_handlers.create_task_logger = lambda *_args, **_kwargs: None
    fake_logging.handlers = fake_logging_handlers
    monkeypatch.setitem(sys.modules, "deeptutor.logging", fake_logging)
    monkeypatch.setitem(sys.modules, "deeptutor.logging.handlers", fake_logging_handlers)

    fake_config = types.ModuleType("deeptutor.services.config")
    fake_config.PROJECT_ROOT = Path.cwd()
    fake_config.load_config_with_main = lambda *_args, **_kwargs: {}
    monkeypatch.setitem(sys.modules, "deeptutor.services.config", fake_config)

    fake_llm_package = _package("deeptutor.services.llm")
    fake_llm_config = types.ModuleType("deeptutor.services.llm.config")
    fake_llm_config.get_llm_config = lambda: None
    fake_llm_package.config = fake_llm_config
    monkeypatch.setitem(sys.modules, "deeptutor.services.llm", fake_llm_package)
    monkeypatch.setitem(sys.modules, "deeptutor.services.llm.config", fake_llm_config)

    fake_settings_package = _package("deeptutor.services.settings")
    fake_interface_settings = types.ModuleType("deeptutor.services.settings.interface_settings")
    fake_interface_settings.get_ui_language = lambda default="en": default
    fake_settings_package.interface_settings = fake_interface_settings
    monkeypatch.setitem(sys.modules, "deeptutor.services.settings", fake_settings_package)
    monkeypatch.setitem(
        sys.modules,
        "deeptutor.services.settings.interface_settings",
        fake_interface_settings,
    )

    fake_auth_package = _package("deeptutor.services.auth")
    fake_auth_deps = types.ModuleType("deeptutor.services.auth.deps")
    fake_auth_schemas = types.ModuleType("deeptutor.services.auth.schemas")
    fake_auth_schemas.AuthenticatedUser = AuthenticatedUser
    fake_auth_deps.get_current_user_from_websocket = lambda _ws: AuthenticatedUser(
        id="teacher-1",
        email="teacher-1@example.com",
        display_name="Teacher One",
        role="teacher",
    )
    fake_auth_package.deps = fake_auth_deps
    fake_auth_package.schemas = fake_auth_schemas
    monkeypatch.setitem(sys.modules, "deeptutor.services.auth", fake_auth_package)
    monkeypatch.setitem(sys.modules, "deeptutor.services.auth.deps", fake_auth_deps)
    monkeypatch.setitem(sys.modules, "deeptutor.services.auth.schemas", fake_auth_schemas)

    fake_tools = _package("deeptutor.tools")
    fake_tools_question = types.ModuleType("deeptutor.tools.question")

    async def _default_mimic_exam_questions(*_args, **_kwargs):
        return {"success": True}

    fake_tools_question.mimic_exam_questions = _default_mimic_exam_questions
    fake_tools.question = fake_tools_question
    monkeypatch.setitem(sys.modules, "deeptutor.tools", fake_tools)
    monkeypatch.setitem(sys.modules, "deeptutor.tools.question", fake_tools_question)

    return importlib.import_module("deeptutor.api.routers.question")


def _build_app(router_module) -> FastAPI:
    app = FastAPI()
    app.include_router(router_module.router, prefix="/api/v1/question")
    return app


def test_mimic_websocket_accepts_config_and_returns_messages(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    question_router_module = _load_question_router_module(monkeypatch)

    async def _fake_mimic_exam_questions(*_args, **_kwargs):
        return {"success": False, "error": "stub mimic failure"}

    monkeypatch.setattr(question_router_module, "mimic_exam_questions", _fake_mimic_exam_questions)
    monkeypatch.setattr(question_router_module, "MIMIC_OUTPUT_DIR", tmp_path / "mimic_papers")

    with TestClient(_build_app(question_router_module)) as client:
        with client.websocket_connect("/api/v1/question/mimic") as websocket:
            websocket.send_json(
                {
                    "mode": "parsed",
                    "paper_path": str(tmp_path / "paper"),
                    "kb_name": "demo-kb",
                    "subject": "Physics",
                    "max_questions": 3,
                }
            )
            messages = [websocket.receive_json() for _ in range(3)]

    assert [message["type"] for message in messages] == ["status", "status", "error"]
    assert messages[0]["stage"] == "init"
    assert messages[1]["stage"] == "processing"
    assert messages[2]["content"] == "stub mimic failure"


def test_mimic_websocket_rejects_blank_parsed_paper_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    question_router_module = _load_question_router_module(monkeypatch)
    monkeypatch.setattr(question_router_module, "MIMIC_OUTPUT_DIR", tmp_path / "mimic_papers")

    with TestClient(_build_app(question_router_module)) as client:
        with client.websocket_connect("/api/v1/question/mimic") as websocket:
            websocket.send_json(
                {
                    "mode": "parsed",
                    "paper_path": "   ",
                    "kb_name": "demo-kb",
                }
            )
            messages = [websocket.receive_json() for _ in range(2)]

    assert messages[0]["type"] == "status"
    assert messages[1] == {"type": "error", "content": "paper_path is required for parsed mode"}


def test_mimic_websocket_rejects_unknown_mode(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    question_router_module = _load_question_router_module(monkeypatch)
    monkeypatch.setattr(question_router_module, "MIMIC_OUTPUT_DIR", tmp_path / "mimic_papers")

    with TestClient(_build_app(question_router_module)) as client:
        with client.websocket_connect("/api/v1/question/mimic") as websocket:
            websocket.send_json({"mode": "mystery", "kb_name": "demo-kb"})
            messages = [websocket.receive_json() for _ in range(2)]

    assert messages[0]["type"] == "status"
    assert messages[1] == {"type": "error", "content": "Unknown mode: mystery"}


def test_mimic_websocket_rejects_invalid_base64_pdf(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    question_router_module = _load_question_router_module(monkeypatch)
    monkeypatch.setattr(question_router_module, "MIMIC_OUTPUT_DIR", tmp_path / "mimic_papers")

    with TestClient(_build_app(question_router_module)) as client:
        with client.websocket_connect("/api/v1/question/mimic") as websocket:
            websocket.send_json(
                {
                    "mode": "upload",
                    "pdf_data": "%%%not-base64%%%",
                    "pdf_name": "exam.pdf",
                    "kb_name": "demo-kb",
                }
            )
            messages = [websocket.receive_json() for _ in range(2)]

    assert messages[0]["type"] == "status"
    assert messages[1]["type"] == "error"
    assert "Invalid base64 PDF data" in messages[1]["content"]


def test_generate_websocket_requires_requirement(monkeypatch: pytest.MonkeyPatch) -> None:
    question_router_module = _load_question_router_module(monkeypatch)

    with TestClient(_build_app(question_router_module)) as client:
        with client.websocket_connect("/api/v1/question/generate") as websocket:
            websocket.send_json({"kb_name": "demo-kb"})
            payload = websocket.receive_json()

    assert payload == {"type": "error", "content": "Requirement is required"}


def test_question_websockets_require_authenticated_cookie(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    question_router_module = _load_question_router_module(monkeypatch)
    monkeypatch.setattr(
        question_router_module,
        "get_current_user_from_websocket",
        lambda _ws: (_ for _ in ()).throw(HTTPException(status_code=401, detail="Authentication required")),
    )

    with TestClient(_build_app(question_router_module)) as client:
        with pytest.raises(Exception):
            with client.websocket_connect("/api/v1/question/generate"):
                pass


def test_generate_websocket_streams_task_and_completion(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    question_router_module = _load_question_router_module(monkeypatch)
    sent: dict[str, object] = {}

    class _FakeCoordinator:
        def __init__(self, **kwargs) -> None:
            sent["coordinator_kwargs"] = kwargs
            self.logger = types.SimpleNamespace(logger=_DummyLogger())
            self._callback = None

        def set_ws_callback(self, callback) -> None:
            self._callback = callback

        async def generate_from_topic(
            self,
            *,
            user_topic: str,
            preference: str,
            num_questions: int,
            difficulty: str,
            question_type: str,
        ) -> dict:
            sent["generate_args"] = {
                "user_topic": user_topic,
                "preference": preference,
                "num_questions": num_questions,
                "difficulty": difficulty,
                "question_type": question_type,
            }
            await self._callback({"type": "log", "content": "working"})
            return {"success": True, "completed": 2, "failed": 0}

    class _FakeTaskManager:
        def generate_task_id(self, prefix: str, task_key: str) -> str:
            sent["task_key"] = (prefix, task_key)
            return "task-123"

        def update_task_status(self, task_id: str, status: str, error: str | None = None) -> None:
            sent["task_status"] = (task_id, status, error)

    monkeypatch.setattr(question_router_module, "AgentCoordinator", _FakeCoordinator)
    monkeypatch.setattr(
        question_router_module.TaskIDManager,
        "get_instance",
        lambda: _FakeTaskManager(),
    )
    monkeypatch.setattr(
        question_router_module,
        "get_ui_language",
        lambda default="en": "vi",
    )
    monkeypatch.setattr(
        question_router_module,
        "get_llm_config",
        lambda: types.SimpleNamespace(api_key="k", base_url="u", api_version="v1"),
    )
    monkeypatch.setattr(
        question_router_module,
        "get_path_service",
        lambda: types.SimpleNamespace(get_question_batch_dir=lambda task_id: tmp_path / task_id),
    )

    with TestClient(_build_app(question_router_module)) as client:
        with client.websocket_connect("/api/v1/question/generate") as websocket:
            websocket.send_json(
                {
                    "requirement": {
                        "knowledge_point": "Quadratic equations",
                        "subject": "Physics",
                        "preference": "Use real-world examples",
                        "difficulty": "medium",
                        "question_type": "choice",
                    },
                    "kb_name": "demo-kb",
                    "count": 2,
                }
            )
            messages = []
            while True:
                try:
                    messages.append(websocket.receive_json())
                except WebSocketDisconnect:
                    break

    message_types = [message["type"] for message in messages]
    assert message_types[0:2] == ["task_id", "status"]
    assert "log" in message_types
    assert "batch_summary" in message_types
    assert "complete" in message_types
    assert sent["generate_args"] == {
        "user_topic": "Quadratic equations",
        "preference": "Subject: Physics\nUse real-world examples",
        "num_questions": 2,
        "difficulty": "medium",
        "question_type": "choice",
    }
    assert sent["task_status"] == ("task-123", "completed", None)
    assert sent["coordinator_kwargs"]["language"] == "vi"


def test_mimic_websocket_upload_mode_completes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    question_router_module = _load_question_router_module(monkeypatch)
    monkeypatch.setattr(question_router_module, "MIMIC_OUTPUT_DIR", tmp_path / "mimic_papers")
    monkeypatch.setattr(
        question_router_module.DocumentValidator,
        "validate_upload_safety",
        lambda filename, *_args, **_kwargs: filename,
    )
    monkeypatch.setattr(
        question_router_module.DocumentValidator,
        "validate_file",
        lambda *_args, **_kwargs: None,
    )

    async def _fake_mimic_exam_questions(*_args, **kwargs):
        await kwargs["ws_callback"]("progress", {"content": "parsed"})
        return {
            "success": True,
            "total_reference_questions": 2,
            "generated_questions": [{"id": "q1"}],
            "failed_questions": [],
        }

    monkeypatch.setattr(question_router_module, "mimic_exam_questions", _fake_mimic_exam_questions)

    pdf_bytes = base64.b64encode(b"%PDF-1.4 demo").decode("ascii")

    with TestClient(_build_app(question_router_module)) as client:
        with client.websocket_connect("/api/v1/question/mimic") as websocket:
            websocket.send_json(
                {
                    "mode": "upload",
                    "pdf_data": pdf_bytes,
                    "pdf_name": "exam.pdf",
                    "kb_name": "demo-kb",
                    "max_questions": 2,
                }
            )
            messages = []
            while True:
                try:
                    messages.append(websocket.receive_json())
                except WebSocketDisconnect:
                    break

    message_types = [message["type"] for message in messages]
    assert message_types[0:4] == ["status", "status", "status", "status"]
    assert "progress" in message_types
    assert message_types[-1] == "complete"


def test_generate_websocket_reports_generation_error(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    question_router_module = _load_question_router_module(monkeypatch)
    sent: dict[str, object] = {}

    class _FailingCoordinator:
        def __init__(self, **_kwargs) -> None:
            self.logger = types.SimpleNamespace(logger=_DummyLogger())

        def set_ws_callback(self, _callback) -> None:
            return None

        async def generate_from_topic(self, **_kwargs) -> dict:
            raise RuntimeError("generation exploded")

    class _FakeTaskManager:
        def generate_task_id(self, *_args, **_kwargs) -> str:
            return "task-err"

        def update_task_status(self, task_id: str, status: str, error: str | None = None) -> None:
            sent["task_status"] = (task_id, status, error)

    monkeypatch.setattr(question_router_module, "AgentCoordinator", _FailingCoordinator)
    monkeypatch.setattr(
        question_router_module.TaskIDManager,
        "get_instance",
        lambda: _FakeTaskManager(),
    )
    monkeypatch.setattr(
        question_router_module,
        "get_path_service",
        lambda: types.SimpleNamespace(get_question_batch_dir=lambda task_id: tmp_path / task_id),
    )

    with TestClient(_build_app(question_router_module)) as client:
        with client.websocket_connect("/api/v1/question/generate") as websocket:
            websocket.send_json(
                {
                    "requirement": {"knowledge_point": "Quadratic equations"},
                    "kb_name": "demo-kb",
                }
            )
            messages = []
            while True:
                try:
                    messages.append(websocket.receive_json())
                except WebSocketDisconnect:
                    break

    assert messages[0]["type"] == "task_id"
    assert messages[1] == {"type": "status", "content": "started"}
    assert messages[2] == {"type": "error", "content": "generation exploded"}
    assert sent["task_status"] == ("task-err", "error", "generation exploded")
