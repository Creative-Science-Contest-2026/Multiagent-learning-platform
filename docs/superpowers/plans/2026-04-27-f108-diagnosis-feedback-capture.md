# Diagnosis Feedback Capture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add structured per-student teacher feedback for the current diagnosis so a diagnosis can be marked helpful, wrong, or incomplete with an optional note.

**Architecture:** This feature extends the existing dashboard/evidence boundary with a lightweight `diagnosis_feedback` record stored alongside recommendation acknowledgements, teacher actions, and intervention assignments. The backend adds bounded create/update endpoints and attaches the latest diagnosis feedback summary back onto `TeacherInsightStudent`, while the frontend adds a compact diagnosis-feedback control on the student card and a summary section on student detail. This task must keep diagnosis-quality feedback separate from recommendation acknowledgement and execution artifacts.

**Tech Stack:** FastAPI, SQLite evidence services, pytest, Next.js App Router, React client components, TypeScript, Tailwind CSS, existing dashboard REST client

---

### Task 1: Define The Diagnosis Feedback Contract And Tests

**Files:**
- Modify: `web/lib/dashboard-api.ts`
- Test: `tests/api/test_dashboard_router.py`

- [ ] Add `DiagnosisFeedbackLabel`, `DiagnosisFeedbackRecord`, and request helpers to `web/lib/dashboard-api.ts`.
- [ ] Extend `TeacherInsightStudent` with `diagnosis_feedback?: DiagnosisFeedbackRecord | null`.
- [ ] Add failing dashboard API tests for:
  - student diagnosis feedback create/read round-trip
  - diagnosis feedback update round-trip
  - diagnosis feedback summary attachment to the student payload
- [ ] Run the targeted pytest slice and confirm failure before implementation.

### Task 2: Implement Backend Diagnosis Feedback Storage And Endpoints

**Files:**
- Create: `deeptutor/services/evidence/diagnosis_feedback.py`
- Modify: `deeptutor/services/evidence/__init__.py`
- Modify: `deeptutor/services/evidence/teacher_insights.py`
- Modify: `deeptutor/api/routers/dashboard.py`
- Test: `tests/api/test_dashboard_router.py`

- [ ] Implement SQLite-backed `diagnosis_feedback` storage with bounded create/list/update helpers.
- [ ] Validate student id, topic, diagnosis type, label, and note trimming.
- [ ] Add `POST /api/v1/dashboard/diagnosis-feedback`.
- [ ] Add `PATCH /api/v1/dashboard/diagnosis-feedback/{feedback_id}`.
- [ ] Thread the latest diagnosis feedback summary into `TeacherInsightStudent`.
- [ ] Keep diagnosis feedback semantics independent from recommendation acknowledgement, teacher actions, and assignments.

### Task 3: Add Dashboard UI Controls And Detail Summary

**Files:**
- Create: `web/components/dashboard/DiagnosisFeedbackComposer.tsx`
- Modify: `web/components/dashboard/StudentInsightCard.tsx`
- Modify: `web/components/dashboard/StudentInsightDetail.tsx`
- Modify: `web/lib/dashboard-api.ts`

- [ ] Add a compact diagnosis-feedback composer/control that can create or update student diagnosis feedback.
- [ ] Surface diagnosis feedback directly on the student card inside the diagnosis section.
- [ ] Add diagnosis feedback summary to student detail near the diagnosis section.
- [ ] Keep the UI compact and per-student only.

### Task 4: Update AI-First Mirrors, Task Packet, And Verification

**Files:**
- Create: `docs/superpowers/tasks/2026-04-27-f108-diagnosis-feedback-capture.md`
- Create: `docs/superpowers/pr-notes/2026-04-27-f108-diagnosis-feedback-capture.md`
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/TASK_REGISTRY.json`
- Modify: `ai_first/daily/2026-04-27.md`
- Modify: `ai_first/architecture/MAIN_SYSTEM_MAP.md` if the data-flow map changes materially

- [ ] Add the dedicated F108 task packet with owned files, validation, and handoff rules.
- [ ] Update `MAIN_SYSTEM_MAP.md` if the new diagnosis-feedback record/API is a material product data-flow change.
- [ ] Update AI-first daily log and coordination state as implementation progresses.
- [ ] Write the PR architecture note with a Mermaid diagram.
- [ ] Run verification:
  - targeted `pytest` for dashboard diagnosis-feedback flows
  - targeted `eslint` for changed dashboard files
  - `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
  - `git diff --check`

### Acceptance Criteria

- [ ] A teacher can mark the current student diagnosis as `helpful`, `wrong`, or `incomplete`.
- [ ] An optional teacher note can be saved with the diagnosis feedback.
- [ ] The latest diagnosis feedback reappears in the same student insight flow immediately.
- [ ] Student detail shows the diagnosis feedback summary.
- [ ] The feature stays per-student only in this first pass.
- [ ] The feature remains separate from recommendation acknowledgement, teacher actions, and intervention assignments.
