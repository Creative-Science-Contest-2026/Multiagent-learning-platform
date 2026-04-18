from __future__ import annotations

import importlib
from pathlib import Path
import sys

import pytest

try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
except Exception:  # pragma: no cover - optional dependency in lightweight envs
    FastAPI = None
    TestClient = None

pytestmark = pytest.mark.skipif(FastAPI is None or TestClient is None, reason="fastapi not installed")

knowledge_router_module = None
router = None


def _import_knowledge_router(monkeypatch, tmp_path: Path):
    if FastAPI is None or TestClient is None:  # pragma: no cover - guarded by pytestmark
        raise RuntimeError("fastapi is not installed")

    config_module = importlib.import_module("deeptutor.services.config")
    fake_settings_dir = tmp_path / "data" / "user" / "settings"
    fake_settings_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(config_module, "PROJECT_ROOT", tmp_path)
    monkeypatch.setattr(
        config_module,
        "load_config_with_main",
        lambda *_args, **_kwargs: {"paths": {"user_log_dir": str(tmp_path / "logs")}},
    )

    sys.modules.pop("deeptutor.api.routers.knowledge", None)
    module = importlib.import_module("deeptutor.api.routers.knowledge")
    return module


def _build_app(knowledge_module) -> FastAPI:
    if FastAPI is None or knowledge_module is None:  # pragma: no cover - guarded by pytestmark
        raise RuntimeError("fastapi is not installed")
    app = FastAPI()
    app.include_router(knowledge_module.router, prefix="/api/v1/knowledge")
    return app


class _FakeKBManager:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.base_dir / "kb_config.json"
        self.config: dict[str, dict] = {"knowledge_bases": {}}

    def _load_config(self) -> dict:
        return self.config

    def _save_config(self) -> None:
        pass

    def list_knowledge_bases(self) -> list[str]:
        return sorted(self.config.get("knowledge_bases", {}).keys())

    def update_kb_status(self, name: str, status: str, progress: dict | None = None) -> None:
        entry = self.config.setdefault("knowledge_bases", {}).setdefault(name, {"path": name})
        entry["status"] = status
        entry["progress"] = progress or {}

    def get_knowledge_base_path(self, name: str) -> Path:
        kb_dir = self.base_dir / name
        kb_dir.mkdir(parents=True, exist_ok=True)
        return kb_dir


class _FakeInitializer:
    def __init__(self, kb_name: str, base_dir: str, **_kwargs) -> None:
        self.kb_name = kb_name
        self.base_dir = base_dir
        self.kb_dir = Path(base_dir) / kb_name
        self.raw_dir = self.kb_dir / "raw"
        self.progress_tracker = _kwargs.get("progress_tracker")

    def create_directory_structure(self) -> None:
        self.raw_dir.mkdir(parents=True, exist_ok=True)

    def _register_to_config(self) -> None:
        pass


def _upload_payload() -> list[tuple[str, tuple[str, bytes, str]]]:
    return [("files", ("demo.txt", b"hello", "text/plain"))]


def test_rag_providers_returns_llamaindex_only() -> None:
    with pytest.MonkeyPatch.context() as monkeypatch:
        knowledge_module = _import_knowledge_router(monkeypatch, Path.cwd())

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.get("/api/v1/knowledge/rag-providers")

    assert response.status_code == 200
    payload = response.json()
    assert payload == {
        "providers": [
            {
                "id": "llamaindex",
                "name": "LlamaIndex",
                "description": "Pure vector retrieval, fastest processing speed.",
            }
        ]
    }


def test_create_kb_does_not_require_llm_precheck(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)
    manager = _FakeKBManager(tmp_path / "knowledge_bases")
    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)
    monkeypatch.setattr(knowledge_module, "KnowledgeBaseInitializer", _FakeInitializer)
    monkeypatch.setattr(knowledge_module, "get_llm_config", lambda: (_ for _ in ()).throw(RuntimeError("should not be called")), raising=False)

    async def _noop_init_task(*_args, **_kwargs):
        return None

    monkeypatch.setattr(knowledge_module, "run_initialization_task", _noop_init_task)
    monkeypatch.setattr(knowledge_module, "_kb_base_dir", tmp_path / "knowledge_bases")

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.post(
            "/api/v1/knowledge/create",
            data={"name": "kb-new", "rag_provider": "llamaindex"},
            files=_upload_payload(),
        )

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "kb-new"
    assert isinstance(body.get("task_id"), str) and body["task_id"]
    assert manager.config["knowledge_bases"]["kb-new"]["rag_provider"] == "llamaindex"
    assert manager.config["knowledge_bases"]["kb-new"]["needs_reindex"] is False


