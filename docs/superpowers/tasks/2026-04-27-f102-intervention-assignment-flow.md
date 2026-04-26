# Intervention Assignment Flow

- Task ID: `F102_INTERVENTION_ASSIGNMENT_FLOW`
- Commit tag: `F102`
- Status: `Ready for execution`
- Branch: `pod-a/intervention-assignment-flow`

## Goal

Let teachers convert an existing `teacher_action` into a bounded `intervention_assignment` for:
- `student`
- `small_group`

This task extends the dashboard loop from `Teacher Action` to a concrete remediation assignment shell without building a full delivery or classroom-operations system.

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
- classroom roster, scheduling, or notification systems
- student-facing assignment delivery contracts
- broader assessment generation flow

## Required Behavior

1. Convert a student-linked `teacher_action` into an `intervention_assignment`.
2. Convert a small-group `teacher_action` into an `intervention_assignment`.
3. Keep a tight assignment catalog only:
   - `practice_set`
   - `reteach_session`
   - `prerequisite_review`
   - `small_group_activity`
4. Show the created assignment back in the same dashboard flow immediately.
5. Show intervention assignments in student detail as a separate teacher-facing section.
6. Allow bounded assignment status updates only:
   - `planned`
   - `done`
   - `dismissed`

## Validation

- `pytest tests/api/test_dashboard_router.py -k "teacher_action or intervention_assignment or dashboard_insights" -q`
- `cd web && ./node_modules/.bin/eslint --config eslint.config.mjs components/dashboard/InterventionAssignmentComposer.tsx components/dashboard/StudentInsightCard.tsx components/dashboard/SmallGroupInsightCard.tsx components/dashboard/StudentInsightDetail.tsx lib/dashboard-api.ts`
- `git diff --check`

## Next AI Should Read

1. `docs/superpowers/specs/2026-04-27-f102-intervention-assignment-flow-design.md`
2. `docs/superpowers/plans/2026-04-27-f102-intervention-assignment-flow.md`
3. this packet

## Suggested Next Action

Implement the linked backend assignment store first, then extend dashboard routes and insight payloads, then wire the assignment composer plus detail surfaces, and finish with docs sync and targeted validation.
