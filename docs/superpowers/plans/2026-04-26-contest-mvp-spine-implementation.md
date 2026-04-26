# Contest MVP+ Spine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first working `Observed -> Inferred -> Recommended Action` spine on top of the current assessment, session, and dashboard stack.

**Architecture:** This plan only covers `Wave 1` from the approved spec because the full spec spans multiple independent subsystems. The implementation adds a small evidence service layer, persists observation and student-state summaries in SQLite, upgrades backend diagnosis/insight endpoints, and exposes the new signals on the existing teacher dashboard without attempting full spec authoring yet.

**Tech Stack:** Python, FastAPI, SQLite, pytest, Next.js, TypeScript, React, ESLint

---

## Scope Boundary

This plan intentionally covers only the first shippable subproject from the approved design:

- In scope: `Lane 3`, `Lane 4`, and the minimum viable dashboard surface from `Lane 5`
- Out of scope: full `Agent Spec Pack` authoring UI, runtime prompt assembly changes, marketplace exposure, and contest evidence refresh for later waves

Follow-on plans should be written separately for `Wave 2` and `Wave 3` after this spine lands.

## File Structure

### Backend evidence layer

- Create: `deeptutor/services/evidence/__init__.py`
  Exports the new evidence extraction, diagnosis, and teacher insight helpers.
- Create: `deeptutor/services/evidence/contracts.py`
  Defines the normalized observation, student-state, diagnosis, and recommendation shapes.
- Create: `deeptutor/services/evidence/extractor.py`
  Converts assessment review payloads into normalized observed signals.
- Create: `deeptutor/services/evidence/diagnosis.py`
  Implements the rule-first diagnosis and recommendation engine.
- Create: `deeptutor/services/evidence/teacher_insights.py`
  Aggregates per-student and small-group insights for the dashboard.

### Session persistence

- Modify: `deeptutor/services/session/sqlite_store.py`
  Adds SQLite tables and helpers for observations and student-state summaries.
- Modify: `deeptutor/services/session/__init__.py`
  Re-exports any new store helpers if needed by routers and services.

### API layer

- Modify: `deeptutor/api/routers/assessment.py`
  Adds a structured diagnosis endpoint while preserving the existing recommendation route.
- Modify: `deeptutor/api/routers/dashboard.py`
  Replaces the string-only insight endpoint with a structured teacher insight payload.

### Tests

- Create: `tests/services/evidence/test_extractor.py`
- Create: `tests/services/evidence/test_diagnosis.py`
- Modify: `tests/services/session/test_sqlite_store.py`
- Modify: `tests/api/test_assessment_router.py`
- Modify: `tests/api/test_dashboard_router.py`

### Frontend

- Create: `web/components/dashboard/TeacherInsightPanel.tsx`
  Renders per-student cards, grouped recommendations, and evidence trace summaries.
- Modify: `web/lib/dashboard-api.ts`
  Adds strong types for the new insight payload.
- Modify: `web/app/(workspace)/dashboard/page.tsx`
  Loads and renders the structured teacher insight panel.

## Task 1: Normalize Assessment Observations

**Files:**
- Create: `deeptutor/services/evidence/contracts.py`
- Create: `deeptutor/services/evidence/extractor.py`
- Create: `deeptutor/services/evidence/__init__.py`
- Test: `tests/services/evidence/test_extractor.py`

- [ ] **Step 1: Write the failing extractor tests**

```python
from deeptutor.services.evidence.extractor import extract_observations_from_review


def test_extract_observations_from_review_builds_topic_level_signals() -> None:
    review = {
        "session_id": "quiz-1",
        "student_id": "student-a",
        "results": [
            {
                "question_id": "q1",
                "question": "Solve fractions subtraction 3/4 - 1/2",
                "is_correct": False,
                "duration_seconds": 48,
            },
            {
                "question_id": "q2",
                "question": "Solve fractions subtraction 5/6 - 1/3",
                "is_correct": False,
                "duration_seconds": 61,
            },
        ],
    }

    rows = extract_observations_from_review(review)

    assert len(rows) == 2
    assert rows[0]["student_id"] == "student-a"
    assert rows[0]["topic"] == "fractions subtraction"
    assert rows[0]["source"] == "assessment"
    assert rows[0]["is_correct"] is False
    assert rows[0]["latency_seconds"] == 48


def test_extract_observations_from_review_marks_dominant_error_for_repeated_misses() -> None:
    review = {
        "session_id": "quiz-2",
        "student_id": "student-b",
        "results": [
            {
                "question_id": "q1",
                "question": "Solve algebra equation 2x = 10",
                "is_correct": False,
                "duration_seconds": 20,
            },
            {
                "question_id": "q2",
                "question": "Solve algebra equation x + 2 = 5",
                "is_correct": False,
                "duration_seconds": 18,
            },
        ],
    }

    rows = extract_observations_from_review(review)

    assert {row["dominant_error"] for row in rows} == {"concept_gap"}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/services/evidence/test_extractor.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'deeptutor.services.evidence'`

