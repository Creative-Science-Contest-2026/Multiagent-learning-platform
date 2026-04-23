from __future__ import annotations

from typing import Any

import pytest

from deeptutor.agents.question.coordinator import AgentCoordinator
from deeptutor.agents.question.models import QuestionTemplate


class _StubIdeaAgent:
    def __init__(self, captured: dict[str, Any]) -> None:
        self._captured = captured

    async def process(self, **kwargs: Any) -> dict[str, Any]:
        self._captured["idea_process"] = kwargs
        return {
            "templates": [
                QuestionTemplate(
                    question_id="",
                    concentration="linear equations",
                    question_type=kwargs.get("target_question_type") or "written",
                    difficulty=kwargs.get("target_difficulty") or "medium",
                )
            ],
            "knowledge_context": "recent quiz performance",
        }


@pytest.mark.asyncio
async def test_generate_from_topic_infers_hard_difficulty_from_recent_quiz_score(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}
    monkeypatch.setattr(
        "deeptutor.agents.question.coordinator.load_config_with_main",
        lambda *_args, **_kwargs: {},
    )
    coordinator = AgentCoordinator(output_dir=str(tmp_path))
    coordinator._create_idea_agent = lambda: _StubIdeaAgent(captured)  # type: ignore[method-assign]

    async def fake_generation_loop(**kwargs: Any) -> list[dict[str, Any]]:
        captured["generation_loop"] = kwargs
        return []

    coordinator._generation_loop = fake_generation_loop  # type: ignore[method-assign]

    result = await coordinator.generate_from_topic(
        user_topic="linear equations",
        preference="",
        num_questions=1,
        difficulty="",
        question_type="",
        history_context=(
            "[Quiz Performance]\n"
            "1. [q_1] Q: Solve 2x=6 -> Answered: 3 (Correct)\n"
            "2. [q_2] Q: Solve 3x=12 -> Answered: 4 (Correct)\n"
            "Score: 2/2 (100%)"
        ),
    )

    assert captured["idea_process"]["target_difficulty"] == "hard"
    assert result["trace"]["adaptive_difficulty"] == {
        "selected": "hard",
        "source": "history_context",
        "score_percent": 100,
    }


@pytest.mark.asyncio
async def test_generate_from_topic_respects_explicit_difficulty_over_history(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}
    monkeypatch.setattr(
        "deeptutor.agents.question.coordinator.load_config_with_main",
        lambda *_args, **_kwargs: {},
    )
    coordinator = AgentCoordinator(output_dir=str(tmp_path))
    coordinator._create_idea_agent = lambda: _StubIdeaAgent(captured)  # type: ignore[method-assign]

    async def fake_generation_loop(**kwargs: Any) -> list[dict[str, Any]]:
        return []

    coordinator._generation_loop = fake_generation_loop  # type: ignore[method-assign]

    result = await coordinator.generate_from_topic(
        user_topic="fractions",
        preference="",
        num_questions=1,
        difficulty="easy",
        question_type="",
        history_context=(
            "[Quiz Performance]\n"
            "1. [q_1] Q: Simplify 6/8 -> Answered: 3/4 (Correct)\n"
            "2. [q_2] Q: Simplify 9/12 -> Answered: 3/4 (Correct)\n"
            "Score: 2/2 (100%)"
        ),
    )

    assert captured["idea_process"]["target_difficulty"] == "easy"
    assert result["trace"]["adaptive_difficulty"] == {
        "selected": "easy",
        "source": "request",
    }


@pytest.mark.asyncio
async def test_generate_from_topic_infers_easy_difficulty_from_low_recent_quiz_score(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}
    monkeypatch.setattr(
        "deeptutor.agents.question.coordinator.load_config_with_main",
        lambda *_args, **_kwargs: {},
    )
    coordinator = AgentCoordinator(output_dir=str(tmp_path))
    coordinator._create_idea_agent = lambda: _StubIdeaAgent(captured)  # type: ignore[method-assign]

    async def fake_generation_loop(**kwargs: Any) -> list[dict[str, Any]]:
        return []

    coordinator._generation_loop = fake_generation_loop  # type: ignore[method-assign]

    result = await coordinator.generate_from_topic(
        user_topic="fractions",
        preference="",
        num_questions=1,
        difficulty="",
        question_type="",
        history_context=(
            "[Quiz Performance]\n"
            "1. [q_1] Q: Simplify 6/8 -> Answered: 6/8 (Incorrect, correct: 3/4)\n"
            "2. [q_2] Q: Simplify 9/12 -> Answered: 9/12 (Incorrect, correct: 3/4)\n"
            "Score: 0/2 (0%)"
        ),
    )

    assert captured["idea_process"]["target_difficulty"] == "easy"
    assert result["trace"]["adaptive_difficulty"] == {
        "selected": "easy",
        "source": "history_context",
        "score_percent": 0,
    }
