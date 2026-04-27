# F110 Teacher Override Log

- Task ID: `F110_TEACHER_OVERRIDE_LOG`
- Commit tag: `F110`
- Status: `In progress`
- Branch: `pod-a/teacher-override-log`

## Goal

Capture bounded teacher override records for student and small-group recommendations while keeping this signal separate from recommendation feedback and execution records.

## Scope

This slice adds:
- a dedicated `teacher_override` record
- student and small-group override create/update endpoints
- dashboard summaries on student cards, small-group cards, and student detail

This slice does **not** add:
- recommendation-engine adaptation
- override analytics
- automatic action creation
- new routes

## Owned Files

- `web/components/dashboard/`
- `web/app/(workspace)/dashboard/`
- `web/lib/dashboard-api.ts`
- `deeptutor/api/routers/dashboard.py`
- bounded helpers under `deeptutor/services/evidence/`
- `tests/api/test_dashboard_router.py`
- `docs/superpowers/pr-notes/`

## Do-Not-Touch

- `deeptutor/services/runtime_policy/`
- `deeptutor/services/session/`
- `/agents` authoring UX
- intervention-effectiveness systems
- class-roster and group-management systems

## Validation

- `pytest tests/api/test_dashboard_router.py -k "teacher_override" -q`
- `pytest tests/api/test_dashboard_router.py -k "teacher_override or recommendation_feedback or recommendation_ack or diagnosis_feedback or teacher_action or intervention_assignment" -q`
- `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `git diff --check`
