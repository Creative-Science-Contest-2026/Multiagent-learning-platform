from __future__ import annotations

from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from deeptutor.core.stream import StreamEvent, StreamEventType
from deeptutor.services.agent_spec.service import AgentSpecService
from deeptutor.services.auth.schemas import AuthenticatedUser
from deeptutor.services.session.sqlite_store import SQLiteSessionStore
from deeptutor.services.session.turn_runtime import TurnRuntimeManager
from deeptutor.services.runtime_policy import compiler as runtime_policy_compiler

FastAPI = pytest.importorskip("fastapi").FastAPI
TestClient = pytest.importorskip("fastapi.testclient").TestClient


async def _noop_refresh(**_kwargs):
    return None


def _teacher_user(user_id: str = "teacher-1", role: str = "teacher") -> AuthenticatedUser:
    return AuthenticatedUser(
        id=user_id,
        email=f"{user_id}@example.com",
        display_name=f"Teacher {user_id}",
        role=role,  # type: ignore[arg-type]
    )


@pytest.fixture(autouse=True)
def _authenticated_unified_ws(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "deeptutor.api.routers.unified_ws.get_current_user_from_websocket",
        lambda _ws: _teacher_user(),
    )


@pytest.mark.asyncio
async def test_turn_runtime_replays_events_and_materializes_messages(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    runtime = TurnRuntimeManager(store)

    class FakeContextBuilder:
        def __init__(self, *_args, **_kwargs) -> None:
            pass

        async def build(self, **kwargs):
            on_event = kwargs.get("on_event")
            if on_event is not None:
                await on_event(
                    StreamEvent(
                        type=StreamEventType.PROGRESS,
                        source="context",
                        stage="summarizing",
                        content="summarize context",
                    )
                )
            return SimpleNamespace(
                conversation_history=[],
                conversation_summary="",
                context_text="",
                token_count=0,
                budget=0,
            )

    class FakeOrchestrator:
        async def handle(self, _context):
            yield StreamEvent(
                type=StreamEventType.CONTENT,
                source="chat",
                stage="responding",
                content="Hello Frank",
                metadata={"call_kind": "llm_final_response"},
            )
            yield StreamEvent(type=StreamEventType.DONE, source="chat")

    monkeypatch.setattr(
        "deeptutor.services.llm.config.get_llm_config",
        lambda: SimpleNamespace(api_key="k", base_url="u", api_version="v1"),
    )
    monkeypatch.setattr("deeptutor.services.session.context_builder.ContextBuilder", FakeContextBuilder)
    monkeypatch.setattr("deeptutor.runtime.orchestrator.ChatOrchestrator", FakeOrchestrator)
    monkeypatch.setattr(
        "deeptutor.services.memory.get_memory_service",
        lambda: SimpleNamespace(
            build_memory_context=lambda owner_user_id=None: "",
            refresh_from_turn=_noop_refresh,
        ),
    )

    session, turn = await runtime.start_turn(
        {
            "type": "start_turn",
            "content": "hello, i'm frank",
            "session_id": None,
            "capability": None,
            "tools": [],
            "knowledge_bases": [],
            "attachments": [],
            "language": "en",
            "config": {},
        }
    )

    events = []
    async for event in runtime.subscribe_turn(turn["id"], after_seq=0):
        events.append(event)

    assert [event["type"] for event in events] == ["session", "progress", "content", "done"]
    assert events[-1]["metadata"]["status"] == "completed"

    detail = await store.get_session_with_messages(session["id"])
    assert detail is not None
    assert [message["role"] for message in detail["messages"]] == ["user", "assistant"]
    assert detail["messages"][1]["content"] == "Hello Frank"
    assert detail["preferences"] == {
        "capability": "chat",
        "tools": [],
        "knowledge_bases": [],
        "language": "en",
    }
    persisted_turn = await store.get_turn(turn["id"])
    assert persisted_turn is not None
    assert persisted_turn["status"] == "completed"


@pytest.mark.asyncio
async def test_turn_runtime_persists_tutoring_signals_under_session_owner(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    runtime = TurnRuntimeManager(store)

    class FakeContextBuilder:
        def __init__(self, *_args, **_kwargs) -> None:
            pass

        async def build(self, **_kwargs):
            return SimpleNamespace(
                conversation_history=[],
                conversation_summary="",
                context_text="",
                token_count=0,
                budget=0,
            )

    class FakeOrchestrator:
        async def handle(self, _context):
            yield StreamEvent(
                type=StreamEventType.CONTENT,
                source="chat",
                stage="responding",
                content="Try decomposing the fraction step by step.",
                metadata={"call_kind": "llm_final_response"},
            )
            yield StreamEvent(type=StreamEventType.DONE, source="chat")

    monkeypatch.setattr(
        "deeptutor.services.llm.config.get_llm_config",
        lambda: SimpleNamespace(api_key="k", base_url="u", api_version="v1"),
    )
    monkeypatch.setattr("deeptutor.services.session.context_builder.ContextBuilder", FakeContextBuilder)
    monkeypatch.setattr("deeptutor.runtime.orchestrator.ChatOrchestrator", FakeOrchestrator)
    monkeypatch.setattr(
        "deeptutor.services.evidence.extractor.extract_observations_from_tutoring_turn",
        lambda **kwargs: [
            {
                "observation_id": "owned-obs-1",
                "session_id": kwargs["session_id"],
                "student_id": kwargs["student_id"],
                "source": "tutoring",
                "topic": "fractions subtraction",
                "question_id": "followup-1",
                "is_correct": False,
                "latency_seconds": 24,
                "hint_count": 1,
                "retry_count": 1,
                "dominant_error": "needs_scaffold",
            }
        ],
    )
    monkeypatch.setattr(
        "deeptutor.services.memory.get_memory_service",
        lambda: SimpleNamespace(
            build_memory_context=lambda owner_user_id=None: "",
            refresh_from_turn=_noop_refresh,
        ),
    )

    await store.create_session(session_id="owned-chat", owner_user_id="teacher-1")
    await store.update_session_preferences(
        "owned-chat",
        {
            "student_id": "student-owned",
            "capability": "chat",
            "tools": [],
            "knowledge_bases": [],
            "language": "en",
        },
    )

    _session, turn = await runtime.start_turn(
        {
            "type": "start_turn",
            "content": "Help me with this fraction problem",
            "session_id": "owned-chat",
            "capability": "chat",
            "tools": [],
            "knowledge_bases": [],
            "attachments": [],
            "language": "en",
            "config": {},
        }
    )

    async for _event in runtime.subscribe_turn(turn["id"], after_seq=0):
        pass

    owned_observations = await store.list_observations("student-owned", owner_user_id="teacher-1")
    anonymous_observations = await store.list_observations("student-owned", owner_user_id="")
    owned_state = await store.get_student_state("student-owned", owner_user_id="teacher-1")

    assert [row["topic"] for row in owned_observations] == ["fractions subtraction"]
    assert anonymous_observations == []
    assert owned_state is not None
    assert owned_state["owner_user_id"] == "teacher-1"
    assert owned_state["misconception_signals"]["dominant_errors"] == {
        "fractions subtraction": "needs_scaffold"
    }


@pytest.mark.asyncio
async def test_turn_runtime_rejects_foreign_owned_session_id(tmp_path) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    runtime = TurnRuntimeManager(store)
    await store.create_session(session_id="teacher-two-session", owner_user_id="teacher-2")

    with pytest.raises(RuntimeError, match="Session not found"):
        await runtime.start_turn(
            {
                "type": "start_turn",
                "content": "hello",
                "session_id": "teacher-two-session",
                "capability": "chat",
                "tools": [],
                "knowledge_bases": [],
                "attachments": [],
                "language": "en",
                "config": {},
            },
            owner_user_id="teacher-1",
        )


def test_unified_ws_rejects_invalid_after_seq(monkeypatch: pytest.MonkeyPatch) -> None:
    from deeptutor.api.routers import unified_ws as unified_ws_router

    class FakeRuntime:
        async def subscribe_turn(self, *_args, **_kwargs):
            if False:  # pragma: no cover
                yield {}

    app = FastAPI()
    app.include_router(unified_ws_router.router, prefix="/api/v1")
    monkeypatch.setattr(
        "deeptutor.services.session.get_turn_runtime_manager",
        lambda: FakeRuntime(),
    )

    with TestClient(app) as client:
        with client.websocket_connect("/api/v1/ws") as websocket:
            websocket.send_text('{"type":"subscribe_turn","turn_id":"turn-1","after_seq":"oops"}')
            payload = websocket.receive_json()

    assert payload == {"type": "error", "content": "Invalid after_seq."}


def test_parse_sequence_value_accepts_valid_numbers_and_rejects_invalid() -> None:
    from deeptutor.api.routers.unified_ws import _parse_sequence_value

    assert _parse_sequence_value("7", "after_seq") == 7
    assert _parse_sequence_value(None, "after_seq") == 0
    with pytest.raises(ValueError, match="Invalid after_seq."):
        _parse_sequence_value("oops", "after_seq")


def test_unified_ws_rejects_invalid_resume_seq(monkeypatch: pytest.MonkeyPatch) -> None:
    from deeptutor.api.routers import unified_ws as unified_ws_router

    class FakeRuntime:
        async def subscribe_turn(self, *_args, **_kwargs):
            if False:  # pragma: no cover
                yield {}

    app = FastAPI()
    app.include_router(unified_ws_router.router, prefix="/api/v1")
    monkeypatch.setattr(
        "deeptutor.services.session.get_turn_runtime_manager",
        lambda: FakeRuntime(),
    )

    with TestClient(app) as client:
        with client.websocket_connect("/api/v1/ws") as websocket:
            websocket.send_text('{"type":"resume_from","turn_id":"turn-1","seq":"oops"}')
            payload = websocket.receive_json()

    assert payload == {"type": "error", "content": "Invalid seq."}


def test_unified_ws_reports_invalid_json() -> None:
    from deeptutor.api.routers import unified_ws as unified_ws_router

    app = FastAPI()
    app.include_router(unified_ws_router.router, prefix="/api/v1")

    with TestClient(app) as client:
        with client.websocket_connect("/api/v1/ws") as websocket:
            websocket.send_text("{")
            payload = websocket.receive_json()

    assert payload == {"type": "error", "content": "Invalid JSON."}


def test_unified_ws_requires_authenticated_cookie(monkeypatch: pytest.MonkeyPatch) -> None:
    from deeptutor.api.routers import unified_ws as unified_ws_router

    monkeypatch.setattr(
        unified_ws_router,
        "get_current_user_from_websocket",
        lambda _ws: (_ for _ in ()).throw(HTTPException(status_code=401, detail="Authentication required")),
    )

    app = FastAPI()
    app.include_router(unified_ws_router.router, prefix="/api/v1")

    with TestClient(app) as client:
        with pytest.raises(Exception):
            with client.websocket_connect("/api/v1/ws"):
                pass


def test_unified_ws_reports_rejected_turn(monkeypatch: pytest.MonkeyPatch) -> None:
    from deeptutor.api.routers import unified_ws as unified_ws_router

    class FakeRuntime:
        async def start_turn(self, _msg, *, owner_user_id=None, actor_user_id=None):
            assert owner_user_id == "teacher-1"
            assert actor_user_id == "teacher-1"
            raise RuntimeError("turn rejected")

    app = FastAPI()
    app.include_router(unified_ws_router.router, prefix="/api/v1")
    monkeypatch.setattr(
        "deeptutor.services.session.get_turn_runtime_manager",
        lambda: FakeRuntime(),
    )

    with TestClient(app) as client:
        with client.websocket_connect("/api/v1/ws") as websocket:
            websocket.send_json({"type": "start_turn", "session_id": "session-1", "content": "hi"})
            payload = websocket.receive_json()

    assert payload["type"] == "error"
    assert payload["source"] == "unified_ws"
    assert payload["metadata"]["status"] == "rejected"
    assert payload["content"] == "turn rejected"


def test_unified_ws_reports_missing_cancel_turn_id() -> None:
    from deeptutor.api.routers import unified_ws as unified_ws_router

    app = FastAPI()
    app.include_router(unified_ws_router.router, prefix="/api/v1")

    with TestClient(app) as client:
        with client.websocket_connect("/api/v1/ws") as websocket:
            websocket.send_json({"type": "cancel_turn"})
            payload = websocket.receive_json()

    assert payload == {"type": "error", "content": "Missing turn_id."}


def test_unified_ws_reports_unknown_message_type() -> None:
    from deeptutor.api.routers import unified_ws as unified_ws_router

    app = FastAPI()
    app.include_router(unified_ws_router.router, prefix="/api/v1")

    with TestClient(app) as client:
        with client.websocket_connect("/api/v1/ws") as websocket:
            websocket.send_json({"type": "mystery"})
            payload = websocket.receive_json()

    assert payload == {"type": "error", "content": "Unknown type: mystery"}


def test_unified_ws_start_turn_forwards_stream_events(monkeypatch: pytest.MonkeyPatch) -> None:
    from deeptutor.api.routers import unified_ws as unified_ws_router

    class FakeRuntime:
        async def start_turn(self, _msg, *, owner_user_id=None, actor_user_id=None):
            assert owner_user_id == "teacher-1"
            assert actor_user_id == "teacher-1"
            return {"id": "session-1"}, {"id": "turn-1"}

        async def subscribe_turn(self, turn_id: str, after_seq: int = 0, owner_user_id=None):
            assert turn_id == "turn-1"
            assert after_seq == 0
            assert owner_user_id == "teacher-1"
            yield {"type": "session", "turn_id": "turn-1", "seq": 0}
            yield {"type": "done", "turn_id": "turn-1", "seq": 1}

    app = FastAPI()
    app.include_router(unified_ws_router.router, prefix="/api/v1")
    monkeypatch.setattr(
        "deeptutor.services.session.get_turn_runtime_manager",
        lambda: FakeRuntime(),
    )

    with TestClient(app) as client:
        with client.websocket_connect("/api/v1/ws") as websocket:
            websocket.send_json({"type": "start_turn", "content": "hello"})
            messages = [websocket.receive_json() for _ in range(2)]

    assert [message["type"] for message in messages] == ["session", "done"]


def test_unified_ws_subscribe_session_forwards_events(monkeypatch: pytest.MonkeyPatch) -> None:
    from deeptutor.api.routers import unified_ws as unified_ws_router

    class FakeRuntime:
        async def subscribe_session(self, session_id: str, after_seq: int = 0, owner_user_id=None):
            assert session_id == "session-1"
            assert after_seq == 2
            assert owner_user_id == "teacher-1"
            yield {"type": "content", "session_id": session_id, "seq": 3}

    app = FastAPI()
    app.include_router(unified_ws_router.router, prefix="/api/v1")
    monkeypatch.setattr(
        "deeptutor.services.session.get_turn_runtime_manager",
        lambda: FakeRuntime(),
    )

    with TestClient(app) as client:
        with client.websocket_connect("/api/v1/ws") as websocket:
            websocket.send_json(
                {"type": "subscribe_session", "session_id": "session-1", "after_seq": 2}
            )
            payload = websocket.receive_json()

    assert payload == {"type": "content", "session_id": "session-1", "seq": 3}


def test_unified_ws_cancel_turn_reports_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    from deeptutor.api.routers import unified_ws as unified_ws_router

    class FakeRuntime:
        async def cancel_turn(self, turn_id: str, owner_user_id=None) -> bool:
            assert turn_id == "turn-missing"
            assert owner_user_id == "teacher-1"
            return False

    app = FastAPI()
    app.include_router(unified_ws_router.router, prefix="/api/v1")
    monkeypatch.setattr(
        "deeptutor.services.session.get_turn_runtime_manager",
        lambda: FakeRuntime(),
    )

    with TestClient(app) as client:
        with client.websocket_connect("/api/v1/ws") as websocket:
            websocket.send_json({"type": "cancel_turn", "turn_id": "turn-missing"})
            payload = websocket.receive_json()

    assert payload == {"type": "error", "content": "Turn not found: turn-missing"}


@pytest.mark.asyncio
async def test_turn_runtime_passes_deep_question_subject_config(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    runtime = TurnRuntimeManager(store)
    captured: dict[str, object] = {}

    class FakeContextBuilder:
        def __init__(self, *_args, **_kwargs) -> None:
            pass

        async def build(self, **_kwargs):
            return SimpleNamespace(
                conversation_history=[],
                conversation_summary="",
                context_text="",
                token_count=0,
                budget=0,
            )

    class FakeOrchestrator:
        async def handle(self, context):
            captured["config_overrides"] = context.config_overrides
            yield StreamEvent(
                type=StreamEventType.CONTENT,
                source="deep_question",
                stage="writing",
                content="Generated quiz",
                metadata={"call_kind": "llm_final_response"},
            )
            yield StreamEvent(type=StreamEventType.DONE, source="deep_question")

    monkeypatch.setattr(
        "deeptutor.services.llm.config.get_llm_config",
        lambda: SimpleNamespace(api_key="k", base_url="u", api_version="v1"),
    )
    monkeypatch.setattr("deeptutor.services.session.context_builder.ContextBuilder", FakeContextBuilder)
    monkeypatch.setattr("deeptutor.runtime.orchestrator.ChatOrchestrator", FakeOrchestrator)
    monkeypatch.setattr(
        "deeptutor.services.memory.get_memory_service",
        lambda: SimpleNamespace(
            build_memory_context=lambda owner_user_id=None: "",
            refresh_from_turn=_noop_refresh,
        ),
    )

    _session, turn = await runtime.start_turn(
        {
            "type": "start_turn",
            "content": "make a quiz",
            "session_id": None,
            "capability": "deep_question",
            "tools": ["rag"],
            "knowledge_bases": ["math-pack"],
            "attachments": [],
            "language": "en",
            "config": {
                "mode": "custom",
                "topic": "quadratic equations",
                "subject": "Physics",
                "num_questions": 3,
                "difficulty": "medium",
                "question_type": "choice",
            },
        }
    )

    events = []
    async for event in runtime.subscribe_turn(turn["id"], after_seq=0):
        events.append(event)

    assert events[-1]["metadata"]["status"] == "completed"
    assert captured["config_overrides"]["subject"] == "Physics"
    assert captured["config_overrides"]["topic"] == "quadratic equations"


@pytest.mark.asyncio
async def test_turn_runtime_bootstraps_question_followup_context_once(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    runtime = TurnRuntimeManager(store)
    captured: dict[str, object] = {}

    class FakeContextBuilder:
        def __init__(self, session_store, *_args, **_kwargs) -> None:
            self.store = session_store

        async def build(self, **kwargs):
            messages = await self.store.get_messages_for_context(kwargs["session_id"])
            captured["history_messages"] = messages
            return SimpleNamespace(
                conversation_history=[
                    {"role": item["role"], "content": item["content"]}
                    for item in messages
                ],
                conversation_summary="",
                context_text="",
                token_count=0,
                budget=0,
            )

    class FakeOrchestrator:
        async def handle(self, context):
            captured["conversation_history"] = context.conversation_history
            captured["config_overrides"] = context.config_overrides
            captured["metadata"] = context.metadata
            yield StreamEvent(
                type=StreamEventType.CONTENT,
                source="chat",
                stage="responding",
                content="Let's discuss this question.",
                metadata={"call_kind": "llm_final_response"},
            )
            yield StreamEvent(type=StreamEventType.DONE, source="chat")

    monkeypatch.setattr(
        "deeptutor.services.llm.config.get_llm_config",
        lambda: SimpleNamespace(api_key="k", base_url="u", api_version="v1"),
    )
    monkeypatch.setattr("deeptutor.services.session.context_builder.ContextBuilder", FakeContextBuilder)
    monkeypatch.setattr("deeptutor.runtime.orchestrator.ChatOrchestrator", FakeOrchestrator)
    monkeypatch.setattr(
        "deeptutor.services.memory.get_memory_service",
        lambda: SimpleNamespace(
            build_memory_context=lambda owner_user_id=None: "",
            refresh_from_turn=_noop_refresh,
        ),
    )

    session, turn = await runtime.start_turn(
        {
            "type": "start_turn",
            "content": "Why is my answer wrong?",
            "session_id": None,
            "capability": None,
            "tools": [],
            "knowledge_bases": [],
            "attachments": [],
            "language": "en",
            "config": {
                "followup_question_context": {
                    "parent_quiz_session_id": "quiz_session_1",
                    "question_id": "q_2",
                    "question_type": "choice",
                    "difficulty": "hard",
                    "concentration": "win-rate comparison",
                    "question": "Which criterion best describes density?",
                    "options": {
                        "A": "Coverage",
                        "B": "Informative value",
                        "C": "Relevant content without redundancy",
                        "D": "Credibility",
                    },
                    "user_answer": "B",
                    "correct_answer": "C",
                    "explanation": "Density focuses on including relevant content without redundancy.",
                    "knowledge_context": "Density measures whether content is relevant and non-redundant.",
                }
            },
        }
    )

    events = []
    async for event in runtime.subscribe_turn(turn["id"], after_seq=0):
        events.append(event)

    assert [event["type"] for event in events] == ["session", "content", "done"]
    detail = await store.get_session_with_messages(session["id"])
    assert detail is not None
    assert [message["role"] for message in detail["messages"]] == ["system", "user", "assistant"]
    assert "Question Follow-up Context" in detail["messages"][0]["content"]
    assert "Which criterion best describes density?" in detail["messages"][0]["content"]
    assert "User answer: B" in detail["messages"][0]["content"]
    assert captured["conversation_history"][0]["role"] == "system"
    assert "followup_question_context" not in captured["config_overrides"]
    assert captured["metadata"]["question_followup_context"]["question_id"] == "q_2"


@pytest.mark.asyncio
async def test_turn_runtime_rejects_deep_research_without_explicit_config(
    tmp_path,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    runtime = TurnRuntimeManager(store)

    with pytest.raises(RuntimeError, match="Invalid deep research config"):
        await runtime.start_turn(
            {
                "type": "start_turn",
                "content": "research transformers",
                "session_id": None,
                "capability": "deep_research",
                "tools": ["rag"],
                "knowledge_bases": ["research-kb"],
                "attachments": [],
                "language": "en",
                "config": {},
            }
        )


@pytest.mark.asyncio
async def test_turn_runtime_persists_deep_research_session_preference(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    runtime = TurnRuntimeManager(store)

    class FakeContextBuilder:
        def __init__(self, *_args, **_kwargs) -> None:
            pass

        async def build(self, **_kwargs):
            return SimpleNamespace(
                conversation_history=[],
                conversation_summary="",
                context_text="",
                token_count=0,
                budget=0,
            )

    class FakeOrchestrator:
        async def handle(self, _context):
            yield StreamEvent(
                type=StreamEventType.CONTENT,
                source="deep_research",
                stage="reporting",
                content="Research report ready.",
                metadata={"call_kind": "llm_final_response"},
            )
            yield StreamEvent(type=StreamEventType.DONE, source="deep_research")

    monkeypatch.setattr(
        "deeptutor.services.llm.config.get_llm_config",
        lambda: SimpleNamespace(api_key="k", base_url="u", api_version="v1"),
    )
    monkeypatch.setattr("deeptutor.services.session.context_builder.ContextBuilder", FakeContextBuilder)
    monkeypatch.setattr("deeptutor.runtime.orchestrator.ChatOrchestrator", FakeOrchestrator)
    monkeypatch.setattr(
        "deeptutor.services.memory.get_memory_service",
        lambda: SimpleNamespace(
            build_memory_context=lambda owner_user_id=None: "",
            refresh_from_turn=_noop_refresh,
        ),
    )

    session, turn = await runtime.start_turn(
        {
            "type": "start_turn",
            "content": "research transformers",
            "session_id": None,
            "capability": "deep_research",
            "tools": ["rag", "web_search"],
            "knowledge_bases": ["research-kb"],
            "attachments": [],
            "language": "en",
            "config": {
                "mode": "report",
                "depth": "standard",
                "sources": ["kb", "web"],
            },
        }
    )

    events = []
    async for event in runtime.subscribe_turn(turn["id"], after_seq=0):
        events.append(event)

    assert [event["type"] for event in events] == ["session", "content", "done"]
    detail = await store.get_session_with_messages(session["id"])
    assert detail is not None
    assert detail["preferences"]["capability"] == "deep_research"
    assert detail["preferences"]["tools"] == ["rag", "web_search"]


@pytest.mark.asyncio
async def test_turn_runtime_injects_memory_and_refreshes_after_completion(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    runtime = TurnRuntimeManager(store)
    captured: dict[str, object] = {}

    class FakeContextBuilder:
        def __init__(self, *_args, **_kwargs) -> None:
            pass

        async def build(self, **_kwargs):
            return SimpleNamespace(
                conversation_history=[],
                conversation_summary="",
                context_text="Recent chat summary",
                token_count=0,
                budget=0,
            )

    class FakeOrchestrator:
        async def handle(self, context):
            captured["conversation_history"] = context.conversation_history
            captured["memory_context"] = context.memory_context
            captured["conversation_context_text"] = context.metadata.get("conversation_context_text")
            yield StreamEvent(
                type=StreamEventType.CONTENT,
                source="chat",
                stage="responding",
                content="Stored reply",
                metadata={"call_kind": "llm_final_response"},
            )
            yield StreamEvent(type=StreamEventType.DONE, source="chat")

    refresh_calls: list[dict[str, object]] = []

    async def fake_refresh_from_turn(**kwargs):
        refresh_calls.append(kwargs)
        return None

    def fake_build_memory_context(owner_user_id=None):
        captured["memory_owner_user_id"] = owner_user_id
        return "## Memory\n## Preferences\n- Prefer concise answers."

    monkeypatch.setattr(
        "deeptutor.services.llm.config.get_llm_config",
        lambda: SimpleNamespace(api_key="k", base_url="u", api_version="v1"),
    )
    monkeypatch.setattr("deeptutor.services.session.context_builder.ContextBuilder", FakeContextBuilder)
    monkeypatch.setattr("deeptutor.runtime.orchestrator.ChatOrchestrator", FakeOrchestrator)
    monkeypatch.setattr(
        "deeptutor.services.memory.get_memory_service",
        lambda: SimpleNamespace(
            build_memory_context=fake_build_memory_context,
            refresh_from_turn=fake_refresh_from_turn,
        ),
    )

    _session, turn = await runtime.start_turn(
        {
            "type": "start_turn",
            "content": "hello, i'm frank",
            "session_id": None,
            "capability": None,
            "tools": [],
            "knowledge_bases": [],
            "attachments": [],
            "language": "en",
            "config": {},
        },
        owner_user_id="teacher-1",
    )

    async for _event in runtime.subscribe_turn(turn["id"], after_seq=0):
        pass

    assert captured["memory_context"] == "## Memory\n## Preferences\n- Prefer concise answers."
    assert captured["memory_owner_user_id"] == "teacher-1"
    assert captured["conversation_history"] == []
    assert captured["conversation_context_text"] == "Recent chat summary"
    assert refresh_calls[0]["assistant_message"] == "Stored reply"
    assert refresh_calls[0]["owner_user_id"] == "teacher-1"


@pytest.mark.asyncio
async def test_turn_runtime_passes_agent_spec_id_for_live_chat_policy_binding(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    runtime = TurnRuntimeManager(store)
    captured: dict[str, object] = {}
    service = AgentSpecService(tmp_path / "agent_specs")
    service.create_pack(
        agent_id="strict-fractions",
        display_name="Strict Fractions",
        structured={
            "identity": {
                "agent_name": "Strict Fractions",
                "subject": "Mathematics",
                "grade_band": "Grade 6",
                "tone": "Strict and concise",
                "primary_language": "English",
                "persona_summary": "A teacher-defined tutor for precise fraction practice.",
            },
            "soul": {
                "teaching_philosophy": "Require justification before correction.",
                "when_student_wrong": "Ask the student to explain the misconception first.",
                "when_student_stuck": "Give a minimal hint only after the student states a plan.",
                "encouragement_style": "Calm and demanding.",
            },
            "rules": {
                "do_not_solve_directly": "yes",
                "max_session_minutes": "20",
                "hint_policy": "One hint after a student attempt.",
                "escalation_rule": "Escalate only after the student justifies a retry.",
                "guardrails": "Never provide the final answer without a student attempt.",
            },
        },
    )

    class FakeContextBuilder:
        def __init__(self, *_args, **_kwargs) -> None:
            pass

        async def build(self, **_kwargs):
            return SimpleNamespace(
                conversation_history=[],
                conversation_summary="",
                context_text="",
                token_count=0,
                budget=0,
            )

    class FakePipeline:
        def __init__(self, language: str = "en") -> None:
            captured["language"] = language

        async def run(self, context, stream) -> None:
            captured["config_overrides"] = dict(context.config_overrides)
            captured["memory_context"] = context.memory_context
            await stream.content(
                "First, explain which denominator you would build and why.",
                source="chat",
                stage="responding",
            )

    monkeypatch.setattr(
        "deeptutor.services.llm.config.get_llm_config",
        lambda: SimpleNamespace(api_key="k", base_url="u", api_version="v1"),
    )
    monkeypatch.setattr("deeptutor.services.session.context_builder.ContextBuilder", FakeContextBuilder)
    monkeypatch.setattr(
        "deeptutor.services.memory.get_memory_service",
        lambda: SimpleNamespace(
            build_memory_context=lambda owner_user_id=None: "",
            refresh_from_turn=_noop_refresh,
        ),
    )
    monkeypatch.setattr("deeptutor.capabilities.chat.AgenticChatPipeline", FakePipeline)
    monkeypatch.setattr(runtime_policy_compiler, "get_agent_spec_service", lambda: service)

    _session, turn = await runtime.start_turn(
        {
            "type": "start_turn",
            "content": "Can you just solve 5/6 - 1/2 for me?",
            "session_id": None,
            "capability": "chat",
            "tools": [],
            "knowledge_bases": [],
            "attachments": [],
            "language": "en",
            "config": {
                "agent_spec_id": "strict-fractions",
            },
        }
    )

    events = []
    async for event in runtime.subscribe_turn(turn["id"], after_seq=0):
        events.append(event)

    assert captured["config_overrides"]["agent_spec_id"] == "strict-fractions"
    assert "Teacher Spec Reference:\nstrict-fractions" in str(captured["memory_context"])
    assert "Require justification before correction." in str(captured["memory_context"])
    assert events[-1]["metadata"]["status"] == "completed"


@pytest.mark.asyncio
async def test_turn_runtime_pins_agent_spec_version_per_session(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    runtime = TurnRuntimeManager(store)
    captured: list[str] = []
    service = AgentSpecService(tmp_path / "agent_specs")
    service.create_pack(
        agent_id="fraction-coach",
        display_name="Fraction Coach",
        structured={
            "identity": {"agent_name": "Fraction Coach"},
            "soul": {"teaching_philosophy": "Version one philosophy."},
            "rules": {"guardrails": "Version one guardrails."},
        },
    )

    class FakeContextBuilder:
        def __init__(self, *_args, **_kwargs) -> None:
            pass

        async def build(self, **_kwargs):
            return SimpleNamespace(
                conversation_history=[],
                conversation_summary="",
                context_text="",
                token_count=0,
                budget=0,
            )

    class FakePipeline:
        def __init__(self, language: str = "en") -> None:
            captured.append(f"lang={language}")

        async def run(self, context, stream) -> None:
            captured.append(str(context.memory_context))
            captured.append(str(context.metadata.get("session_preferences", {})))
            await stream.content("Pinned response", source="chat", stage="responding")

    monkeypatch.setattr(
        "deeptutor.services.llm.config.get_llm_config",
        lambda: SimpleNamespace(api_key="k", base_url="u", api_version="v1"),
    )
    monkeypatch.setattr("deeptutor.services.session.context_builder.ContextBuilder", FakeContextBuilder)
    monkeypatch.setattr(
        "deeptutor.services.memory.get_memory_service",
        lambda: SimpleNamespace(
            build_memory_context=lambda owner_user_id=None: "",
            refresh_from_turn=_noop_refresh,
        ),
    )
    monkeypatch.setattr("deeptutor.capabilities.chat.AgenticChatPipeline", FakePipeline)
    monkeypatch.setattr(runtime_policy_compiler, "get_agent_spec_service", lambda: service)

    session, turn = await runtime.start_turn(
        {
            "type": "start_turn",
            "content": "Help me with fractions",
            "session_id": None,
            "capability": "chat",
            "tools": [],
            "knowledge_bases": [],
            "attachments": [],
            "language": "en",
            "config": {
                "agent_spec_id": "fraction-coach",
            },
        }
    )

    async for _event in runtime.subscribe_turn(turn["id"], after_seq=0):
        pass

    persisted = await store.get_session(session["id"])
    assert persisted is not None
    assert "agent_spec_pin" in captured[-1]
    assert persisted["preferences"]["agent_spec_pin"]["agent_spec_id"] == "fraction-coach"
    assert persisted["preferences"]["agent_spec_pin"]["version"] == 1

    service.save_pack(
        agent_id="fraction-coach",
        display_name="Fraction Coach",
        structured={
            "identity": {"agent_name": "Fraction Coach"},
            "soul": {"teaching_philosophy": "Version two philosophy."},
            "rules": {"guardrails": "Version two guardrails."},
        },
    )

    _session, second_turn = await runtime.start_turn(
        {
            "type": "start_turn",
            "content": "Help me again",
            "session_id": session["id"],
            "capability": "chat",
            "tools": [],
            "knowledge_bases": [],
            "attachments": [],
            "language": "en",
            "config": {},
        }
    )

    async for _event in runtime.subscribe_turn(second_turn["id"], after_seq=0):
        pass

    memory_contexts = [entry for entry in captured if "Teacher Runtime Policy:" in entry]
    assert "Version one philosophy." in memory_contexts[0]
    assert "Version one philosophy." in memory_contexts[1]
    assert "Version two philosophy." not in memory_contexts[1]


@pytest.mark.asyncio
async def test_turn_runtime_passes_agent_spec_id_for_deep_question_policy_binding(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    runtime = TurnRuntimeManager(store)
    captured: dict[str, object] = {}
    service = AgentSpecService(tmp_path / "agent_specs")
    service.create_pack(
        agent_id="strict-fractions",
        display_name="Strict Fractions",
        structured={
            "identity": {"agent_name": "Strict Fractions"},
            "assessment": {"question_quality_bar": "Require justification prompts."},
            "rules": {"guardrails": "Do not reveal final answers in stems."},
        },
    )

    class FakeContextBuilder:
        def __init__(self, *_args, **_kwargs) -> None:
            pass

        async def build(self, **_kwargs):
            return SimpleNamespace(
                conversation_history=[],
                conversation_summary="",
                context_text="",
                token_count=0,
                budget=0,
            )

    class FakeCoordinator:
        def __init__(self, **_kwargs) -> None:
            self._callback = None

        def set_ws_callback(self, callback) -> None:
            self._callback = callback

        async def generate_from_topic(self, **kwargs):
            captured["preference"] = kwargs["preference"]
            if self._callback is not None:
                await self._callback({"type": "idea_round", "message": "ideas"})
            return {"results": []}

    import sys
    import types

    llm_module = types.ModuleType("deeptutor.services.llm.config")
    llm_module.get_llm_config = lambda: SimpleNamespace(api_key="k", base_url="u", api_version="v1")
    monkeypatch.setitem(sys.modules, "deeptutor.services.llm.config", llm_module)
    monkeypatch.setattr("deeptutor.services.session.context_builder.ContextBuilder", FakeContextBuilder)
    monkeypatch.setattr(
        "deeptutor.services.memory.get_memory_service",
        lambda: SimpleNamespace(
            build_memory_context=lambda owner_user_id=None: "",
            refresh_from_turn=_noop_refresh,
        ),
    )
    monkeypatch.setattr(runtime_policy_compiler, "get_agent_spec_service", lambda: service)

    module = types.ModuleType("deeptutor.agents.question.coordinator")
    module.AgentCoordinator = FakeCoordinator
    monkeypatch.setitem(sys.modules, "deeptutor.agents.question.coordinator", module)

    _session, turn = await runtime.start_turn(
        {
            "type": "start_turn",
            "content": "make a quiz",
            "session_id": None,
            "capability": "deep_question",
            "tools": ["rag"],
            "knowledge_bases": ["math-pack"],
            "attachments": [],
            "language": "en",
            "config": {
                "mode": "custom",
                "topic": "compare fractions",
                "agent_spec_id": "strict-fractions",
            },
        }
    )

    events = []
    async for event in runtime.subscribe_turn(turn["id"], after_seq=0):
        events.append(event)

    assert "Teacher Assessment Runtime Policy:" in str(captured["preference"])
    assert "Strict Fractions" in str(captured["preference"])
    assert events[-1]["metadata"]["status"] == "completed"


@pytest.mark.asyncio
async def test_turn_runtime_passes_agent_spec_id_for_deep_solve_policy_binding(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    runtime = TurnRuntimeManager(store)
    captured: dict[str, object] = {}
    service = AgentSpecService(tmp_path / "agent_specs")
    service.create_pack(
        agent_id="strict-fractions",
        display_name="Strict Fractions",
        structured={
            "identity": {"agent_name": "Strict Fractions"},
            "soul": {"teaching_philosophy": "Require justification before correction."},
            "rules": {"guardrails": "Do not give final answers immediately."},
        },
    )

    class FakeContextBuilder:
        def __init__(self, *_args, **_kwargs) -> None:
            pass

        async def build(self, **_kwargs):
            return SimpleNamespace(
                conversation_history=[],
                conversation_summary="",
                context_text="",
                token_count=0,
                budget=0,
            )

    class FakeSolver:
        def __init__(self, **_kwargs) -> None:
            self.logger = SimpleNamespace(
                logger=SimpleNamespace(addHandler=lambda *_: None, removeHandler=lambda *_: None)
            )

        async def ainit(self) -> None:
            return None

        async def solve(self, **kwargs):
            captured["conversation_context"] = kwargs["conversation_context"]
            return {"final_answer": "Start by naming the denominator you want to build."}

    import sys
    import types

    llm_module = types.ModuleType("deeptutor.services.llm.config")
    llm_module.get_llm_config = lambda: SimpleNamespace(api_key="k", base_url="u", api_version="v1")
    monkeypatch.setitem(sys.modules, "deeptutor.services.llm.config", llm_module)
    monkeypatch.setattr("deeptutor.services.session.context_builder.ContextBuilder", FakeContextBuilder)
    monkeypatch.setattr(
        "deeptutor.services.memory.get_memory_service",
        lambda: SimpleNamespace(
            build_memory_context=lambda owner_user_id=None: "",
            refresh_from_turn=_noop_refresh,
        ),
    )
    monkeypatch.setattr(runtime_policy_compiler, "get_agent_spec_service", lambda: service)

    module = types.ModuleType("deeptutor.agents.solve.main_solver")
    module.MainSolver = FakeSolver
    monkeypatch.setitem(sys.modules, "deeptutor.agents.solve.main_solver", module)

    _session, turn = await runtime.start_turn(
        {
            "type": "start_turn",
            "content": "Can you solve 5/6 - 1/2 for me?",
            "session_id": None,
            "capability": "deep_solve",
            "tools": ["rag"],
            "knowledge_bases": ["math-pack"],
            "attachments": [],
            "language": "en",
            "config": {
                "detailed_answer": False,
                "agent_spec_id": "strict-fractions",
            },
        }
    )

    events = []
    async for event in runtime.subscribe_turn(turn["id"], after_seq=0):
        events.append(event)

    assert "Teacher Runtime Policy:" in str(captured["conversation_context"])
    assert "Require justification before correction." in str(captured["conversation_context"])
    assert events[-1]["metadata"]["status"] == "completed"
