from __future__ import annotations

import asyncio
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from deeptutor.core.stream import StreamEvent, StreamEventType
from deeptutor.services.session.turn_runtime import (
    _LiveSubscriber,
    _TurnExecution,
    _build_tutoring_observations,
    _clip_text,
    _ensure_agent_spec_pin,
    _extract_followup_question_context,
    _extract_persist_user_message,
    _format_followup_question_context,
    _should_capture_assistant_content,
    get_turn_runtime_manager,
)
from deeptutor.services.session.turn_runtime import TurnRuntimeManager


class _FakePinStore:
    def __init__(self, preferences: dict | None = None) -> None:
        self.preferences = preferences or {}
        self.updated: list[tuple[str, dict]] = []

    async def get_session(self, _session_id: str) -> dict:
        return {"preferences": dict(self.preferences)}

    async def update_session_preferences(self, session_id: str, updates: dict) -> None:
        self.updated.append((session_id, updates))


def test_should_capture_assistant_content_only_keeps_final_llm_chunks() -> None:
    content = StreamEvent(type=StreamEventType.CONTENT, source="chat", content="hello")
    tool_chunk = StreamEvent(
        type=StreamEventType.CONTENT,
        source="chat",
        content="tool",
        metadata={"call_id": "c1", "call_kind": "tool"},
    )
    final_chunk = StreamEvent(
        type=StreamEventType.CONTENT,
        source="chat",
        content="final",
        metadata={"call_id": "c2", "call_kind": "llm_final_response"},
    )
    progress = StreamEvent(type=StreamEventType.PROGRESS, source="chat", content="noop")

    assert _should_capture_assistant_content(content) is True
    assert _should_capture_assistant_content(tool_chunk) is False
    assert _should_capture_assistant_content(final_chunk) is True
    assert _should_capture_assistant_content(progress) is False


def test_clip_text_trims_and_truncates() -> None:
    assert _clip_text("  hello  ", limit=10) == "hello"
    assert _clip_text("abcdef", limit=4) == "abcd\n...[truncated]"


@pytest.mark.asyncio
async def test_ensure_agent_spec_pin_keeps_existing_pin() -> None:
    store = _FakePinStore({"agent_spec_pin": {"agent_spec_id": "demo", "version": 2}})

    preferences = await _ensure_agent_spec_pin(store, "session-1", {"agent_spec_id": "ignored"})

    assert preferences["agent_spec_pin"]["agent_spec_id"] == "demo"
    assert store.updated == []


@pytest.mark.asyncio
async def test_ensure_agent_spec_pin_skips_missing_or_unknown_spec(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "deeptutor.services.runtime_policy.compiler.get_agent_spec_service",
        lambda: SimpleNamespace(get_pack=lambda _agent_spec_id: (_ for _ in ()).throw(FileNotFoundError())),
    )
    store = _FakePinStore()

    no_spec = await _ensure_agent_spec_pin(store, "session-1", {})
    missing_spec = await _ensure_agent_spec_pin(store, "session-1", {"agent_spec_id": "missing"})

    assert no_spec == {}
    assert missing_spec == {}
    assert store.updated == []


@pytest.mark.asyncio
async def test_ensure_agent_spec_pin_persists_pack_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "deeptutor.services.runtime_policy.compiler.get_agent_spec_service",
        lambda: SimpleNamespace(
            get_pack=lambda _agent_spec_id: {
                "agent_id": "agent/demo",
                "version": 3,
                "updated_at": "2026-05-01T09:00:00",
            }
        ),
    )
    store = _FakePinStore()

    preferences = await _ensure_agent_spec_pin(store, "session-1", {"agent_spec_id": "demo"})

    assert preferences["agent_spec_pin"] == {
        "agent_spec_id": "agent/demo",
        "version": 3,
        "updated_at": "2026-05-01T09:00:00",
    }
    assert store.updated == [
        (
            "session-1",
            {
                "agent_spec_pin": {
                    "agent_spec_id": "agent/demo",
                    "version": 3,
                    "updated_at": "2026-05-01T09:00:00",
                }
            },
        )
    ]


def test_extract_followup_question_context_normalizes_payload() -> None:
    config = {
        "followup_question_context": {
            "parent_quiz_session_id": " quiz-1 ",
            "question_id": " q-1 ",
            "question": " What is 2 + 2? ",
            "question_type": "mcq",
            "options": {"a": "3", " B ": "4", "C": "  "},
            "correct_answer": "B",
            "explanation": "Because 4 is correct",
            "difficulty": "easy",
            "concentration": "algebra",
            "knowledge_context": "x" * 50,
            "user_answer": "A",
            "is_correct": False,
        }
    }

    context = _extract_followup_question_context(config)

    assert "followup_question_context" not in config
    assert context == {
        "parent_quiz_session_id": "quiz-1",
        "question_id": "q-1",
        "question": "What is 2 + 2?",
        "question_type": "mcq",
        "options": {"A": "3", "B": "4"},
        "correct_answer": "B",
        "explanation": "Because 4 is correct",
        "difficulty": "easy",
        "concentration": "algebra",
        "knowledge_context": "x" * 50,
        "user_answer": "A",
        "is_correct": False,
    }


def test_extract_followup_question_context_rejects_invalid_payloads() -> None:
    assert _extract_followup_question_context(None) is None
    assert _extract_followup_question_context({"followup_question_context": "bad"}) is None
    assert (
        _extract_followup_question_context({"followup_question_context": {"question": "   "}})
        is None
    )


