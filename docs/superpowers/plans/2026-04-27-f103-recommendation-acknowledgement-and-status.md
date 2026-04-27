# Recommendation Acknowledgement And Status Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` or `superpowers:subagent-driven-development` when executing this plan in a separate session. Steps use checkbox syntax for tracking.

**Goal:** Add an explicit teacher-facing acknowledgement layer so a recommendation can be marked `accepted`, `deferred`, `dismissed`, or `completed` without requiring a teacher action or intervention assignment first.

**Architecture:** This task extends the dashboard/evidence boundary with a lightweight `recommendation_acks` record stored alongside `teacher_actions` and `intervention_assignments`. The backend adds bounded create/update endpoints and attaches the latest acknowledgement summary back onto both student and small-group insight payloads. The frontend adds compact acknowledgement controls on student and small-group cards plus a summary surface in student detail. This task must preserve the separation between recommendation response, execution action, and intervention delivery.

**Tech Stack:** FastAPI, SQLite evidence services, pytest, Next.js App Router, React client components, TypeScript, Tailwind CSS, existing dashboard REST client

---

### Task 1: Define The Contract And Add Failing Coverage

**Files:**
- Modify: `web/lib/dashboard-api.ts`
- Test: `tests/api/test_dashboard_router.py`

- [ ] Add `RecommendationAckStatus`, `RecommendationAckRecord`, request helpers, and payload attachments in `web/lib/dashboard-api.ts`.
- [ ] Extend `TeacherInsightStudent` with `recommendation_ack?: RecommendationAckRecord | null`.
- [ ] Extend `DashboardInsights["small_groups"]` rows with `recommendation_ack?: RecommendationAckRecord | null`.
- [ ] Add failing dashboard API tests for:
  - student acknowledgement create/read round-trip
  - small-group acknowledgement summary attachment
  - acknowledgement status update round-trip
- [ ] Run the targeted pytest slice and confirm failure before implementation.

### Task 2: Implement Backend Recommendation Acknowledgement Storage And Endpoints

**Files:**
- Create: `deeptutor/services/evidence/recommendation_acks.py`
- Modify: `deeptutor/services/evidence/__init__.py`
- Modify: `deeptutor/services/evidence/teacher_insights.py`
- Modify: `deeptutor/api/routers/dashboard.py`
- Test: `tests/api/test_dashboard_router.py`

- [ ] Implement SQLite-backed `recommendation_acks` storage with bounded create/list/update helpers.
- [ ] Validate target type, status, source recommendation id, and note trimming.
- [ ] Add `POST /api/v1/dashboard/recommendation-acks`.
- [ ] Add `PATCH /api/v1/dashboard/recommendation-acks/{ack_id}`.
- [ ] Thread the latest acknowledgement summaries into `build_teacher_insights_payload` for both student and small-group surfaces.
- [ ] Keep acknowledgement semantics independent from `teacher_actions` and `intervention_assignments`.

### Task 3: Add Dashboard UI Controls And Detail Summary

**Files:**
- Create: `web/components/dashboard/RecommendationAckComposer.tsx`
- Modify: `web/components/dashboard/StudentInsightCard.tsx`
- Modify: `web/components/dashboard/SmallGroupInsightCard.tsx`
- Modify: `web/components/dashboard/StudentInsightDetail.tsx`
- Modify: `web/lib/dashboard-api.ts`

- [ ] Add a compact acknowledgement composer/control that can create or update a recommendation acknowledgement.
- [ ] Surface acknowledgement directly on student cards with immediate summary feedback.
- [ ] Surface acknowledgement directly on small-group cards with the same bounded flow.
- [ ] Add recommendation acknowledgement summary to student detail.
- [ ] Keep the UI compact and avoid turning this slice into a history manager.

### Task 4: Update AI-First Mirrors, Architecture Notes, And Verification

**Files:**
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/TASK_REGISTRY.json`
- Modify: `ai_first/daily/2026-04-26.md`
- Modify: `ai_first/architecture/MAIN_SYSTEM_MAP.md`
- Create: `docs/superpowers/tasks/2026-04-27-f103-recommendation-acknowledgement-and-status.md`
- Create: `docs/superpowers/pr-notes/2026-04-27-f103-recommendation-acknowledgement-and-status.md`

- [ ] Add the dedicated F103 task packet with owned files, validation, and handoff rules.
- [ ] Update `MAIN_SYSTEM_MAP.md` to show `recommendation_ack` between recommendation and teacher action.
- [ ] Update AI-first daily log and coordination state as implementation progresses.
- [ ] Write the PR architecture note with a Mermaid diagram.
- [ ] Run verification:
  - targeted `pytest` for dashboard acknowledgement flows
  - targeted `eslint` for changed dashboard files
  - `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
  - `git diff --check`

### Acceptance Criteria

- [ ] A teacher can mark a recommendation as `accepted`, `deferred`, `dismissed`, or `completed`.
- [ ] The flow works for both student and small-group recommendations.
- [ ] The latest acknowledgement reappears in the same dashboard payload immediately.
- [ ] Student detail shows the acknowledgement summary.
- [ ] The feature does not require creating a teacher action or intervention assignment first.
- [ ] `recommendation_ack` remains distinct from `teacher_action` and `intervention_assignment`.
