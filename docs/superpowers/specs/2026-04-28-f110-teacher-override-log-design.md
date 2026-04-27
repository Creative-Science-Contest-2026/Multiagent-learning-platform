# F110 Teacher Override Log Design

- Task ID: `F110_TEACHER_OVERRIDE_LOG`
- Commit tag: `F110`
- Branch: `pod-a/teacher-override-log`
- Status: `Design approved for implementation`

## Goal

Record when a teacher intentionally chooses a different pedagogical move than the one the system recommended, so the product does not lose human judgment context.

This slice should answer:

- did the teacher override the AI recommendation?
- what alternative move did the teacher prefer?
- why did the teacher think the recommendation should be overridden?

It must stay clearly separate from:

- `recommendation_feedback`:
  whether the recommendation felt practical, relevant, or too generic
- `recommendation_ack`:
  whether the teacher accepted, deferred, dismissed, or completed the recommendation
- `teacher_action`:
  what action shell the teacher actually created to execute

## Non-goals

This slice does **not**:

- change recommendation-engine behavior automatically
- create analytics dashboards over overrides
- infer override records from teacher actions silently
- add a new route or review-management page

## Recommended approach

Create a dedicated `teacher_override` record type with a tight reason set and an explicit teacher-selected move.

Support both:

- `student` recommendations
- `small_group` recommendations

Surface the composer directly where the recommendation is already visible:

- `StudentInsightCard`
- `SmallGroupInsightCard`
- `StudentInsightDetail`

This keeps the override close to the recommendation that is being rejected or replaced.

## Alternatives considered

### 1. Extend `teacher_action`

Pros:
- one fewer record type

Cons:
- mixes execution with disagreement
- loses the distinction between “I created an action” and “I think the AI move was wrong for this case”

Rejected.

### 2. Extend `recommendation_feedback`

Pros:
- one fewer endpoint

Cons:
- “too generic” is not the same as “I will use a different move”
- weak machine-readable separation

Rejected.

### 3. Dedicated override record with bounded reasons

Pros:
- clean semantics
- future-proof for later analytics or model-improvement loops
- still small enough for one slice

Chosen.

## Data contract

Add a new record:

- `id`
- `source_recommendation_id`
- `target_type`
  - `student`
  - `small_group`
- `target_id`
- `override_reason`
  - `different_strategy`
  - `needs_more_context`
  - `not_classroom_fit`
- `teacher_selected_move`
  - `reteach_concept`
  - `scaffolded_practice`
  - `review_prerequisite`
  - `small_group_remediation`
- `teacher_note`
- `created_at`
- `updated_at`

## UI design

### Student card

Inside the existing `Teacher move` section:

- add a `TeacherOverrideComposer`
- show summary:
  - `Override reason: {{reason}}`
  - `Teacher-selected move: {{move}}`
  - teacher note if present

### Small-group card

Inside the group recommendation card:

- add the same override capture flow
- show the latest override summary for the group recommendation

### Student detail

Inside the recommendation area:

- show the same composer
- show current latest teacher override

### No new route

This slice stays inside existing dashboard surfaces only.

## Backend boundaries

Allowed backend change:

- add storage helper under `deeptutor/services/evidence/`
- add create/update endpoints in the dashboard router
- attach latest override summaries to teacher insights payloads

Not allowed:

- analytics pipeline
- automatic action creation from overrides
- recommendation-engine policy changes
- new runtime/session behavior

## File scope

### Owned files

- `web/components/dashboard/`
- `web/app/(workspace)/dashboard/`
- `web/lib/dashboard-api.ts`
- `deeptutor/api/routers/dashboard.py`
- bounded helper code under `deeptutor/services/evidence/`
- `tests/api/test_dashboard_router.py`
- `docs/superpowers/pr-notes/`

### Do-not-touch

- `deeptutor/services/runtime_policy/`
- `deeptutor/services/session/`
- `/agents` authoring UI
- intervention-effectiveness tracking
- class-roster or group-management systems

## Acceptance criteria

1. Teachers can create override records for student recommendations.
2. Teachers can create override records for small-group recommendations.
3. Overrides use the bounded reason set and explicit teacher-selected move.
4. Student and small-group insight payloads include the latest override summary.
5. Student detail shows the latest override without introducing a new route.
6. Teacher override remains semantically separate from recommendation feedback, acknowledgement, and execution records.