def test_extract_persist_user_message_supports_strings_and_defaults() -> None:
    assert _extract_persist_user_message(None) is True
    assert _extract_persist_user_message({"_persist_user_message": False}) is False
    assert _extract_persist_user_message({"_persist_user_message": "false"}) is False
    assert _extract_persist_user_message({"_persist_user_message": "yes"}) is True
    assert _extract_persist_user_message({"_persist_user_message": 0}) is False


def test_format_followup_question_context_supports_en_and_zh() -> None:
    context = {
        "parent_quiz_session_id": "quiz-1",
        "question_id": "q-1",
        "question_type": "mcq",
        "difficulty": "easy",
        "concentration": "algebra",
        "question": "What is 2 + 2?",
        "options": {"A": "3", "B": "4"},
        "user_answer": "A",
        "is_correct": False,
        "correct_answer": "B",
        "explanation": "Because 4 is correct",
        "knowledge_context": "Use addition facts.",
    }

    english = _format_followup_question_context(context, language="en")
    chinese = _format_followup_question_context(context, language="zh-CN")

    assert "Question ID: q-1" in english
    assert "A. 3" in english
    assert "User result: incorrect" in english
    assert "Knowledge context:" in english
    assert "你正在处理一道测验题的后续追问。" in chinese
    assert "Reference answer: B" in chinese


def test_build_tutoring_observations_short_circuits_or_delegates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert (
        _build_tutoring_observations(
            capability="deep_solve",
            session_id="s1",
            student_id="u1",
            user_message="hello",
            assistant_message="world",
            followup_question_context=None,
            assistant_events=[],
        )
        == []
    )
    assert (
        _build_tutoring_observations(
            capability="chat",
            session_id="s1",
            student_id="u1",
            user_message=" ",
            assistant_message=" ",
            followup_question_context=None,
            assistant_events=[],
        )
        == []
    )

    monkeypatch.setattr(
        "deeptutor.services.evidence.extractor.extract_observations_from_tutoring_turn",
        lambda **kwargs: [{"kind": "observation", "payload": kwargs}],
    )
    result = _build_tutoring_observations(
        capability="chat",
        session_id="s1",
        student_id="u1",
        user_message="hello",
        assistant_message="world",
        followup_question_context={"question": "demo"},
        assistant_events=[{"type": "content"}],
    )

    assert result[0]["kind"] == "observation"
    assert result[0]["payload"]["session_id"] == "s1"


@pytest.mark.asyncio
async def test_persist_and_publish_sets_done_status_and_notifies_subscribers(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    class _FakeStore:
        async def append_turn_event(self, _turn_id: str, payload: dict) -> dict:
            return {**payload, "seq": 5}

    runtime = TurnRuntimeManager(_FakeStore())
    queue: asyncio.Queue[dict] = asyncio.Queue()
    execution = _TurnExecution(
        turn_id="turn-1",
        session_id="session-1",
        capability="chat",
        payload={},
        subscribers=[_LiveSubscriber(queue=queue)],
    )
    runtime._executions["turn-1"] = execution

    monkeypatch.setattr(
        "deeptutor.services.session.turn_runtime.get_path_service",
        lambda: SimpleNamespace(
            get_task_workspace=lambda capability, turn_id: tmp_path / capability / turn_id
        ),
    )

    payload = await runtime._persist_and_publish(
        execution,
        StreamEvent(type=StreamEventType.DONE, source="chat"),
    )

    assert payload["metadata"]["status"] == "completed"
    assert payload["session_id"] == "session-1"
    assert payload["turn_id"] == "turn-1"
    assert await queue.get() == payload
    event_file = tmp_path / "chat" / "turn-1" / "events.jsonl"
    assert json.loads(event_file.read_text(encoding="utf-8").strip())["seq"] == 5


@pytest.mark.asyncio
async def test_persist_and_publish_tolerates_missing_turn(monkeypatch: pytest.MonkeyPatch) -> None:
    class _FakeStore:
        async def append_turn_event(self, _turn_id: str, _payload: dict) -> dict:
            raise ValueError("Turn not found: turn-1")

    runtime = TurnRuntimeManager(_FakeStore())
    monkeypatch.setattr(
        TurnRuntimeManager,
        "_mirror_event_to_workspace",
        staticmethod(lambda *_args, **_kwargs: None),
    )
    execution = _TurnExecution(turn_id="turn-1", session_id="session-1", capability="chat", payload={})

    payload = await runtime._persist_and_publish(
        execution,
        StreamEvent(type=StreamEventType.ERROR, source="chat", content="failed"),
    )

    assert payload["type"] == "error"
    assert payload["content"] == "failed"


def test_mirror_event_to_workspace_swallow_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    execution = _TurnExecution(turn_id="turn-1", session_id="session-1", capability="chat", payload={})
    monkeypatch.setattr(
        "deeptutor.services.session.turn_runtime.get_path_service",
        lambda: SimpleNamespace(get_task_workspace=lambda *_args: (_ for _ in ()).throw(RuntimeError("boom"))),
    )

    TurnRuntimeManager._mirror_event_to_workspace(execution, {"type": "content"})


def test_get_turn_runtime_manager_reuses_singleton(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("deeptutor.services.session.turn_runtime._runtime_instance", None)

    manager_one = get_turn_runtime_manager()
    manager_two = get_turn_runtime_manager()

    assert manager_one is manager_two
