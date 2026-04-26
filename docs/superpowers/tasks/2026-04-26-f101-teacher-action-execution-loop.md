# Teacher Action Execution Loop

- Task ID: `F101_TEACHER_ACTION_EXECUTION_LOOP`
- Commit tag: `F101`
- Status: `Ready for execution`
- Branch: `pod-a/teacher-action-loop`

## Goal

Turn teacher recommendations into structured in-product teacher actions for:
- `student`
- `small_group`

This task closes the loop from insight to action without building a full assignment-delivery system.

## Owned Files

- `web/components/dashboard/`
- `web/app/(workspace)/dashboard/`
- `web/app/(workspace)/dashboard/student/`
- `web/lib/dashboard-api.ts`
- `deeptutor/api/routers/dashboard.py`
- bounded helper code under `deeptutor/services/evidence/`
- `tests/api/test_dashboard_router.py`
- task docs, PR note, daily log, `ACTIVE_ASSIGNMENTS.md`, `TASK_REGISTRY.json`

## Do-Not-Touch

- `deeptutor/services/runtime_policy/`
- `deeptutor/services/session/`
- `/agents` authoring UI
- broader assessment generation flow
- class roster, notification, or student delivery systems

## Required Behavior

1. Create a structured action from a student recommendation.
2. Create a structured action from a small-group recommendation.
3. Use a tight action catalog only:
   - `reteach_concept`
   - `scaffolded_practice`
   - `review_prerequisite`
   - `small_group_remediation`
4. Show the created action back in the dashboard immediately.
5. Show student-linked actions in student detail.
6. Allow bounded status updates:
   - `planned`
   - `done`
   - `dismissed`

## Validation

- `pytest tests/api/test_dashboard_router.py::test_dashboard_teacher_action_create_round_trip tests/api/test_dashboard_router.py::test_dashboard_teacher_action_small_group_summary_attaches_to_group_card tests/api/test_dashboard_router.py::test_dashboard_teacher_action_status_update_round_trip tests/api/test_dashboard_router.py::test_dashboard_insights_returns_students_and_small_groups -q`
- `cd web && ./node_modules/.bin/eslint --config eslint.config.mjs components/dashboard/TeacherActionComposer.tsx components/dashboard/StudentInsightCard.tsx components/dashboard/SmallGroupInsightCard.tsx components/dashboard/StudentInsightDetail.tsx app/'(workspace)'/dashboard/student/page.tsx lib/dashboard-api.ts`
- `git diff --check`

## Next AI Should Read

1. `docs/superpowers/specs/2026-04-26-f101-teacher-action-execution-loop-design.md`
2. `docs/superpowers/plans/2026-04-26-f101-teacher-action-execution-loop.md`
3. this packet

## Suggested Next Action

Implement the backend create/read/update contract first, then wire student and small-group action creation into the dashboard UI, then finish student detail status updates and docs sync.