- [ ] **Step 3: Write the contracts and extractor**

```python
# deeptutor/services/evidence/contracts.py
from __future__ import annotations

from typing import Literal, TypedDict


ObservationSource = Literal["assessment", "tutoring"]
DiagnosisType = Literal["concept_gap", "careless_error", "low_confidence", "needs_scaffold"]


class ObservationRecord(TypedDict):
    observation_id: str
    session_id: str
    student_id: str
    source: ObservationSource
    topic: str
    question_id: str
    is_correct: bool
    latency_seconds: int | None
    hint_count: int
    retry_count: int
    dominant_error: DiagnosisType | None


class StudentStateRecord(TypedDict):
    student_id: str
    repeated_mistakes: list[str]
    support_level: Literal["independent", "guided", "intensive"]
    confidence_trend: Literal["up", "flat", "down"]


class DiagnosisRecord(TypedDict):
    diagnosis_type: DiagnosisType
    confidence_tag: Literal["low", "medium", "high"]
    topic: str
    evidence: list[str]


class RecommendationRecord(TypedDict):
    action_id: str
    action_type: Literal["review_prerequisite", "retry_easier", "increase_scaffold", "small_group_support"]
    target_student_ids: list[str]
    topic: str
    rationale: str
```

```python
# deeptutor/services/evidence/extractor.py
from __future__ import annotations

import uuid
from typing import Any

from deeptutor.services.assessment.analysis import infer_topic_from_question

from .contracts import ObservationRecord


def _dominant_error(result: dict[str, Any], repeated_topic_misses: int) -> str | None:
    if bool(result.get("is_correct")):
        return None
    duration = int(result.get("duration_seconds") or 0)
    if repeated_topic_misses >= 2:
        return "concept_gap"
    if duration <= 15:
        return "careless_error"
    return "needs_scaffold"


def extract_observations_from_review(review: dict[str, Any]) -> list[ObservationRecord]:
    results = review.get("results") if isinstance(review.get("results"), list) else []
    topic_miss_counts: dict[str, int] = {}
    for item in results:
        topic = infer_topic_from_question(str(item.get("question") or ""), fallback="general")
        if not bool(item.get("is_correct")):
            topic_miss_counts[topic] = topic_miss_counts.get(topic, 0) + 1

    rows: list[ObservationRecord] = []
    for item in results:
        topic = infer_topic_from_question(str(item.get("question") or ""), fallback="general")
        rows.append(
            {
                "observation_id": f"obs_{uuid.uuid4().hex[:12]}",
                "session_id": str(review.get("session_id") or ""),
                "student_id": str(review.get("student_id") or review.get("session_id") or "unknown"),
                "source": "assessment",
                "topic": topic,
                "question_id": str(item.get("question_id") or ""),
                "is_correct": bool(item.get("is_correct")),
                "latency_seconds": int(item.get("duration_seconds")) if item.get("duration_seconds") else None,
                "hint_count": int(item.get("hint_count") or 0),
                "retry_count": int(item.get("retry_count") or 0),
                "dominant_error": _dominant_error(item, topic_miss_counts.get(topic, 0)),
            }
        )
    return rows
```

```python
# deeptutor/services/evidence/__init__.py
from .extractor import extract_observations_from_review

__all__ = [
    "extract_observations_from_review",
]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/services/evidence/test_extractor.py -v`
Expected: PASS with `2 passed`

- [ ] **Step 5: Commit**

```bash
git add tests/services/evidence/test_extractor.py deeptutor/services/evidence/__init__.py deeptutor/services/evidence/contracts.py deeptutor/services/evidence/extractor.py
git commit -m "feat: add evidence observation extraction"
```

## Task 2: Persist Observations and Student State in SQLite

**Files:**
- Modify: `deeptutor/services/session/sqlite_store.py`
- Modify: `tests/services/session/test_sqlite_store.py`

- [ ] **Step 1: Write the failing SQLite store test**

