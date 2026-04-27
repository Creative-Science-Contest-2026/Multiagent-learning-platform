# F103 Recommendation Acknowledgement And Status

- Task ID: `F103_RECOMMENDATION_ACKNOWLEDGEMENT_AND_STATUS`
- Commit tag: `F103`
- Status: `In progress`
- Branch: `pod-a/recommendation-acknowledgement-status`

## Goal

Add a bounded teacher-facing recommendation acknowledgement layer so teachers can explicitly respond to a recommendation before or without creating a teacher action or intervention assignment.

## Scope

This slice adds:
- explicit recommendation acknowledgement records
- dashboard endpoints to create and update acknowledgements
- student and small-group acknowledgement surfaces
- bounded acknowledgement summary in student detail

This slice does **not** add:
- recommendation history timelines
- analytics over acknowledgement behavior
- classroom delivery or due dates
- automatic coupling to teacher-action or assignment lifecycle

## Owned Files

- `web/components/dashboard/`
- `web/app/(workspace)/dashboard/`
- `web/app/(workspace)/dashboard/student/`
- `web/lib/dashboard-api.ts`
- `deeptutor/api/routers/dashboard.py`
- bounded helper code under `deeptutor/services/evidence/`
- `tests/api/test_dashboard_router.py`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md`
- `docs/superpowers/pr-notes/`

## Do-Not-Touch

- `deeptutor/services/runtime_policy/`
- `deeptutor/services/session/`
- `/agents` authoring UI
- class roster, delivery, or notification systems
- recommendation analytics and intervention-effectiveness systems beyond bounded acknowledgement display

## Backend Contract

Add:
- `POST /api/v1/dashboard/recommendation-acks`
- `PATCH /api/v1/dashboard/recommendation-acks/{ack_id}`

Use the acknowledgement shape:
- `id`
- `source_recommendation_id`
- `target_type`
- `target_id`
- `status`
- `teacher_note`
- `created_at`
- `updated_at`

Allowed status values:
- `accepted`
- `deferred`
- `dismissed`
- `completed`

## UI Contract

Student card and small-group card must support:
- direct acknowledgement
- optional short note
- immediate acknowledgement summary

Student detail must show:
- current acknowledgement status
- short note if present

## Validation

- `pytest tests/api/test_dashboard_router.py -k "recommendation_ack" -q`
- targeted `eslint` for changed dashboard files
- `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `git diff --check`

## Handoff Notes

- Keep `recommendation_ack` separate from `teacher_action`.
- Use only the latest acknowledgement summary in this first pass.
- Prefer compact UI over a new management panel.
