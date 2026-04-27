# F109 Recommendation Feedback Capture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add bounded teacher feedback on recommendation quality for both student and small-group recommendations, keeping that signal separate from acknowledgement and execution records.

**Architecture:** Introduce a dedicated `recommendation_feedback` record in the dashboard evidence layer, expose the latest feedback summary on student and small-group insight payloads, and render a compact feedback composer directly inside existing recommendation surfaces. The slice reuses current dashboard patterns and avoids analytics or recommendation-engine behavior changes.

**Tech Stack:** FastAPI, Python evidence helpers, TypeScript React, existing dashboard API client, pytest

---

### Task 1: Create the packet and lock the boundaries

**Files:**
- Create: `docs/superpowers/tasks/2026-04-28-f109-recommendation-feedback-capture.md`
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/daily/2026-04-27.md`

- [ ] **Step 1: Write the task packet**

The packet must say:

- owned files are `web/components/dashboard/`, `web/app/(workspace)/dashboard/`, `web/lib/dashboard-api.ts`, `deeptutor/api/routers/dashboard.py`, bounded helpers under `deeptutor/services/evidence/`, and `tests/api/test_dashboard_router.py`
- do-not-touch includes runtime/session layers, `/agents` UI, effectiveness tracking, and new analytics surfaces
- validation commands are the recommendation-feedback dashboard pytest slice, `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`, and `git diff --check`

- [ ] **Step 2: Sync the assignment wording**

Ensure `ACTIVE_ASSIGNMENTS` and the daily log point to the dedicated `F109` packet instead of only the two-session backlog packet.

- [ ] **Step 3: Commit the docs baseline**

```bash
git add ai_first/ACTIVE_ASSIGNMENTS.md ai_first/daily/2026-04-27.md docs/superpowers/specs/2026-04-28-f109-recommendation-feedback-capture-design.md docs/superpowers/plans/2026-04-28-f109-recommendation-feedback-capture.md docs/superpowers/tasks/2026-04-28-f109-recommendation-feedback-capture.md
git commit -m "docs(dashboard): prepare recommendation feedback packet [F109]"
```

### Task 2: Add backend recommendation-feedback support

**Files:**
- Create: `deeptutor/services/evidence/recommendation_feedback.py`
- Modify: `deeptutor/services/evidence/__init__.py`
- Modify: `deeptutor/services/evidence/teacher_insights.py`
- Modify: `deeptutor/api/routers/dashboard.py`
- Test: `tests/api/test_dashboard_router.py`

- [ ] **Step 1: Write failing backend tests**

Add tests that prove:

- student recommendation feedback can be created and updated
- small-group recommendation feedback attaches to the group payload
- the latest recommendation feedback summary appears on student payloads

- [ ] **Step 2: Run the focused failing tests**

Run:

```bash
pytest tests/api/test_dashboard_router.py -k "recommendation_feedback" -q
```

Expected: FAIL because the endpoints and payload field do not exist yet.

- [ ] **Step 3: Implement the storage helper**

Create a SQLite-backed helper for:

- `list_recommendation_feedback`
- `create_recommendation_feedback`
- `update_recommendation_feedback`

with fields:

```python
{
    "id": "...",
    "source_recommendation_id": "...",
    "target_type": "student",
    "target_id": "...",
    "feedback_label": "practical",
    "teacher_note": "",
    "created_at": 0,
    "updated_at": 0,
}
```

- [ ] **Step 4: Attach feedback summaries to payloads**

Extend `teacher_insights.py` so:

- students receive `recommendation_feedback`
- small groups receive `recommendation_feedback`

using the latest matching record for the recommendation target pairing.

- [ ] **Step 5: Add the dashboard endpoints**

Add:

- `POST /api/v1/dashboard/recommendation-feedback`
- `PATCH /api/v1/dashboard/recommendation-feedback/{feedback_id}`

- [ ] **Step 6: Re-run the focused tests**

Run:

```bash
pytest tests/api/test_dashboard_router.py -k "recommendation_feedback" -q
```

Expected: PASS

- [ ] **Step 7: Commit the backend slice**

```bash
git add deeptutor/services/evidence/recommendation_feedback.py deeptutor/services/evidence/__init__.py deeptutor/services/evidence/teacher_insights.py deeptutor/api/routers/dashboard.py tests/api/test_dashboard_router.py
git commit -m "feat(dashboard): add recommendation feedback records [F109]"
```

### Task 3: Add frontend feedback surfaces

**Files:**
- Create: `web/components/dashboard/RecommendationFeedbackComposer.tsx`
- Modify: `web/components/dashboard/StudentInsightCard.tsx`
- Modify: `web/components/dashboard/SmallGroupInsightCard.tsx`
- Modify: `web/components/dashboard/StudentInsightDetail.tsx`
- Modify: `web/lib/dashboard-api.ts`

- [ ] **Step 1: Extend dashboard client types**

Add:

```ts
export type RecommendationFeedbackLabel = "practical" | "relevant" | "too_generic";