```python
import pytest

from deeptutor.services.session.sqlite_store import SQLiteSessionStore


@pytest.mark.asyncio
async def test_sqlite_store_persists_observations_and_student_state(tmp_path) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")

    await store.save_observations(
        [
            {
                "observation_id": "obs_1",
                "session_id": "quiz-1",
                "student_id": "student-a",
                "source": "assessment",
                "topic": "fractions subtraction",
                "question_id": "q1",
                "is_correct": False,
                "latency_seconds": 48,
                "hint_count": 0,
                "retry_count": 1,
                "dominant_error": "concept_gap",
            }
        ]
    )
    await store.upsert_student_state(
        "student-a",
        {
            "student_id": "student-a",
            "repeated_mistakes": ["fractions subtraction"],
            "support_level": "guided",
            "confidence_trend": "down",
        },
    )

    observations = await store.list_observations(student_id="student-a")
    state = await store.get_student_state("student-a")

    assert len(observations) == 1
    assert observations[0]["topic"] == "fractions subtraction"
    assert state["support_level"] == "guided"
    assert state["confidence_trend"] == "down"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/services/session/test_sqlite_store.py::test_sqlite_store_persists_observations_and_student_state -v`
Expected: FAIL with `AttributeError: 'SQLiteSessionStore' object has no attribute 'save_observations'`

- [ ] **Step 3: Add the schema migration and store helpers**

```python
# sqlite_store.py - inside _initialize()
conn.executescript(
    """
    CREATE TABLE IF NOT EXISTS observations (
        observation_id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        student_id TEXT NOT NULL,
        source TEXT NOT NULL,
        topic TEXT NOT NULL,
        question_id TEXT DEFAULT '',
        is_correct INTEGER NOT NULL,
        latency_seconds INTEGER,
        hint_count INTEGER NOT NULL DEFAULT 0,
        retry_count INTEGER NOT NULL DEFAULT 0,
        dominant_error TEXT DEFAULT '',
        created_at REAL NOT NULL DEFAULT (strftime('%s', 'now'))
    );

    CREATE INDEX IF NOT EXISTS idx_observations_student_created
        ON observations(student_id, created_at DESC);

    CREATE TABLE IF NOT EXISTS student_states (
        student_id TEXT PRIMARY KEY,
        repeated_mistakes_json TEXT NOT NULL DEFAULT '[]',
        support_level TEXT NOT NULL DEFAULT 'independent',
        confidence_trend TEXT NOT NULL DEFAULT 'flat',
        updated_at REAL NOT NULL
    );
    """
)
```

```python
# sqlite_store.py - add new methods
def _save_observations_sync(self, observations: list[dict[str, Any]]) -> None:
    now = time.time()
    with self._connect() as conn:
        conn.executemany(
            """
            INSERT OR REPLACE INTO observations (
                observation_id, session_id, student_id, source, topic, question_id,
                is_correct, latency_seconds, hint_count, retry_count, dominant_error, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    row["observation_id"],
                    row["session_id"],
                    row["student_id"],
                    row["source"],
                    row["topic"],
                    row["question_id"],
                    1 if row["is_correct"] else 0,
                    row["latency_seconds"],
                    row["hint_count"],
                    row["retry_count"],
                    row["dominant_error"] or "",
                    now,
                )
                for row in observations
            ],
        )
        conn.commit()


async def save_observations(self, observations: list[dict[str, Any]]) -> None:
    await self._run(self._save_observations_sync, observations)


def _upsert_student_state_sync(self, student_id: str, state: dict[str, Any]) -> None:
    now = time.time()
    with self._connect() as conn:
        conn.execute(
            """
            INSERT INTO student_states (
                student_id, repeated_mistakes_json, support_level, confidence_trend, updated_at
            ) VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(student_id) DO UPDATE SET
                repeated_mistakes_json = excluded.repeated_mistakes_json,
                support_level = excluded.support_level,
                confidence_trend = excluded.confidence_trend,
                updated_at = excluded.updated_at
            """,
            (
                student_id,
                _json_dumps(state.get("repeated_mistakes", [])),
                state.get("support_level", "independent"),
                state.get("confidence_trend", "flat"),
                now,
            ),
        )
        conn.commit()
```

