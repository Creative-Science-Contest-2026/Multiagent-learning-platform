# F109 Recommendation Feedback Capture

- Task ID: `F109_RECOMMENDATION_FEEDBACK_CAPTURE`
- Commit tag: `F109`
- Status: `In progress`
- Branch: `pod-a/recommendation-feedback-capture`

## Goal

Capture bounded teacher feedback on recommendation quality for student and small-group recommendations, while keeping this signal separate from acknowledgement and execution records.

## Scope

This slice adds:
- a dedicated `recommendation_feedback` record
- student and small-group recommendation feedback create/update endpoints
- dashboard summaries on student cards, small-group cards, and student detail

This slice does **not** add:
- recommendation effectiveness scoring
- recommendation-engine behavior changes
- analytics over recommendation feedback
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

- `pytest tests/api/test_dashboard_router.py -k "recommendation_feedback" -q`
- `pytest tests/api/test_dashboard_router.py -k "recommendation_feedback or recommendation_ack or diagnosis_feedback or teacher_action or intervention_assignment" -q`
- `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `git diff --check`

## Handoff Notes

- Keep recommendation feedback separate from recommendation acknowledgement.
- Support both student and small-group targets in the first pass.
- Use only the bounded labels `practical`, `relevant`, and `too_generic` in this slice.