export interface RecommendationFeedbackRecord {
  id: string;
  source_recommendation_id: string;
  target_type: "student" | "small_group";
  target_id: string;
  feedback_label: RecommendationFeedbackLabel;
  teacher_note: string;
  created_at: number;
  updated_at: number;
}
```

plus:

- `recommendation_feedback?: RecommendationFeedbackRecord | null` on `TeacherInsightStudent`
- `recommendation_feedback?: RecommendationFeedbackRecord | null` on small-group payloads
- create/update API helpers

- [ ] **Step 2: Build the reusable composer**

Create a small component parallel to `RecommendationAckComposer` that captures:

- bounded label select
- optional note
- save/update button

- [ ] **Step 3: Wire student card and detail**

Inside the existing recommendation surface:

- render the feedback composer
- show a compact summary if feedback exists

- [ ] **Step 4: Wire small-group card**

Inside the group recommendation card:

- render the same composer
- show the latest summary if feedback exists

- [ ] **Step 5: Run targeted frontend validation if feasible**

Preferred command:

```bash
cd web && ./node_modules/.bin/eslint --config eslint.config.mjs components/dashboard/RecommendationFeedbackComposer.tsx components/dashboard/StudentInsightCard.tsx components/dashboard/SmallGroupInsightCard.tsx components/dashboard/StudentInsightDetail.tsx lib/dashboard-api.ts
```

If worktree path handling still makes ESLint ignore files, record that limitation and rely on CI frontend validation.

- [ ] **Step 6: Commit the frontend slice**

```bash
git add web/components/dashboard/RecommendationFeedbackComposer.tsx web/components/dashboard/StudentInsightCard.tsx web/components/dashboard/SmallGroupInsightCard.tsx web/components/dashboard/StudentInsightDetail.tsx web/lib/dashboard-api.ts
git commit -m "feat(dashboard): capture recommendation quality feedback [F109]"
```

### Task 4: Finish docs, validation, and PR handoff

**Files:**
- Modify: `ai_first/architecture/MAIN_SYSTEM_MAP.md`
- Create: `docs/superpowers/pr-notes/2026-04-28-f109-recommendation-feedback-capture.md`
- Modify: `ai_first/daily/2026-04-27.md`
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`

- [ ] **Step 1: Update the architecture map**

Reflect the new recommendation-feedback API and payload summary in the teacher-insights/dashboard path.

- [ ] **Step 2: Write the PR note with Mermaid**

Cover:

- dedicated recommendation feedback records
- student + group attachment to teacher insights
- whether `MAIN_SYSTEM_MAP` changed

- [ ] **Step 3: Run final validation**

Run:

```bash
pytest tests/api/test_dashboard_router.py -k "recommendation_feedback or recommendation_ack or diagnosis_feedback or teacher_action or intervention_assignment" -q
python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null
git diff --check
```

Expected: all pass

- [ ] **Step 4: Open the Draft PR**

Push `pod-a/recommendation-feedback-capture`, open Draft PR, and update `ACTIVE_ASSIGNMENTS` with the PR number and status.