```python
# sqlite_store.py - add readers
async def upsert_student_state(self, student_id: str, state: dict[str, Any]) -> None:
    await self._run(self._upsert_student_state_sync, student_id, state)


def _get_student_state_sync(self, student_id: str) -> dict[str, Any] | None:
    with self._connect() as conn:
        row = conn.execute(
            """
            SELECT student_id, repeated_mistakes_json, support_level, confidence_trend, updated_at
            FROM student_states
            WHERE student_id = ?
            """,
            (student_id,),
        ).fetchone()
    if row is None:
        return None
    return {
        "student_id": row["student_id"],
        "repeated_mistakes": _json_loads(row["repeated_mistakes_json"], []),
        "support_level": row["support_level"],
        "confidence_trend": row["confidence_trend"],
        "updated_at": row["updated_at"],
    }


async def get_student_state(self, student_id: str) -> dict[str, Any] | None:
    return await self._run(self._get_student_state_sync, student_id)


def _list_observations_sync(self, student_id: str) -> list[dict[str, Any]]:
    with self._connect() as conn:
        rows = conn.execute(
            """
            SELECT observation_id, session_id, student_id, source, topic, question_id, is_correct,
                   latency_seconds, hint_count, retry_count, dominant_error
            FROM observations
            WHERE student_id = ?
            ORDER BY created_at DESC
            """,
            (student_id,),
        ).fetchall()
    return [
        {
            "observation_id": row["observation_id"],
            "session_id": row["session_id"],
            "student_id": row["student_id"],
            "source": row["source"],
            "topic": row["topic"],
            "question_id": row["question_id"],
            "is_correct": bool(row["is_correct"]),
            "latency_seconds": row["latency_seconds"],
            "hint_count": row["hint_count"],
            "retry_count": row["retry_count"],
            "dominant_error": row["dominant_error"] or None,
        }
        for row in rows
    ]


async def list_observations(self, student_id: str) -> list[dict[str, Any]]:
    return await self._run(self._list_observations_sync, student_id)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/services/session/test_sqlite_store.py::test_sqlite_store_persists_observations_and_student_state -v`
Expected: PASS with `1 passed`

- [ ] **Step 5: Commit**

```bash
git add deeptutor/services/session/sqlite_store.py tests/services/session/test_sqlite_store.py
git commit -m "feat: persist evidence observations and student state"
```

## Task 3: Add Rule-First Diagnosis and Structured Assessment Output

**Files:**
- Create: `deeptutor/services/evidence/diagnosis.py`
- Create: `tests/services/evidence/test_diagnosis.py`
- Modify: `deeptutor/api/routers/assessment.py`
- Modify: `tests/api/test_assessment_router.py`

- [ ] **Step 1: Write the failing diagnosis tests**

```python
from deeptutor.services.evidence.diagnosis import build_student_diagnosis


def test_build_student_diagnosis_returns_structured_hypotheses_and_actions() -> None:
    observations = [
        {
            "observation_id": "obs_1",
            "session_id": "quiz-1",
            "student_id": "student-a",
            "source": "assessment",
            "topic": "fractions subtraction",
            "question_id": "q1",
            "is_correct": False,
            "latency_seconds": 48,
            "hint_count": 0,
            "retry_count": 1,
            "dominant_error": "concept_gap",
        },
        {
            "observation_id": "obs_2",
            "session_id": "quiz-1",
            "student_id": "student-a",
            "source": "assessment",
            "topic": "fractions subtraction",
            "question_id": "q2",
            "is_correct": False,
            "latency_seconds": 61,
            "hint_count": 0,
            "retry_count": 1,
            "dominant_error": "concept_gap",
        },
    ]
    state = {
        "student_id": "student-a",
        "repeated_mistakes": ["fractions subtraction"],
        "support_level": "guided",
        "confidence_trend": "down",
    }

    payload = build_student_diagnosis(student_id="student-a", observations=observations, student_state=state)

    assert payload["student_id"] == "student-a"
    assert payload["observed"]["topic"] == "fractions subtraction"
    assert payload["inferred"][0]["diagnosis_type"] == "concept_gap"
    assert payload["recommended_actions"][0]["action_type"] == "review_prerequisite"
```

```python
@pytest.mark.asyncio
async def test_assessment_diagnosis_endpoint_returns_structured_payload(tmp_path, monkeypatch) -> None:
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
        "[Quiz Performance]\\n"
        "1. [q1] Q: Solve fractions subtraction 3/4 - 1/2 -> Answered: 1/5 (Incorrect, correct: 1/4, time: 48s)\\n"
        "2. [q2] Q: Solve fractions subtraction 5/6 - 1/3 -> Answered: 1/6 (Incorrect, correct: 1/2, time: 61s)\\n"
        "Score: 0/2 (0%)",
        capability="deep_question",
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/assessment/diagnosis/assessment-recent")

    assert response.status_code == 200
    payload = response.json()
    assert payload["student_id"] == "assessment-recent"
    assert payload["inferred"][0]["diagnosis_type"] == "concept_gap"
    assert payload["recommended_actions"][0]["topic"] == "fractions subtraction"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/services/evidence/test_diagnosis.py tests/api/test_assessment_router.py::test_assessment_diagnosis_endpoint_returns_structured_payload -v`
