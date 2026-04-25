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