def test_create_rejects_unregistered_provider(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)
    manager = _FakeKBManager(tmp_path / "knowledge_bases")
    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)
    monkeypatch.setattr(knowledge_module, "_kb_base_dir", tmp_path / "knowledge_bases")

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.post(
            "/api/v1/knowledge/create",
            data={"name": "kb-invalid", "rag_provider": "lightrag"},
            files=_upload_payload(),
        )

    assert response.status_code == 400
    assert "Unsupported RAG provider" in response.json()["detail"]


def test_upload_returns_409_when_kb_needs_reindex(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)
    manager = _FakeKBManager(tmp_path / "knowledge_bases")
    manager.config["knowledge_bases"]["legacy-kb"] = {
        "path": "legacy-kb",
        "rag_provider": "llamaindex",
        "needs_reindex": True,
        "status": "needs_reindex",
    }
    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.post("/api/v1/knowledge/legacy-kb/upload", files=_upload_payload())

    assert response.status_code == 409
    assert "needs reindex" in response.json()["detail"].lower()


def test_upload_ready_kb_returns_task_id(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)
    manager = _FakeKBManager(tmp_path / "knowledge_bases")
    manager.config["knowledge_bases"]["ready-kb"] = {
        "path": "ready-kb",
        "rag_provider": "llamaindex",
        "needs_reindex": False,
        "status": "ready",
    }
    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)
    monkeypatch.setattr(knowledge_module, "_kb_base_dir", tmp_path / "knowledge_bases")

    async def _noop_upload_task(*_args, **_kwargs):
        return None

    monkeypatch.setattr(knowledge_module, "run_upload_processing_task", _noop_upload_task)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.post("/api/v1/knowledge/ready-kb/upload", files=_upload_payload())

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body.get("task_id"), str) and body["task_id"]


def test_update_config_rejects_unregistered_provider() -> None:
    class _FakeConfigService:
        def set_kb_config(self, kb_name: str, config: dict) -> None:
            self.kb_name = kb_name
            self.config = config

        def get_kb_config(self, _kb_name: str) -> dict:
            return {"rag_provider": "llamaindex"}

    fake_service = _FakeConfigService()

    config_module = importlib.import_module("deeptutor.services.config")
    with pytest.MonkeyPatch.context() as monkeypatch:
        knowledge_module = _import_knowledge_router(monkeypatch, Path.cwd())
        monkeypatch.setattr(config_module, "get_kb_config_service", lambda: fake_service)
        with TestClient(_build_app(knowledge_module)) as client:
            response = client.put(
                "/api/v1/knowledge/demo/config",
                json={"rag_provider": "raganything"},
            )

    assert response.status_code == 400
    assert "Unsupported RAG provider" in response.json()["detail"]