Expected: FAIL with `ModuleNotFoundError` for `deeptutor.services.evidence.diagnosis` and `404` for the missing route

- [ ] **Step 3: Implement the diagnosis service and endpoint**

```python
# deeptutor/services/evidence/diagnosis.py
from __future__ import annotations

from collections import Counter
from typing import Any


def _confidence_tag(observations: list[dict[str, Any]]) -> str:
    if len(observations) >= 3:
        return "high"
    if len(observations) == 2:
        return "medium"
    return "low"


def _support_level(observations: list[dict[str, Any]]) -> str:
    if any((row.get("hint_count") or 0) >= 2 for row in observations):
        return "intensive"
    if any(not row.get("is_correct") for row in observations):
        return "guided"
    return "independent"


def build_student_diagnosis(
    *,
    student_id: str,
    observations: list[dict[str, Any]],
    student_state: dict[str, Any] | None,
) -> dict[str, Any]:
    if not observations:
        return {
            "student_id": student_id,
            "observed": None,
            "inferred": [],
            "recommended_actions": [],
        }

    topic_counter = Counter(row["topic"] for row in observations if not row.get("is_correct"))
    dominant_topic, _ = topic_counter.most_common(1)[0]
    dominant_rows = [row for row in observations if row["topic"] == dominant_topic]
    dominant_error = Counter(
        row["dominant_error"] for row in dominant_rows if row.get("dominant_error")
    ).most_common(1)[0][0]
    confidence = _confidence_tag(dominant_rows)

    diagnosis = {
        "diagnosis_type": dominant_error,
        "confidence_tag": confidence,
        "topic": dominant_topic,
        "evidence": [
            f"{len(dominant_rows)} missed question(s) in {dominant_topic}",
            f"support_level={_support_level(dominant_rows)}",
        ],
    }
    recommendation_type = "review_prerequisite" if dominant_error == "concept_gap" else "increase_scaffold"
    recommendation = {
        "action_id": f"{student_id}:{dominant_topic}:{recommendation_type}",
        "action_type": recommendation_type,
        "target_student_ids": [student_id],
        "topic": dominant_topic,
        "rationale": f"Revisit {dominant_topic} before moving to mixed practice.",
    }
    return {
        "student_id": student_id,
        "observed": {
            "topic": dominant_topic,
            "miss_count": len(dominant_rows),
            "avg_latency_seconds": round(
                sum(int(row.get('latency_seconds') or 0) for row in dominant_rows) / len(dominant_rows)
            ),
        },
        "student_state": student_state or {
            "student_id": student_id,
            "repeated_mistakes": [dominant_topic],
            "support_level": _support_level(dominant_rows),
            "confidence_trend": "down",
        },
        "inferred": [diagnosis],
        "recommended_actions": [recommendation],
    }
```

```python
# assessment.py
from deeptutor.services.evidence.diagnosis import build_student_diagnosis
from deeptutor.services.evidence.extractor import extract_observations_from_review


@router.get("/diagnosis/{session_id}")
async def get_assessment_diagnosis(session_id: str):
    store = get_sqlite_session_store()
    detail = await store.get_session_with_messages(session_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Assessment session not found")

    review = extract_assessment_review(detail)
    if review is None:
        raise HTTPException(status_code=404, detail="Assessment review not found")

    review["student_id"] = str((detail.get("preferences") or {}).get("student_id") or session_id)
    observations = extract_observations_from_review(review)
    await store.save_observations(observations)

    student_id = review["student_id"]
    state = {
        "student_id": student_id,
        "repeated_mistakes": sorted({row["topic"] for row in observations if not row["is_correct"]}),
        "support_level": "guided" if any(not row["is_correct"] for row in observations) else "independent",
        "confidence_trend": "down" if any(not row["is_correct"] for row in observations) else "flat",
    }
    await store.upsert_student_state(student_id, state)

    return build_student_diagnosis(
        student_id=student_id,
        observations=observations,
        student_state=await store.get_student_state(student_id),
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/services/evidence/test_diagnosis.py tests/api/test_assessment_router.py::test_assessment_diagnosis_endpoint_returns_structured_payload -v`
Expected: PASS with `2 passed`

- [ ] **Step 5: Commit**

```bash
git add deeptutor/services/evidence/diagnosis.py deeptutor/api/routers/assessment.py tests/services/evidence/test_diagnosis.py tests/api/test_assessment_router.py
git commit -m "feat: add structured assessment diagnosis endpoint"
```

## Task 4: Aggregate Teacher Insights and Small-Group Recommendations

