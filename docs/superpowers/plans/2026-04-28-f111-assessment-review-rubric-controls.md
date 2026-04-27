# F111 Assessment Review Rubric Controls Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a persisted teacher-review rubric to the existing assessment review flow so teachers can record structured quality judgments before reuse.

**Architecture:** Extend the existing session review API with a bounded `teacher_review` record keyed by `session_id`, then surface that record on the current assessment review page with a compact rubric editor and summary. Keep the feature isolated to the assessment review route and avoid opening any publish or dashboard workflow.

**Tech Stack:** FastAPI, Pydantic, SQLite session store helpers, Next.js App Router, React client state, pytest

---

### Task 1: Add failing API tests for rubric review persistence

**Files:**
- Modify: `tests/api/test_session_review_router.py`
- Read: `deeptutor/api/routers/sessions.py`

- [ ] **Step 1: Write the failing create/reload test**

```python
@pytest.mark.asyncio
async def test_assessment_review_supports_teacher_rubric_review(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await store.create_session(session_id="quiz-rubric-session")
    await store.add_message(
        "quiz-rubric-session",
        "user",
        "[Quiz Performance]\n1. [q1] Q: 2+2 -> Answered: 3 (Incorrect, correct: 4)\nScore: 0/1 (0%)",
        capability="deep_question",
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        create_response = client.post(
            "/api/v1/sessions/quiz-rubric-session/assessment-rubric-review",
            json={
                "wording_quality": "acceptable",
                "distractor_quality": "weak",
                "explanation_clarity": "strong",
                "overall_decision": "needs_edit_before_reuse",
                "teacher_note": "Distractors are too easy to eliminate.",
            },
        )
        review_response = client.get("/api/v1/sessions/quiz-rubric-session/assessment-review")

    assert create_response.status_code == 200
    payload = review_response.json()
    assert payload["teacher_review"]["overall_decision"] == "needs_edit_before_reuse"
    assert payload["teacher_review"]["distractor_quality"] == "weak"
```

- [ ] **Step 2: Write the failing update test**

```python
@pytest.mark.asyncio
async def test_assessment_rubric_review_can_be_updated(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await store.create_session(session_id="quiz-rubric-update-session")
    await store.add_message(
        "quiz-rubric-update-session",
        "user",
        "[Quiz Performance]\n1. [q1] Q: 2+2 -> Answered: 3 (Incorrect, correct: 4)\nScore: 0/1 (0%)",
        capability="deep_question",
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        client.post(
            "/api/v1/sessions/quiz-rubric-update-session/assessment-rubric-review",
            json={
                "wording_quality": "acceptable",
                "distractor_quality": "acceptable",
                "explanation_clarity": "acceptable",
                "overall_decision": "needs_edit_before_reuse",
                "teacher_note": "",
            },
        )
        patch_response = client.patch(
            "/api/v1/sessions/quiz-rubric-update-session/assessment-rubric-review",
            json={
                "wording_quality": "strong",
                "distractor_quality": "acceptable",
                "explanation_clarity": "strong",
                "overall_decision": "approved_for_reuse",
                "teacher_note": "Ready after wording cleanup.",
            },
        )

    assert patch_response.status_code == 200
    assert patch_response.json()["overall_decision"] == "approved_for_reuse"
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `pytest tests/api/test_session_review_router.py -k "rubric_review" -q`

Expected: FAIL because the rubric endpoints and `teacher_review` payload do not exist yet.

- [ ] **Step 4: Commit the failing tests**

```bash
git add tests/api/test_session_review_router.py
git commit -m "test(sessions): add failing rubric review coverage [F111]"
```

### Task 2: Implement bounded rubric review storage and API

**Files:**
- Create: `deeptutor/services/session/assessment_review_rubric.py`
- Modify: `deeptutor/api/routers/sessions.py`
- Test: `tests/api/test_session_review_router.py`

- [ ] **Step 1: Add a tiny persistence helper**

```python
from __future__ import annotations

import json
import sqlite3
import time
import uuid
from pathlib import Path