def test_update_config_persists_teacher_pack_metadata(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)

    class _FakeConfigService:
        def __init__(self) -> None:
            self.store = {
                "demo": {
                    "rag_provider": "llamaindex",
                    "subject": "Old",
                }
            }

        def set_kb_config(self, kb_name: str, config: dict) -> None:
            current = self.store.get(kb_name, {})
            current.update(config)
            self.store[kb_name] = current

        def get_kb_config(self, kb_name: str) -> dict:
            return self.store.get(kb_name, {})

    fake_service = _FakeConfigService()
    config_module = importlib.import_module("deeptutor.services.config")

    payload = {
        "subject": "Math",
        "grade": "10",
        "curriculum": "Vietnam National Curriculum",
        "learning_objectives": ["Quadratic equations", "Graph reading"],
        "owner": "teacher-a",
        "sharing_status": "private",
    }

    monkeypatch.setattr(config_module, "get_kb_config_service", lambda: fake_service)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.put("/api/v1/knowledge/demo/config", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["config"]["subject"] == "Math"
    assert body["config"]["grade"] == "10"
    assert body["config"]["curriculum"] == "Vietnam National Curriculum"
    assert body["config"]["learning_objectives"] == ["Quadratic equations", "Graph reading"]
    assert body["config"]["owner"] == "teacher-a"
    assert body["config"]["sharing_status"] == "private"


def test_get_knowledge_base_details_exposes_teacher_pack_metadata(
    monkeypatch, tmp_path: Path
) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)

    kb_root = tmp_path / "knowledge_bases"
    kb_dir = kb_root / "demo"
    (kb_dir / "llamaindex_storage").mkdir(parents=True, exist_ok=True)

    manager_module = importlib.import_module("deeptutor.knowledge.manager")
    manager = manager_module.KnowledgeBaseManager(base_dir=str(kb_root))
    manager.config = {
        "knowledge_bases": {
            "demo": {
                "path": "demo",
                "description": "Knowledge base: demo",
                "rag_provider": "llamaindex",
                "subject": "Math",
                "grade": "10",
                "curriculum": "Vietnam National Curriculum",
                "learning_objectives": ["Quadratic equations", "Graph reading"],
                "owner": "teacher-a",
                "sharing_status": "private",
                "status": "ready",
            }
        }
    }
    manager._save_config()

    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.get("/api/v1/knowledge/demo")

    assert response.status_code == 200
    metadata = response.json()["metadata"]
    assert metadata["subject"] == "Math"
    assert metadata["grade"] == "10"
    assert metadata["curriculum"] == "Vietnam National Curriculum"
    assert metadata["learning_objectives"] == ["Quadratic equations", "Graph reading"]
    assert metadata["owner"] == "teacher-a"
    assert metadata["sharing_status"] == "private"


def test_list_knowledge_bases_includes_teacher_pack_metadata(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)

    class _MetadataAwareManager(_FakeKBManager):
        def get_default(self) -> str | None:
            return "demo"

        def get_info(self, name: str) -> dict:
            return {
                "name": name,
                "is_default": True,
                "statistics": {"raw_documents": 1},
                "status": "ready",
                "progress": None,
                "metadata": {
                    "subject": "Math",
                    "grade": "10",
                    "curriculum": "Vietnam National Curriculum",
                    "learning_objectives": ["Quadratic equations"],
                    "owner": "teacher-a",
                    "sharing_status": "private",
                },
            }

    manager = _MetadataAwareManager(tmp_path / "knowledge_bases")
    manager.config["knowledge_bases"]["demo"] = {"path": "demo"}
    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.get("/api/v1/knowledge/list")

    assert response.status_code == 200
    payload = response.json()
    assert payload[0]["metadata"]["subject"] == "Math"
    assert payload[0]["metadata"]["grade"] == "10"
    assert payload[0]["metadata"]["owner"] == "teacher-a"


def test_update_config_rejects_invalid_sharing_status(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)

    class _FakeConfigService:
        def __init__(self) -> None:
            self.store = {"demo": {"rag_provider": "llamaindex"}}

        def set_kb_config(self, kb_name: str, config: dict) -> None:
            current = self.store.get(kb_name, {})
            current.update(config)
            self.store[kb_name] = current

        def get_kb_config(self, kb_name: str) -> dict:
            return self.store.get(kb_name, {})

    fake_service = _FakeConfigService()
    config_module = importlib.import_module("deeptutor.services.config")
    monkeypatch.setattr(config_module, "get_kb_config_service", lambda: fake_service)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.put(
            "/api/v1/knowledge/demo/config",
            json={"sharing_status": "school"},
        )

    assert response.status_code == 400
    assert "sharing_status" in response.json()["detail"]


def test_update_config_normalizes_learning_objectives(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)

    class _FakeConfigService:
        def __init__(self) -> None:
            self.store = {"demo": {"rag_provider": "llamaindex"}}

        def set_kb_config(self, kb_name: str, config: dict) -> None:
            current = self.store.get(kb_name, {})
            current.update(config)
            self.store[kb_name] = current

        def get_kb_config(self, kb_name: str) -> dict:
            return self.store.get(kb_name, {})

    fake_service = _FakeConfigService()
    config_module = importlib.import_module("deeptutor.services.config")
    monkeypatch.setattr(config_module, "get_kb_config_service", lambda: fake_service)

    payload = {
        "learning_objectives": ["  Quadratic equations  ", "", "  ", "Graph reading"],
        "owner": " teacher-a ",
    }

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.put("/api/v1/knowledge/demo/config", json=payload)

    assert response.status_code == 200
    config = response.json()["config"]
    assert config["learning_objectives"] == ["Quadratic equations", "Graph reading"]
    assert config["owner"] == "teacher-a"