**Files:**
- Create: `deeptutor/services/evidence/teacher_insights.py`
- Modify: `deeptutor/api/routers/dashboard.py`
- Modify: `tests/api/test_dashboard_router.py`

- [ ] **Step 1: Write the failing dashboard insight test**

```python
@pytest.mark.asyncio
async def test_dashboard_insights_returns_students_and_small_groups(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await _seed_session(
        store,
        session_id="student-a-session",
        capability="deep_question",
        message="Generate a quiz on fractions",
        knowledge_bases=["fractions-pack"],
    )
    await store.update_session_preferences(
        "student-a-session",
        {"student_id": "student-a", "knowledge_bases": ["fractions-pack"], "capability": "deep_question"},
    )
    await store.add_message(
        "student-a-session",
        "user",
        "[Quiz Performance]\\n"
        "1. [q1] Q: Solve fractions subtraction 3/4 - 1/2 -> Answered: 1/5 (Incorrect, correct: 1/4, time: 48s)\\n"
        "Score: 0/1 (0%)",
        capability="deep_question",
    )

    await _seed_session(
        store,
        session_id="student-b-session",
        capability="deep_question",
        message="Generate a quiz on fractions",
        knowledge_bases=["fractions-pack"],
    )
    await store.update_session_preferences(
        "student-b-session",
        {"student_id": "student-b", "knowledge_bases": ["fractions-pack"], "capability": "deep_question"},
    )
    await store.add_message(
        "student-b-session",
        "user",
        "[Quiz Performance]\\n"
        "1. [q1] Q: Solve fractions subtraction 5/6 - 1/3 -> Answered: 1/6 (Incorrect, correct: 1/2, time: 52s)\\n"
        "Score: 0/1 (0%)",
        capability="deep_question",
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/dashboard/insights")

    assert response.status_code == 200
    payload = response.json()
    assert payload["students"][0]["student_id"] in {"student-a", "student-b"}
    assert payload["small_groups"][0]["topic"] == "fractions subtraction"
    assert sorted(payload["small_groups"][0]["student_ids"]) == ["student-a", "student-b"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/api/test_dashboard_router.py::test_dashboard_insights_returns_students_and_small_groups -v`
Expected: FAIL because `/api/v1/dashboard/insights` does not yet return `students` or `small_groups`

- [ ] **Step 3: Implement the teacher insight aggregator and router wiring**

```python
# deeptutor/services/evidence/teacher_insights.py
from __future__ import annotations

from collections import defaultdict
from typing import Any

from .diagnosis import build_student_diagnosis


def build_teacher_insights_payload(
    *,
    student_payloads: list[dict[str, Any]],
) -> dict[str, Any]:
    grouped: dict[tuple[str, str], list[str]] = defaultdict(list)
    for payload in student_payloads:
        inferred = payload.get("inferred") or []
        if not inferred:
            continue
        key = (inferred[0]["topic"], inferred[0]["diagnosis_type"])
        grouped[key].append(payload["student_id"])

    small_groups = [
        {
            "topic": topic,
            "diagnosis_type": diagnosis_type,
            "student_ids": sorted(student_ids),
            "recommended_action": "small_group_support",
        }
        for (topic, diagnosis_type), student_ids in grouped.items()
        if len(student_ids) >= 2
    ]

    return {
        "students": student_payloads,
        "small_groups": small_groups,
    }
```

```python
# dashboard.py
from deeptutor.services.evidence.diagnosis import build_student_diagnosis
from deeptutor.services.evidence.extractor import extract_observations_from_review
from deeptutor.services.evidence.teacher_insights import build_teacher_insights_payload


@router.get("/insights")
async def get_dashboard_insights(
    limit: int = 100,
    knowledge_base: str | None = None,
    cohort: str | None = None,
    start_ts: int | None = None,
    end_ts: int | None = None,
):
    store = get_sqlite_session_store()
    sessions = await store.list_sessions(limit=limit, offset=0)
    student_payloads: list[dict[str, Any]] = []

    for session in sessions:
        activity = await _activity_with_review(store, session)
        if activity["type"] != "assessment":
            continue
        if not _matches_dashboard_filters(activity, knowledge_base=knowledge_base, cohort=cohort):
            continue
        ts = activity.get("timestamp") or 0
        if start_ts is not None and ts < start_ts:
            continue
        if end_ts is not None and ts > end_ts:
            continue

        detail = await store.get_session_with_messages(activity["id"])
        review = extract_assessment_review(detail) if detail else None
        if review is None:
            continue
        student_id = str((detail.get("preferences") or {}).get("student_id") or activity["id"])
        review["student_id"] = student_id
        observations = extract_observations_from_review(review)
        await store.save_observations(observations)
        state = await store.get_student_state(student_id)
        if state is None:
            state = {
                "student_id": student_id,
                "repeated_mistakes": sorted({row["topic"] for row in observations if not row["is_correct"]}),
                "support_level": "guided" if any(not row["is_correct"] for row in observations) else "independent",
                "confidence_trend": "down" if any(not row["is_correct"] for row in observations) else "flat",
            }
            await store.upsert_student_state(student_id, state)

        student_payloads.append(
            build_student_diagnosis(
                student_id=student_id,
                observations=observations,
                student_state=state,
            )
        )

    return build_teacher_insights_payload(student_payloads=student_payloads)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/api/test_dashboard_router.py::test_dashboard_insights_returns_students_and_small_groups -v`