def _ensure_table(db_path: Path) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS assessment_rubric_reviews (
                session_id TEXT PRIMARY KEY,
                payload_json TEXT NOT NULL
            )
            """
        )
        conn.commit()
```

- [ ] **Step 2: Add create/get/update helpers**

```python
def upsert_review(db_path: Path, session_id: str, payload: dict[str, object]) -> dict[str, object]:
    _ensure_table(db_path)
    now = int(time.time())
    record = {
        "id": payload.get("id") or str(uuid.uuid4()),
        "session_id": session_id,
        "wording_quality": payload["wording_quality"],
        "distractor_quality": payload["distractor_quality"],
        "explanation_clarity": payload["explanation_clarity"],
        "overall_decision": payload["overall_decision"],
        "teacher_note": payload.get("teacher_note", ""),
        "created_at": payload.get("created_at", now),
        "updated_at": now,
    }
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "REPLACE INTO assessment_rubric_reviews (session_id, payload_json) VALUES (?, ?)",
            (session_id, json.dumps(record)),
        )
        conn.commit()
    return record
```

- [ ] **Step 3: Extend the session router models and endpoints**

```python
class AssessmentRubricLevel(str, Enum):
    strong = "strong"
    acceptable = "acceptable"
    weak = "weak"


class AssessmentRubricDecision(str, Enum):
    approved_for_reuse = "approved_for_reuse"
    needs_edit_before_reuse = "needs_edit_before_reuse"
    not_ready = "not_ready"
```

Add:
- `TeacherAssessmentReviewRequest`
- `POST /{session_id}/assessment-rubric-review`
- `PATCH /{session_id}/assessment-rubric-review`
- include `teacher_review` in `get_assessment_review(...)`

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/api/test_session_review_router.py -k "rubric_review or assessment_review" -q`

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add deeptutor/services/session/assessment_review_rubric.py deeptutor/api/routers/sessions.py tests/api/test_session_review_router.py
git commit -m "feat(sessions): add assessment rubric review API [F111]"
```

### Task 3: Extend the frontend API contract

**Files:**
- Modify: `web/lib/dashboard-api.ts`

- [ ] **Step 1: Add teacher-review types**

```ts
export type AssessmentRubricLevel = "strong" | "acceptable" | "weak";
export type AssessmentRubricDecision =
  | "approved_for_reuse"
  | "needs_edit_before_reuse"
  | "not_ready";

export interface TeacherAssessmentReviewRecord {
  id: string;
  session_id: string;
  wording_quality: AssessmentRubricLevel;
  distractor_quality: AssessmentRubricLevel;
  explanation_clarity: AssessmentRubricLevel;
  overall_decision: AssessmentRubricDecision;
  teacher_note: string;
  created_at: number;
  updated_at: number;
}
```

- [ ] **Step 2: Extend `AssessmentReview` and add write helpers**

```ts
export interface AssessmentReview {
  // existing fields...
  teacher_review?: TeacherAssessmentReviewRecord | null;
}

export async function createAssessmentRubricReview(
  sessionId: string,
  payload: CreateTeacherAssessmentReviewRequest,
): Promise<TeacherAssessmentReviewRecord> { /* ... */ }
```

- [ ] **Step 3: Verify TypeScript surface manually**

Run: `rg -n "teacher_review|AssessmentRubricDecision|createAssessmentRubricReview" web/lib/dashboard-api.ts`

Expected: all new symbols appear once and are named consistently.

- [ ] **Step 4: Commit**

```bash
git add web/lib/dashboard-api.ts
git commit -m "feat(web): add assessment rubric review client contract [F111]"
```

### Task 4: Build the rubric composer UI

**Files:**
- Create: `web/components/assessment/AssessmentRubricReviewCard.tsx`
- Modify: `web/app/(workspace)/dashboard/assessments/[sessionId]/page.tsx`

- [ ] **Step 1: Add the rubric review card component**

```tsx
export function AssessmentRubricReviewCard({ sessionId, existingReview, t }: Props) {
  const [wordingQuality, setWordingQuality] = useState(existingReview?.wording_quality ?? "acceptable");
  const [distractorQuality, setDistractorQuality] = useState(existingReview?.distractor_quality ?? "acceptable");
  const [explanationClarity, setExplanationClarity] = useState(existingReview?.explanation_clarity ?? "acceptable");
  const [overallDecision, setOverallDecision] = useState(existingReview?.overall_decision ?? "needs_edit_before_reuse");
  const [teacherNote, setTeacherNote] = useState(existingReview?.teacher_note ?? "");
  // save/update handler
}
```

- [ ] **Step 2: Mount it below the safety gate**

```tsx
<AssessmentRubricReviewCard
  sessionId={sessionId}
  existingReview={review.teacher_review ?? null}
  t={t}
/>
```

- [ ] **Step 3: Show a compact saved summary**

```tsx
{savedReview ? (
  <div className="rounded-2xl border ...">
    <div>{t("Overall decision: {{value}}", { value: savedReview.overall_decision })}</div>
  </div>
) : null}
```

- [ ] **Step 4: Run targeted frontend verification**

Run from repo root:
`./web/node_modules/.bin/eslint --config web/eslint.config.mjs /Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/pod-a-assessment-review-rubric-controls/web/app/'(workspace)'/dashboard/assessments/'[sessionId]'/page.tsx /Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/pod-a-assessment-review-rubric-controls/web/components/assessment/AssessmentRubricReviewCard.tsx /Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/pod-a-assessment-review-rubric-controls/web/lib/dashboard-api.ts`

Expected: no errors, or only the known repo-level Next.js `pages` warning.

- [ ] **Step 5: Commit**

```bash
git add web/app/'(workspace)'/dashboard/assessments/'[sessionId]'/page.tsx web/components/assessment/AssessmentRubricReviewCard.tsx
git commit -m "feat(assessment): add rubric review controls [F111]"
```

### Task 5: Update AI-first docs and final verification

**Files:**
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/TASK_REGISTRY.json`
- Modify: `ai_first/daily/2026-04-27.md`
- Modify: `ai_first/architecture/MAIN_SYSTEM_MAP.md`
- Create: `docs/superpowers/pr-notes/2026-04-28-f111-assessment-review-rubric-controls.md`

- [ ] **Step 1: Update the main system map**

Add a bounded node for rubric review:

```mermaid
AssessmentReview --> AssessmentRubricAPI["POST/PATCH /api/v1/sessions/{session_id}/assessment-rubric-review"]
AssessmentRubricAPI --> AssessmentRubricReview["Teacher assessment review record"]
```

- [ ] **Step 2: Write the PR note with Mermaid**

Document:
- new rubric record
- session review API changes
- why this is not a publish workflow

- [ ] **Step 3: Update AI-first mirrors**

Mark:
- `ACTIVE_ASSIGNMENTS` as `implementation-verified` or `draft-pr-open`
- `TASK_REGISTRY` as `in-progress`
- daily log with tests and scope

- [ ] **Step 4: Run final verification**

Run:
- `pytest tests/api/test_session_review_router.py -k "rubric_review or assessment_review" -q`
- `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `git diff --check`

Expected: PASS / clean diff check

- [ ] **Step 5: Open Draft PR**

```bash
git push -u origin pod-a/assessment-review-rubric-controls
gh pr create --draft --base main --head pod-a/assessment-review-rubric-controls
```
