from __future__ import annotations

import sqlite3

import pytest
import fitz

try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
except Exception:  # pragma: no cover - optional dependency in lightweight envs
    FastAPI = None
    TestClient = None

from deeptutor.services.session.sqlite_store import SQLiteSessionStore

pytestmark = pytest.mark.skipif(FastAPI is None or TestClient is None, reason="fastapi not installed")


def _build_app(store: SQLiteSessionStore, monkeypatch: pytest.MonkeyPatch) -> FastAPI:
    from deeptutor.api.routers import dashboard

    app = FastAPI()
    app.include_router(dashboard.router, prefix="/api/v1/dashboard")
    monkeypatch.setattr(dashboard, "get_sqlite_session_store", lambda: store)
    return app


async def _seed_session(
    store: SQLiteSessionStore,
    *,
    session_id: str,
    capability: str,
    message: str,
    knowledge_bases: list[str],
    status: str = "completed",
) -> None:
    await store.create_session(session_id=session_id)
    await store.update_session_preferences(
        session_id,
        {
            "capability": capability,
            "tools": ["rag"] if knowledge_bases else [],
            "knowledge_bases": knowledge_bases,
            "language": "en",
        },
    )
    turn = await store.create_turn(session_id, capability=capability)
    await store.add_message(session_id, "user", message, capability=capability)
    await store.update_turn_status(turn["id"], status)


def _set_session_timestamp(store: SQLiteSessionStore, session_id: str, timestamp: float) -> None:
    with sqlite3.connect(store.db_path) as conn:
        conn.execute(
            "UPDATE sessions SET created_at = ?, updated_at = ? WHERE id = ?",
            (timestamp, timestamp, session_id),
        )
        conn.execute(
            "UPDATE turns SET created_at = ?, updated_at = ?, finished_at = ? WHERE session_id = ?",
            (timestamp, timestamp, timestamp, session_id),
        )
        conn.execute(
            "UPDATE messages SET created_at = ? WHERE session_id = ?",
            (timestamp, session_id),
        )
        conn.commit()


