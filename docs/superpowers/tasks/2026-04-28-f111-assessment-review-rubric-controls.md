# F111 Assessment Review Rubric Controls

- Task ID: `F111_ASSESSMENT_REVIEW_RUBRIC_CONTROLS`
- Commit tag: `F111`
- Status: `In progress`
- Branch: `pod-a/assessment-review-rubric-controls`

## Goal

Strengthen the teacher review step on the existing assessment review route with a structured rubric record instead of static safety-gate copy only.

## Scope

This slice adds:
- a bounded `teacher_review` rubric record keyed by `session_id`
- create/update endpoints under the existing session review route
- rubric controls on the assessment review page

This slice does **not** add:
- publish/release workflow
- question-level rubric per item
- dashboard aggregation
- student-facing approval semantics

## Owned Files

- `web/components/assessment/`
- `web/app/(workspace)/dashboard/assessments/`
- `deeptutor/api/routers/sessions.py`
- bounded assessment-review persistence helpers
- `tests/api/test_session_review_router.py`
- `docs/superpowers/pr-notes/`

## Do-Not-Touch

- `deeptutor/services/runtime_policy/`
- dashboard teacher-insight routes
- `/agents` authoring UX
- classroom roster and assignment systems

## Validation

- `pytest tests/api/test_session_review_router.py -k "rubric or assessment_review" -q`
- `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `git diff --check`