Expected: PASS with `1 passed`

- [ ] **Step 5: Commit**

```bash
git add deeptutor/services/evidence/teacher_insights.py deeptutor/api/routers/dashboard.py tests/api/test_dashboard_router.py
git commit -m "feat: add structured teacher insights aggregation"
```

## Task 5: Render Structured Teacher Insights on the Dashboard

**Files:**
- Create: `web/components/dashboard/TeacherInsightPanel.tsx`
- Modify: `web/lib/dashboard-api.ts`
- Modify: `web/app/(workspace)/dashboard/page.tsx`

- [ ] **Step 1: Write the failing frontend type integration**

```ts
export interface TeacherInsightStudent {
  student_id: string;
  observed: {
    topic: string;
    miss_count: number;
    avg_latency_seconds: number;
  } | null;
  inferred: Array<{
    diagnosis_type: string;
    confidence_tag: string;
    topic: string;
    evidence: string[];
  }>;
  recommended_actions: Array<{
    action_id: string;
    action_type: string;
    target_student_ids: string[];
    topic: string;
    rationale: string;
  }>;
}

export interface DashboardInsights {
  students: TeacherInsightStudent[];
  small_groups: Array<{
    topic: string;
    diagnosis_type: string;
    student_ids: string[];
    recommended_action: string;
  }>;
}
```

Run: `cd web && npm run lint`
Expected: FAIL because `getDashboardInsights()` still returns the old analytics-only shape and the dashboard page does not use the new payload

- [ ] **Step 2: Add the API types and fetch helper**

```ts
// web/lib/dashboard-api.ts
export interface TeacherInsightStudent {
  student_id: string;
  observed: {
    topic: string;
    miss_count: number;
    avg_latency_seconds: number;
  } | null;
  student_state?: {
    support_level: string;
    confidence_trend: string;
  } | null;
  inferred: Array<{
    diagnosis_type: string;
    confidence_tag: string;
    topic: string;
    evidence: string[];
  }>;
  recommended_actions: Array<{
    action_id: string;
    action_type: string;
    target_student_ids: string[];
    topic: string;
    rationale: string;
  }>;
}

export interface DashboardInsights {
  students: TeacherInsightStudent[];
  small_groups: Array<{
    topic: string;
    diagnosis_type: string;
    student_ids: string[];
    recommended_action: string;
  }>;
}
```

- [ ] **Step 3: Create the dashboard insight panel**

```tsx
// web/components/dashboard/TeacherInsightPanel.tsx
import type { DashboardInsights } from "@/lib/dashboard-api";

export function TeacherInsightPanel({
  insights,
}: {
  insights: DashboardInsights | null;
}) {
  if (!insights || (insights.students.length === 0 && insights.small_groups.length === 0)) {
    return (
      <section className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-5">
        <h2 className="text-[16px] font-semibold text-[var(--foreground)]">Teacher insights</h2>
        <p className="mt-2 text-[13px] text-[var(--muted-foreground)]">
          No structured evidence yet. Complete at least one assessment to unlock diagnosis and next-step actions.
        </p>
      </section>
    );
  }

  return (
    <section className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-5">
      <h2 className="text-[16px] font-semibold text-[var(--foreground)]">Teacher insights</h2>
      <div className="mt-4 grid gap-4 lg:grid-cols-2">
        <div className="space-y-3">
          {insights.students.map((student) => (
            <article key={student.student_id} className="rounded-2xl bg-[var(--muted)]/50 p-4">
              <div className="text-[12px] font-semibold uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
                {student.student_id}
              </div>
              <div className="mt-2 text-[14px] font-medium text-[var(--foreground)]">
                {student.observed?.topic ?? "No dominant topic"}
              </div>
              <div className="mt-1 text-[12px] text-[var(--muted-foreground)]">
                {student.inferred[0]?.diagnosis_type ?? "No diagnosis"} · {student.inferred[0]?.confidence_tag ?? "n/a"} confidence
              </div>
              <div className="mt-3 text-[13px] text-[var(--foreground)]">
                {student.recommended_actions[0]?.rationale ?? "No recommendation"}
              </div>
            </article>
          ))}
        </div>
        <div className="space-y-3">
          {insights.small_groups.map((group) => (
            <article key={`${group.topic}:${group.diagnosis_type}`} className="rounded-2xl bg-[var(--muted)]/50 p-4">
              <div className="text-[14px] font-medium text-[var(--foreground)]">{group.topic}</div>
              <div className="mt-1 text-[12px] text-[var(--muted-foreground)]">
                {group.diagnosis_type} · {group.student_ids.join(", ")}
              </div>
              <div className="mt-3 text-[13px] text-[var(--foreground)]">
                Recommended action: {group.recommended_action}
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
```

