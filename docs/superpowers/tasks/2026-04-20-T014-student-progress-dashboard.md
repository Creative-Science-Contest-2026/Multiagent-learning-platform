# Feature Pod Task: Student Progress Tracking Dashboard

Owner: Codex
Branch: `pod-a/t014-student-progress-dashboard`
GitHub Issue: `#53`

## Goal

Add a student-facing dashboard view that shows progress across assessments, recent learning activity, and topic or knowledge-pack level signals using existing session data.

## User-visible outcome

- Students can open a dashboard view focused on their own learning progress.
- The view summarizes recent assessments and tutoring sessions in one place.
- Students can see at-a-glance progress trends without opening each assessment review separately.

## Owned files/modules

- `web/app/(workspace)/dashboard/`
- `web/lib/dashboard-api.ts`
- `deeptutor/api/routers/dashboard.py`
- `tests/api/test_dashboard_router.py`
- `docs/superpowers/tasks/2026-04-20-T014-student-progress-dashboard.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-20.md`

## Do-not-touch files/modules

- `deeptutor/core/`
- `deeptutor/runtime/`
- Unrelated marketplace, settings, and knowledge-page files
- Root license and upstream attribution files

## API/data contract

- Prefer extending the current dashboard route family in `deeptutor/api/routers/dashboard.py`
- Reuse existing recent-activity and assessment-summary data before introducing new storage
- Keep the first version read-only and deterministic

## Acceptance criteria

- A student-facing dashboard route or section exists under the current dashboard flow.
- The UI shows recent assessment/tutoring activity with useful progress context.
- The backend exposes only the minimal additional data needed for the student dashboard.
- Empty/loading/error states are handled cleanly.

## Required tests

- Targeted backend tests for any new dashboard response shape
- Frontend build/lint validation for touched dashboard files

## Manual verification

- Open the dashboard student view.
- Confirm recent progress data renders.
- Confirm a user with no activity sees a clean empty state.

## PR architecture note

- Must include Mermaid diagram.
- Must update `ai_first/architecture/MAIN_SYSTEM_MAP.md` if feature structure changes.

## Handoff notes

- `T009`, `T010`, `T011`, `T013`, `T022`, and `T028` are now merged and should be treated as completed.
- Start from existing dashboard session summaries and assessment review data; do not invent a second analytics model unless forced by missing fields.
- Implemented on branch `pod-a/t014-student-progress-dashboard` with:
  - `GET /api/v1/dashboard/student-progress`
  - `web/app/(workspace)/dashboard/student/page.tsx`
  - direct teacher-dashboard link into the student progress view
- Validation completed:
  - `python3 -m pytest tests/api/test_dashboard_router.py -q`
  - `python3 -m py_compile deeptutor/api/routers/dashboard.py`
  - `cd web && npm run build`
- PR note prepared:
  - `docs/superpowers/pr-notes/2026-04-21-student-progress-dashboard.md`
