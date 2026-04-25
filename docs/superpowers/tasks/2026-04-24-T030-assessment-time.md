# Feature Pod Task: Assessment Time Tracking & Analytics

Owner: Codex
Branch: `pod-a/t030-assessment-time`
GitHub Issue: `#81`

## Goal

Add a lightweight time-tracking slice for assessment answers so review flows can show how fast or slow a learner answered.

## User-visible outcome

- Assessment answers can carry per-question duration data without breaking existing review flows.
- Assessment review surfaces a compact time-based summary useful to teachers and students.
- The first slice stays backward-compatible with older sessions that have no timing data.

## Owned files/modules

- `deeptutor/api/routers/sessions.py`
- `deeptutor/services/session/assessment_review.py`
- `web/components/quiz/QuizViewer.tsx`
- `web/lib/dashboard-api.ts`
- `web/lib/session-api.ts`
- `web/app/(workspace)/dashboard/assessments/[sessionId]/page.tsx`
- `tests/api/test_session_review_router.py`
- `tests/api/test_assessment_router.py`
- `docs/superpowers/tasks/2026-04-24-T030-assessment-time.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-24.md` if created, otherwise `ai_first/daily/2026-04-23.md`

## Do-not-touch files/modules

- Marketplace, knowledge, tutor, and settings features
- Unrelated API routers
- `deeptutor/core/`
- `deeptutor/runtime/`
- Root license and upstream attribution files

## API/data contract

- Preserve compatibility for existing quiz result submissions that do not send timing data.
- Extend the current assessment result/review payload instead of introducing a new analytics route family for this slice.
- Older sessions without time data should still render cleanly.

## Acceptance criteria

- Question-level duration can be recorded in the current quiz result flow.
- Assessment review exposes at least one useful aggregate timing metric.
- Assessment review can optionally show per-question duration when present.
- Existing assessment review behavior does not regress when timing data is absent.

## Required tests

- Session/review router regression coverage for timing-aware payloads
- Frontend production build verification

## Manual verification

- Submit an assessment result payload with per-question durations
- Open the assessment review page and confirm the timing summary renders coherently

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.

## Handoff notes

- `T029` merged to `main` through PR `#80`.
- GitHub issue sync initially failed with transient GitHub CLI `503` responses, then succeeded later as issue `#81`.
- The implementation stores timing inside the existing `[Quiz Performance]` transcript instead of adding a new assessment-results storage table.
