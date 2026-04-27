# F107 Intervention History View Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a bounded per-student intervention history feed that shows the chronological sequence of acknowledgements, teacher actions, intervention assignments, and diagnosis feedback on student detail.

**Architecture:** Derive a normalized `intervention_history` list in the teacher-insights backend instead of creating a new persistence layer. Extend the dashboard payload contract, then render the feed on student detail using existing dashboard patterns and data already stored in SQLite-backed evidence helpers.

**Tech Stack:** FastAPI, Python evidence helpers, TypeScript React, existing dashboard API client, pytest

---

### Task 1: Define packet and payload boundaries

**Files:**
- Create: `docs/superpowers/tasks/2026-04-27-f107-intervention-history-view.md`
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/daily/2026-04-27.md`

- [ ] **Step 1: Write the task packet**

Add a packet that states:

- owned files are `web/components/dashboard/`, `web/app/(workspace)/dashboard/student/`, `web/lib/dashboard-api.ts`, `deeptutor/api/routers/dashboard.py`, bounded evidence shaping helpers, and `tests/api/test_dashboard_router.py`
- do-not-touch includes runtime policy, session orchestration, group-management systems, and effectiveness scoring
- validation commands are the dashboard pytest slice, `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`, and `git diff --check`

- [ ] **Step 2: Record task state**

Confirm `ACTIVE_ASSIGNMENTS` and the daily log describe `F107` as a design/implementation session and point at the new packet.

- [ ] **Step 3: Commit the docs baseline**

```bash
git add ai_first/ACTIVE_ASSIGNMENTS.md ai_first/daily/2026-04-27.md docs/superpowers/tasks/2026-04-27-f107-intervention-history-view.md docs/superpowers/specs/2026-04-27-f107-intervention-history-view-design.md docs/superpowers/plans/2026-04-27-f107-intervention-history-view.md
git commit -m "docs(dashboard): prepare intervention history task packet [F107]"
```

### Task 2: Add backend intervention-history normalization

**Files:**
- Modify: `deeptutor/services/evidence/teacher_insights.py`
- Modify: `deeptutor/api/routers/dashboard.py`
- Test: `tests/api/test_dashboard_router.py`

- [ ] **Step 1: Write failing backend tests for history payload**

Add tests that prove:

- a student payload exposes `intervention_history`
- the feed includes `recommendation_ack`, `teacher_action`, `intervention_assignment`, and `diagnosis_feedback`
- items are sorted newest-first by timestamp

- [ ] **Step 2: Run the focused failing tests**

Run:

```bash
pytest tests/api/test_dashboard_router.py -k "intervention_history" -q
```

Expected: FAIL because `intervention_history` is not yet part of the payload.

- [ ] **Step 3: Implement minimal normalization**

Add a helper in `teacher_insights.py` that maps existing records to entries with:

```python
{
    "id": "...",
    "item_type": "teacher_action",
    "timestamp": 0,
    "title": "...",
    "detail": "...",
    "status": "...",
    "topic": "...",
    "source_id": "...",
}
```

Attach the sorted list as `row["intervention_history"]` on each student payload.

- [ ] **Step 4: Re-run the focused tests**

Run:

```bash
pytest tests/api/test_dashboard_router.py -k "intervention_history" -q
```

Expected: PASS

- [ ] **Step 5: Commit backend history shaping**

```bash
git add deeptutor/services/evidence/teacher_insights.py deeptutor/api/routers/dashboard.py tests/api/test_dashboard_router.py
git commit -m "feat(dashboard): add intervention history payload [F107]"
```

### Task 3: Wire the frontend detail view

**Files:**
- Modify: `web/lib/dashboard-api.ts`
- Modify: `web/components/dashboard/StudentInsightDetail.tsx`

- [ ] **Step 1: Extend the dashboard client types**

Add:

```ts
export interface InterventionHistoryItem {
  id: string;
  item_type: "recommendation_ack" | "teacher_action" | "intervention_assignment" | "diagnosis_feedback";
  timestamp: number;
  title: string;
  detail: string;
  status: string;
  topic: string;
  source_id: string;
}
```

and add:

```ts
intervention_history?: InterventionHistoryItem[];
```

to `TeacherInsightStudent`.

- [ ] **Step 2: Render the history section on student detail**

Add a new section below the existing execution sections that:

- shows `{{count}} recorded steps` when data exists
- renders item cards with label, title, topic, detail, and status/timestamp
- shows an empty state when no history exists

- [ ] **Step 3: Run frontend-targeted validation if feasible**

Preferred command:

```bash
cd web && ./node_modules/.bin/eslint --config eslint.config.mjs components/dashboard/StudentInsightDetail.tsx lib/dashboard-api.ts
```

If the worktree cannot resolve the frontend install path cleanly, record the limitation and rely on CI.

- [ ] **Step 4: Commit the detail UI**

```bash
git add web/lib/dashboard-api.ts web/components/dashboard/StudentInsightDetail.tsx
git commit -m "feat(dashboard): show intervention history detail [F107]"
```

### Task 4: Finish validation and PR handoff

**Files:**
- Modify: `ai_first/architecture/MAIN_SYSTEM_MAP.md`
- Create: `docs/superpowers/pr-notes/2026-04-27-f107-intervention-history-view.md`
- Modify: `ai_first/daily/2026-04-27.md`
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`

- [ ] **Step 1: Update architecture note**

Reflect that teacher insights now expose a derived intervention-history feed on student detail. Keep the update bounded to the dashboard/evidence path.

- [ ] **Step 2: Write the PR note with Mermaid**

Document:

- normalized feed source types
- student detail rendering path
- whether `MAIN_SYSTEM_MAP` changed

- [ ] **Step 3: Run final verification**

Run:

```bash
pytest tests/api/test_dashboard_router.py -k "intervention_history or teacher_action or intervention_assignment or recommendation_ack or diagnosis_feedback" -q
python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null
git diff --check
```

Expected: all pass

- [ ] **Step 4: Open Draft PR**

Use commit tag `[F107]`, push `pod-a/intervention-history-view`, open Draft PR, and update `ACTIVE_ASSIGNMENTS` with the PR number and status.