- [ ] **Step 4: Wire the dashboard page to the new endpoint and verify lint**

```tsx
// dashboard/page.tsx
import { TeacherInsightPanel } from "@/components/dashboard/TeacherInsightPanel";
import {
  getDashboardInsights,
  getDashboardOverview,
  type DashboardInsights,
  type DashboardOverview,
  type DashboardOverviewFilters,
} from "@/lib/dashboard-api";

const [insights, setInsights] = useState<DashboardInsights | null>(null);

useEffect(() => {
  let cancelled = false;
  Promise.all([getDashboardOverview(50, filters), getDashboardInsights(50, { knowledge_base: filters.knowledge_base })])
    .then(([overviewData, insightsData]) => {
      if (!cancelled) {
        setOverview(overviewData);
        setInsights(insightsData);
        setError(null);
      }
    })
    .catch((err) => {
      if (!cancelled) setError(err instanceof Error ? err.message : String(err));
    })
    .finally(() => {
      if (!cancelled) setLoading(false);
    });
  return () => {
    cancelled = true;
  };
}, [filters]);
```

```tsx
<TeacherInsightPanel insights={insights} />
```

Run: `cd web && npm run lint`
Expected: PASS with no ESLint errors

- [ ] **Step 5: Commit**

```bash
git add web/lib/dashboard-api.ts web/components/dashboard/TeacherInsightPanel.tsx 'web/app/(workspace)/dashboard/page.tsx'
git commit -m "feat: surface structured teacher insights on dashboard"
```

## Task 6: End-to-End Verification and Handoff

**Files:**
- Modify: `ai_first/daily/2026-04-26.md`
- Create: `docs/superpowers/pr-notes/2026-04-26-wave-1-evidence-spine.md`

- [ ] **Step 1: Run the backend test slice**

Run: `pytest tests/services/evidence/test_extractor.py tests/services/evidence/test_diagnosis.py tests/services/session/test_sqlite_store.py tests/api/test_assessment_router.py tests/api/test_dashboard_router.py -v`
Expected: PASS with all new evidence, assessment, session, and dashboard tests green

- [ ] **Step 2: Run the frontend verification**

Run: `cd web && npm run lint`
Expected: PASS with no ESLint errors

- [ ] **Step 3: Run a manual API smoke check**

Run:

```bash
python - <<'PY'
from fastapi.testclient import TestClient
from deeptutor.api.main import app

with TestClient(app) as client:
    response = client.get("/api/v1/dashboard/insights")
    print(response.status_code)
PY
```

Expected: `200` in a seeded environment, or `200` with an empty `students` list in a clean environment

- [ ] **Step 4: Update the daily log and PR note**

```md
- Done: Implemented Wave 1 evidence spine with observation capture, student-state persistence, structured diagnosis, and teacher dashboard insights.
- Tests: pytest tests/services/evidence/test_extractor.py tests/services/evidence/test_diagnosis.py tests/services/session/test_sqlite_store.py tests/api/test_assessment_router.py tests/api/test_dashboard_router.py -v; cd web && npm run lint
```

- [ ] **Step 5: Commit**

```bash
git add ai_first/daily/2026-04-26.md docs/superpowers/pr-notes/2026-04-26-wave-1-evidence-spine.md
git commit -m "docs: record wave 1 evidence spine validation"
```

## Self-Review Notes

- Spec coverage for this plan:
  - `Lane 3` covered by Tasks 1-2
  - `Lane 4` covered by Tasks 3-4
  - minimum `Lane 5` surface covered by Task 5
- Deferred to later plans:
  - `Lane 1` agent spec authoring
  - deeper `Lane 2` runtime policy assembly
  - `Lane 6` contest evidence refresh beyond local verification
