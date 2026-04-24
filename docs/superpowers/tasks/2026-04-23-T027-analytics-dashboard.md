# Feature Pod Task: Teacher Analytics Dashboard

Owner: Codex
Branch: `pod-a/t027-analytics-dashboard`
GitHub Issue: `#77`

## Goal

Add a higher-signal teacher analytics slice so the dashboard shows more than session lists and basic student progress summaries.

## User-visible outcome

- Teachers can see richer dashboard insights for engagement, assessment trends, and common learning difficulties.
- The dashboard stays grounded in existing session and assessment-review data instead of introducing a separate analytics store in this slice.
- Existing dashboard filters and review drill-downs continue to work.

## Owned files/modules

- `web/app/(workspace)/dashboard/page.tsx`
- `deeptutor/api/routers/dashboard.py`
- `tests/api/test_dashboard_router.py`
- `docs/superpowers/tasks/2026-04-23-T027-analytics-dashboard.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-23.md`

## Do-not-touch files/modules

- Marketplace, knowledge, tutor, and settings pages
- Unrelated API routers
- `deeptutor/core/`
- `deeptutor/runtime/`
- Root license and upstream attribution files

## API/data contract

- Prefer extending the existing dashboard overview payload instead of creating a separate dashboard API family in this first slice.
- Use current session history and assessment review parsing as the source of truth.
- Keep existing dashboard filters backward-compatible.

## Acceptance criteria

- Dashboard exposes at least one new engagement signal, one assessment trend signal, and one learning-difficulty signal useful to teachers.
- Backend analytics remain derived from the current session/review data already stored in the app.
- Existing overview and student progress routes do not regress.

## Required tests

- Dashboard router regression coverage for the new analytics fields
- Frontend production build verification

## Manual verification

- Open the teacher dashboard with mixed assessment/session history
- Confirm the new analytics summaries render and stay coherent with the existing filters

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.

## Handoff notes

- `T026` merged to `main` through PR `#76`.
- Start from the current dashboard overview flow and extend the most useful signals first; avoid building a full charting system in one slice.
