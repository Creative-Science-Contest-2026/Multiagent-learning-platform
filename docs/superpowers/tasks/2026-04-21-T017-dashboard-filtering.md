# Feature Pod Task: Assessment History Filtering & Search

Owner: Codex
Branch: `pod-a/t017-dashboard-filtering`
GitHub Issue: `#59`

## Goal

Add filter and search controls to the teacher dashboard so recent assessment history can be narrowed by common signals.

## User-visible outcome

- Teachers can filter dashboard history by assessment/tutoring type, knowledge pack, score range, and search term.
- The first version stays inside the current dashboard route and API family.
- Empty state remains clean when filters remove all rows.

## Owned files/modules

- `web/app/(workspace)/dashboard/`
- `web/lib/dashboard-api.ts`
- `deeptutor/api/routers/dashboard.py`
- `tests/api/test_dashboard_router.py`
- `docs/superpowers/tasks/2026-04-21-T017-dashboard-filtering.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-21.md`

## Do-not-touch files/modules

- `deeptutor/core/`
- `deeptutor/runtime/`
- Unrelated marketplace, settings, and tutor files
- Root license and upstream attribution files

## API/data contract

- Extend the current dashboard route family
- Reuse existing recent activity and assessment summary data
- Keep filters query-param based and deterministic

## Acceptance criteria

- Dashboard history can be narrowed by at least search term, knowledge pack, and score-oriented assessment filter.
- Backend applies the same filters the UI exposes.
- Filtered empty/loading/error states render cleanly.
- Targeted dashboard API tests cover new filtering behavior.

## Required tests

- Targeted backend tests for dashboard filter behavior
- Frontend build validation for touched dashboard files

## Manual verification

- Open dashboard and apply each filter independently
- Confirm filtered rows match expected history
- Confirm no-result state is still readable

## PR architecture note

- Must include Mermaid diagram.
- Must update `ai_first/architecture/MAIN_SYSTEM_MAP.md` if feature structure changes.

## Handoff notes

- `T016` is merged to `main` through PR `#58`.
- Start from the existing dashboard overview/history flow before adding new analytics or separate listing endpoints.
- Implemented on branch `pod-a/t017-dashboard-filtering` with:
  - dashboard overview filter params
  - teacher dashboard filter panel
  - filtered empty state behavior
- Validation completed:
  - `python3 -m pytest tests/api/test_dashboard_router.py -q`
  - `python3 -m py_compile deeptutor/api/routers/dashboard.py`
  - `cd web && npm run build`
- PR note prepared:
  - `docs/superpowers/pr-notes/2026-04-21-dashboard-filtering.md`
