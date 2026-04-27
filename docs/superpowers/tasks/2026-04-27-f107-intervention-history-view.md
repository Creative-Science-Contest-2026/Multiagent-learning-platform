# F107 Intervention History View

- Task ID: `F107_INTERVENTION_HISTORY_VIEW`
- Commit tag: `F107`
- Status: `In progress`
- Branch: `pod-a/intervention-history-view`

## Goal

Show a unified per-student intervention history feed so a teacher can inspect the sequence of acknowledgement, execution, assignment, and diagnosis-review records in one detail surface.

## Scope

This slice adds:
- a derived `intervention_history` feed on `TeacherInsightStudent`
- student-detail rendering for intervention history
- payload tests for ordering and record coverage

This slice does **not** add:
- effectiveness scoring
- class-level or small-group history pages
- new persistent tables
- new execution objects

## Owned Files

- `web/components/dashboard/`
- `web/app/(workspace)/dashboard/student/`
- `web/lib/dashboard-api.ts`
- `deeptutor/api/routers/dashboard.py`
- bounded evidence/dashboard shaping helpers
- `tests/api/test_dashboard_router.py`
- `docs/superpowers/pr-notes/`

## Do-Not-Touch

- `deeptutor/services/runtime_policy/`
- `deeptutor/services/session/`
- class-roster systems
- intervention-effectiveness scoring logic
- `/agents` authoring UX

## Validation

- `pytest tests/api/test_dashboard_router.py -k "intervention_history" -q`
- `pytest tests/api/test_dashboard_router.py -k "intervention_history or teacher_action or intervention_assignment or recommendation_ack or diagnosis_feedback" -q`
- `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `git diff --check`

## Handoff Notes

- Keep the history feed per-student only in this slice.
- Normalize history in the backend rather than stitching it entirely in React.
- Do not let the UI imply intervention effectiveness; this slice is descriptive history only.
