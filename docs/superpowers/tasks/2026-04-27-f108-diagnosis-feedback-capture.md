# F108 Diagnosis Feedback Capture

- Task ID: `F108_DIAGNOSIS_FEEDBACK_CAPTURE`
- Commit tag: `F108`
- Status: `In progress`
- Branch: `pod-a/diagnosis-feedback-capture`

## Goal

Capture structured teacher feedback on diagnosis quality so the teacher can say whether the current student diagnosis was helpful, wrong, or incomplete.

## Scope

This slice adds:
- explicit per-student diagnosis feedback records
- dashboard endpoints to create and update diagnosis feedback
- diagnosis feedback surfaces on student cards and student detail

This slice does **not** add:
- small-group diagnosis feedback
- analytics over diagnosis feedback
- automatic changes to recommendation, action, or assignment state
- historical diagnosis-feedback timelines

## Owned Files

- `web/components/dashboard/`
- `web/app/(workspace)/dashboard/student/`
- `web/lib/dashboard-api.ts`
- `deeptutor/api/routers/dashboard.py`
- bounded helper code under `deeptutor/services/evidence/`
- `tests/api/test_dashboard_router.py`
- `docs/superpowers/pr-notes/`

## Do-Not-Touch

- `deeptutor/services/runtime_policy/`
- `deeptutor/services/session/`
- small-group management flows
- recommendation feedback systems
- intervention-effectiveness systems
- `/agents` authoring UI

## Backend Contract

Add:
- `POST /api/v1/dashboard/diagnosis-feedback`
- `PATCH /api/v1/dashboard/diagnosis-feedback/{feedback_id}`

Use the diagnosis feedback shape:
- `id`
- `student_id`
- `source_topic`
- `source_diagnosis_type`
- `feedback_label`
- `teacher_note`
- `created_at`
- `updated_at`

Allowed labels:
- `helpful`
- `wrong`
- `incomplete`

## UI Contract

Student card must support:
- direct diagnosis feedback capture
- optional short note
- immediate diagnosis-feedback summary

Student detail must show:
- current diagnosis feedback label
- optional teacher note

## Validation

- `pytest tests/api/test_dashboard_router.py -k "diagnosis_feedback" -q`
- targeted `eslint` for changed dashboard files
- `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `git diff --check`

## Handoff Notes

- Keep diagnosis feedback separate from recommendation acknowledgement.
- Keep this first pass per-student only.
- Prefer compact UI over a review-management panel.
