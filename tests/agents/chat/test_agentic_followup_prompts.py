from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

from deeptutor.agents.chat.agentic_pipeline import AgenticChatPipeline
from deeptutor.core.context import UnifiedContext
from deeptutor.core.stream import StreamEvent
from deeptutor.core.stream_bus import StreamBus


async def _collect_bus_events(bus: StreamBus) -> tuple[list[StreamEvent], asyncio.Task[Any]]:
    events: list[StreamEvent] = []

    async def _consume() -> None:
        async for event in bus.subscribe():
            events.append(event)

    consumer = asyncio.create_task(_consume())
    await asyncio.sleep(0)
    return events, consumer  # type: ignore[return-value]


def test_extract_followup_questions_parses_visible_section(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "deeptutor.agents.chat.agentic_pipeline.get_llm_config",
        lambda: SimpleNamespace(
            binding="openai",
            model="gpt-test",
            api_key="k",
            base_url="u",
            api_version=None,
        ),
    )
    monkeypatch.setattr(
        "deeptutor.agents.chat.agentic_pipeline.get_tool_registry",
        lambda: SimpleNamespace(build_prompt_text=lambda *_args, **_kwargs: "", get_enabled=lambda _selected: []),
    )
    pipeline = AgenticChatPipeline(language="en")

    cleaned, questions = pipeline._extract_followup_questions(
        "The derivative of x^2 is 2x.\n\n"
        "Follow-up questions:\n"
        "1. Which power rule applies to x^2?\n"
        "2. What derivative do you get for x^3?\n"
        "3. Why is 2x different from x here?"
    )

    assert cleaned.startswith("The derivative of x^2 is 2x.")
    assert questions == [
        "Which power rule applies to x^2?",
        "What derivative do you get for x^3?",
        "Why is 2x different from x here?",
    ]


@pytest.mark.asyncio
async def test_run_emits_followup_questions_in_result_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "deeptutor.agents.chat.agentic_pipeline.get_llm_config",
        lambda: SimpleNamespace(
            binding="openai",
            model="gpt-test",
            api_key="k",
            base_url="u",
            api_version=None,
        ),
    )
    monkeypatch.setattr(
        "deeptutor.agents.chat.agentic_pipeline.get_tool_registry",
        lambda: SimpleNamespace(build_prompt_text=lambda *_args, **_kwargs: "", get_enabled=lambda _selected: []),
    )

    pipeline = AgenticChatPipeline(language="en")
    monkeypatch.setattr(pipeline, "_extract_answer_now_context", lambda _context: None)

    async def fake_stage_thinking(*_args, **_kwargs):
        return ""

    async def fake_stage_acting(*_args, **_kwargs):
        return []

    async def fake_stage_observing(*_args, **_kwargs):
        return "Student is still mixing up the power rule."

    async def fake_stage_responding(*_args, **_kwargs):
        return (
            "The derivative of x^2 is 2x because the exponent becomes a multiplier and then drops by one.\n\n"
            "Follow-up questions:\n"
            "1. What derivative do you get for x^3?\n"
            "2. Which step turns x^2 into 2x?\n",
            {"label": "Final response"},
        )

    monkeypatch.setattr(pipeline, "_stage_thinking", fake_stage_thinking)
    monkeypatch.setattr(pipeline, "_stage_acting", fake_stage_acting)
    monkeypatch.setattr(pipeline, "_stage_observing", fake_stage_observing)
    monkeypatch.setattr(pipeline, "_stage_responding", fake_stage_responding)

    bus = StreamBus()
    events, consumer = await _collect_bus_events(bus)
    context = UnifiedContext(
        session_id="session-1",
        user_message="I think the derivative of x^2 is x.",
        enabled_tools=[],
        language="en",
        metadata={"turn_id": "turn-1"},
    )

    await pipeline.run(context, bus)
    await asyncio.sleep(0)
    await bus.close()
    await consumer

    result_event = next(event for event in events if event.type.value == "result")
    assert result_event.metadata["followup_questions"] == [
        "What derivative do you get for x^3?",
        "Which step turns x^2 into 2x?",
    ]
    assert "Follow-up questions:" in result_event.metadata["response"]
