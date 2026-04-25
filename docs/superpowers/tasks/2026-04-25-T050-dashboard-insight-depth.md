# Feature Pod Task: Dashboard Insight Depth Pass

Owner:
Branch: `pod-b/t050-dashboard-insight-depth`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Make teacher dashboard summaries and assessment review outputs more actionable through bounded route and service depth rather than a new analytics subsystem.

## User-visible outcome

- Dashboard signals feel more useful for teacher follow-up.
- Assessment review communicates clearer next-step insights.
- Lane 1 can consume better data later without changing this slice's ownership.

## Progress (in this cycle)

- Implemented backend endpoint: `GET /api/v1/dashboard/insights` in `deeptutor/api/routers/dashboard.py`.
- Added unit test coverage: `tests/api/test_dashboard_router.py` includes `test_dashboard_insights_returns_teacher_recommendations`.
- Added a minimal TypeScript client wrapper and types in `web/lib/dashboard-api.ts` (`getDashboardInsights`, `DashboardInsights`).
- Draft PR opened on branch `pod-b/t050-dashboard-insight-depth` (PR #123).

## Next steps

- Expand `insights` payload with cohort- and teacher-scoped filters (if requested).
- Add front-end consumption examples or a small widget if Lane 1 requests UI exposure.
- Add additional tests and refine recommendations language.

## Owned files/modules

- `deeptutor/api/routers/dashboard.py`
- `deeptutor/services/session/assessment_review.py`
- `web/lib/dashboard-api.ts`
- `tests/api/test_dashboard_router.py`
- `tests/api/test_session_review_router.py`

## Do-not-touch files/modules

- `web/app/(workspace)/dashboard/`
- `web/components/assessment/`
- `web/locales/vi/`
- `ai_first/`

## API/data contract

This slice may add incremental dashboard and review payload fields, but existing route behavior must remain compatible.

## Acceptance criteria

- Dashboard and review payloads surface clearer next-step signals.
- Changes stay inside existing routes rather than opening new route families.
- Added contract depth is documented and test-covered.

## Required tests

- `python3 -m pytest tests/api/test_dashboard_router.py tests/api/test_session_review_router.py -q`
- `python3 -m py_compile deeptutor/api/routers/dashboard.py deeptutor/services/session/assessment_review.py`
- `git diff --check`

## Manual verification

- Confirm dashboard and review payloads still load through current API clients.
- Confirm added fields remain understandable and bounded.

## Parallel-work notes

- Confirm `ai_first/ACTIVE_ASSIGNMENTS.md` is updated before code starts.
- Do not modify dashboard page components in this slice.
- If UI changes are needed to expose the new depth, hand them off to Lane 1 or a later frontend packet.

## PR architecture note

- Must include Mermaid diagram.
- Update `ai_first/architecture/MAIN_SYSTEM_MAP.md` only if the dashboard workflow structure changes materially.

## Handoff notes