@pytest.mark.asyncio
async def test_dashboard_overview_groups_activity_and_knowledge_packs(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await _seed_session(
        store,
        session_id="quiz-session",
        capability="deep_question",
        message="Generate a quiz on quadratic equations",
        knowledge_bases=["math-pack"],
    )
    await _seed_session(
        store,
        session_id="tutor-session",
        capability="chat",
        message="Help a student review linear functions",
        knowledge_bases=["math-pack"],
        status="running",
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/dashboard/overview")

    assert response.status_code == 200
    payload = response.json()
    assert payload["totals"]["total_sessions"] == 2
    assert payload["totals"]["assessments"] == 1
    assert payload["totals"]["tutoring_sessions"] == 1
    assert payload["totals"]["running"] == 1
    assert payload["knowledge_packs"] == [{"name": "math-pack", "session_count": 2}]
    assert payload["recent_activity"][0]["knowledge_bases"] == ["math-pack"]
    assert payload["recent_activity"][0]["type"] in {"assessment", "tutoring"}


@pytest.mark.asyncio
async def test_dashboard_recent_filters_assessment_activity(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await _seed_session(
        store,
        session_id="quiz-session",
        capability="deep_question",
        message="Generate a quiz",
        knowledge_bases=["math-pack"],
    )
    await _seed_session(
        store,
        session_id="chat-session",
        capability="chat",
        message="Tutor a student",
        knowledge_bases=["math-pack"],
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/dashboard/recent?type=assessment")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["id"] == "quiz-session"
    assert payload[0]["type"] == "assessment"


@pytest.mark.asyncio
async def test_dashboard_overview_includes_assessment_summary(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await _seed_session(
        store,
        session_id="quiz-session",
        capability="deep_question",
        message="Generate a quiz on fractions",
        knowledge_bases=["fractions-pack"],
    )
    await store.add_message(
        "quiz-session",
        "user",
        "[Quiz Performance]\n"
        "1. [q1] Q: 1+1 -> Answered: 2 (Correct)\n"
        "Score: 1/1 (100%)",
        capability="deep_question",
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/dashboard/overview")

    assert response.status_code == 200
    payload = response.json()
    assessment_row = payload["recent_activity"][0]
    assert assessment_row["review_ref"] == "dashboard/assessments/quiz-session"
    assert assessment_row["assessment_summary"]["score_percent"] == 100
    assert assessment_row["assessment_summary"]["total_questions"] == 1


@pytest.mark.asyncio
async def test_dashboard_assessment_analysis_returns_topic_breakdown(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await _seed_session(
        store,
        session_id="analysis-session",
        capability="deep_question",
        message="Generate a quiz on algebra",
        knowledge_bases=["algebra-pack"],
    )
    await store.add_message(
        "analysis-session",
        "user",
        "[Quiz Performance]\n"
        "1. [q1] Q: Solve algebra equation x + 2 = 5 -> Answered: 3 (Correct)\n"
        "2. [q2] Q: Solve algebra equation 2x = 10 -> Answered: 3 (Incorrect, correct: 5)\n"
        "Score: 1/2 (50%)",
        capability="deep_question",
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/dashboard/assessment-analysis/analysis-session")

    assert response.status_code == 200
    payload = response.json()
    assert payload["session_id"] == "analysis-session"
    assert payload["summary"]["score_percent"] == 50
    assert len(payload["performance_by_topic"]) >= 1
    assert "recommendations" in payload
    assert len(payload["recommendations"]) >= 1


@pytest.mark.asyncio
async def test_student_progress_summarizes_scores_topics_and_streak(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await _seed_session(
        store,
        session_id="assessment-recent",
        capability="deep_question",
        message="Generate a quiz on fractions",
        knowledge_bases=["fractions-pack"],
    )
    await store.add_message(
        "assessment-recent",
        "user",
        "[Quiz Performance]\n"
        "1. [q1] Q: Solve fractions addition 1/2 + 1/4 -> Answered: 3/4 (Correct)\n"
        "2. [q2] Q: Solve fractions subtraction 3/4 - 1/2 -> Answered: 1/5 (Incorrect, correct: 1/4)\n"
        "Score: 1/2 (50%)",
        capability="deep_question",
    )
    _set_session_timestamp(store, "assessment-recent", 1_710_000_000)

    await _seed_session(
        store,
        session_id="assessment-older",
        capability="deep_question",
        message="Generate a quiz on algebra",
        knowledge_bases=["algebra-pack"],
    )
    await store.add_message(
        "assessment-older",
        "user",
        "[Quiz Performance]\n"
        "1. [q1] Q: Solve algebra equation x + 2 = 5 -> Answered: 3 (Correct)\n"
        "2. [q2] Q: Solve algebra equation 2x = 10 -> Answered: 5 (Correct)\n"
        "Score: 2/2 (100%)",
        capability="deep_question",
    )
    _set_session_timestamp(store, "assessment-older", 1_709_913_600)

    await _seed_session(
        store,
        session_id="tutor-recent",
        capability="chat",
        message="Help me review fractions mistakes",
        knowledge_bases=["fractions-pack"],
    )
    _set_session_timestamp(store, "tutor-recent", 1_709_827_200)

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/dashboard/student-progress")

    assert response.status_code == 200
    payload = response.json()
    assert payload["totals"] == {
        "assessments_completed": 2,
        "tutoring_sessions": 1,
        "knowledge_packs_used": 2,
        "average_score_percent": 75,
        "streak_days": 3,
    }
    assert payload["focus_topics"][0]["topic"] == "fractions subtraction"
    assert payload["focus_topics"][0]["incorrect_count"] == 1
    assert payload["mastered_topics"][0]["topic"] == "algebra equation"
    assert payload["score_trend"] == [
        {"session_id": "assessment-older", "score_percent": 100, "timestamp": 1_709_913_600},
        {"session_id": "assessment-recent", "score_percent": 50, "timestamp": 1_710_000_000},
    ]
    assert [row["session_id"] for row in payload["recent_assessments"]] == [
        "assessment-recent",
        "assessment-older",
    ]
    assert payload["suggested_learning_path"][0]["topic"] == "fractions subtraction"
    assert payload["suggested_learning_path"][0]["status"] == "review"
    assert payload["suggested_learning_path"][0]["source"] == "focus_topic"


def test_learning_path_builder_includes_kb_objectives_and_skips_mastered(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from deeptutor.services import learning_path

    class FakeManager:
        def get_metadata(self, name: str) -> dict:
            if name == "fractions-pack":
                return {
                    "learning_objectives": [
                        "Fractions subtraction",
                        "Fractions addition",
                    ]
                }
            if name == "algebra-pack":
                return {"learning_objectives": ["Algebra equation"]}
            return {}

    monkeypatch.setattr(learning_path, "_get_kb_manager", lambda: FakeManager())

    suggestions = learning_path.build_suggested_learning_path(
        focus_topics=[
            {
                "topic": "fractions subtraction",
                "incorrect_count": 2,
                "accuracy_percent": 0,
            }
        ],
        mastered_topics=[
            {
                "topic": "algebra equation",
                "correct_count": 2,
                "accuracy_percent": 100,
            }
        ],
        knowledge_bases=["fractions-pack", "algebra-pack"],
    )

    assert suggestions == [
        {
            "topic": "fractions subtraction",
            "status": "review",
            "source": "focus_topic",
        },
        {
            "topic": "Fractions addition",
            "status": "next",
            "source": "learning_objective",
            "knowledge_base": "fractions-pack",
        },
    ]


@pytest.mark.asyncio
async def test_dashboard_overview_applies_search_kb_type_and_min_score_filters(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await _seed_session(
        store,
        session_id="algebra-high",
        capability="deep_question",
        message="Generate an algebra assessment",
        knowledge_bases=["algebra-pack"],
    )
    await store.add_message(
        "algebra-high",
        "user",
        "[Quiz Performance]\n"
        "1. [q1] Q: Solve algebra equation x + 2 = 5 -> Answered: 3 (Correct)\n"
        "Score: 1/1 (100%)",
        capability="deep_question",
    )

    await _seed_session(
        store,
        session_id="fractions-low",
        capability="deep_question",
        message="Generate a fractions assessment",
        knowledge_bases=["fractions-pack"],
    )
    await store.add_message(
        "fractions-low",
        "user",
        "[Quiz Performance]\n"
        "1. [q1] Q: Solve fractions subtraction 3/4 - 1/2 -> Answered: 1/5 (Incorrect, correct: 1/4)\n"
        "Score: 0/1 (0%)",
        capability="deep_question",
    )

    await _seed_session(
        store,
        session_id="tutor-fractions",
        capability="chat",
        message="Tutor the student on fractions",
        knowledge_bases=["fractions-pack"],
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get(
            "/api/v1/dashboard/overview?type=assessment&knowledge_base=algebra-pack&search=algebra&min_score=80"
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["totals"]["total_sessions"] == 1
    assert payload["totals"]["assessments"] == 1
    assert payload["totals"]["tutoring_sessions"] == 0
    assert payload["knowledge_packs"] == [{"name": "algebra-pack", "session_count": 1}]
    assert [row["id"] for row in payload["recent_activity"]] == ["algebra-high"]


@pytest.mark.asyncio
async def test_dashboard_overview_includes_teacher_analytics_signals(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await _seed_session(
        store,
        session_id="assessment-latest",
        capability="deep_question",
        message="Generate a quiz on fractions",
        knowledge_bases=["fractions-pack"],
    )
    await store.add_message(
        "assessment-latest",
        "user",
        "[Quiz Performance]\n"
        "1. [q1] Q: Solve fractions subtraction 3/4 - 1/2 -> Answered: 1/5 (Incorrect, correct: 1/4)\n"
        "2. [q2] Q: Solve fractions addition 1/2 + 1/4 -> Answered: 3/4 (Correct)\n"
        "Score: 1/2 (50%)",
        capability="deep_question",
    )
    _set_session_timestamp(store, "assessment-latest", 1_710_000_000)

    await _seed_session(
        store,
        session_id="assessment-older",
        capability="deep_question",
        message="Generate a quiz on algebra",
        knowledge_bases=["algebra-pack"],
    )
    await store.add_message(
        "assessment-older",
        "user",
        "[Quiz Performance]\n"
        "1. [q1] Q: Solve algebra equation x + 2 = 5 -> Answered: 3 (Correct)\n"
        "2. [q2] Q: Solve algebra equation 2x = 10 -> Answered: 5 (Correct)\n"
        "Score: 2/2 (100%)",
        capability="deep_question",
    )
    _set_session_timestamp(store, "assessment-older", 1_709_913_600)

    await _seed_session(
        store,
        session_id="tutor-recent",
        capability="chat",
        message="Tutor the student on fraction mistakes",
        knowledge_bases=["fractions-pack"],
    )
    _set_session_timestamp(store, "tutor-recent", 1_709_827_200)

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/dashboard/overview")

    assert response.status_code == 200
    payload = response.json()
    assert payload["analytics"]["engagement"] == {
        "active_days": 3,
        "streak_days": 3,
        "knowledge_packs_used": 2,
    }
    assert payload["analytics"]["assessment_trend"] == {
        "assessments_completed": 2,
        "average_score_percent": 75,
        "latest_score_percent": 50,
        "score_delta": -50,
    }
    assert payload["analytics"]["learning_signals"]["focus_topics"][0]["topic"] == "fractions subtraction"
    assert payload["analytics"]["learning_signals"]["mastered_topics"][0]["topic"] == "algebra equation"


@pytest.mark.asyncio
async def test_dashboard_recent_tutoring_activity_includes_replay_ref(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await _seed_session(
        store,
        session_id="tutor-replay",
        capability="chat",
        message="Help me understand photosynthesis",
        knowledge_bases=["biology-pack"],
    )
    await store.add_message(
        "tutor-replay",
        "assistant",
        "Let's break photosynthesis into inputs, process, and outputs.",
        capability="chat",
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/dashboard/overview")

    assert response.status_code == 200
    payload = response.json()
    tutoring_row = next(row for row in payload["recent_activity"] if row["id"] == "tutor-replay")
    assert tutoring_row["type"] == "tutoring"
    assert tutoring_row["replay_ref"] == "dashboard/sessions/tutor-replay"


@pytest.mark.asyncio
async def test_dashboard_assessment_export_returns_pdf_report(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await _seed_session(
        store,
        session_id="export-session",
        capability="deep_question",
        message="Generate a quiz on geometry",
        knowledge_bases=["geometry-pack"],
    )
    await store.add_message(
        "export-session",
        "user",
        "[Quiz Performance]\n"
        "1. [q1] Q: What is the sum of angles in a triangle? -> Answered: 180 degrees (Correct)\n"
        "2. [q2] Q: How many sides does a pentagon have? -> Answered: 4 (Incorrect, correct: 5)\n"
        "Score: 1/2 (50%)",
        capability="deep_question",
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/dashboard/assessment-export/export-session")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment;" in response.headers["content-disposition"]
    assert response.content.startswith(b"%PDF")

    pdf = fitz.open(stream=response.content, filetype="pdf")
    text = "\n".join(page.get_text() for page in pdf)
    assert "Generate a quiz on geometry" in text
    assert "geometry-pack" in text
    assert "What is the sum of angles in a triangle?" in text
    assert "How many sides does a pentagon have?" in text
    assert "Score: 50%" in text
