# F109 Recommendation Feedback Capture Design

- Task ID: `F109_RECOMMENDATION_FEEDBACK_CAPTURE`
- Commit tag: `F109`
- Branch: `pod-a/recommendation-feedback-capture`
- Status: `Design approved for implementation`

## Goal

Capture bounded teacher feedback on recommendation quality so the product can learn whether a recommended teacher move felt practical, relevant, or too generic.

This slice should answer:

- was the recommendation useful as a recommendation?
- if not, why did the teacher think it missed?

It must stay clearly separate from:

- `recommendation_ack`:
  whether the teacher accepted, deferred, dismissed, or completed the recommendation
- `teacher_action`:
  what the teacher actually chose to do
- `diagnosis_feedback`:
  whether the diagnosis itself was correct or helpful

## Non-goals

This slice does **not**:

- score recommendation effectiveness
- alter diagnosis or recommendation generation automatically
- create analytics dashboards over recommendation quality
- add a new route or review-management page

Those belong later in:

- `F110_TEACHER_OVERRIDE_LOG`
- `F120_INTERVENTION_EFFECTIVENESS_TRACKING`
- broader recommendation-engine improvement work

## Recommended approach

Create a dedicated `recommendation_feedback` record type with a tight label set and an optional teacher note.

Support both:

- `student` recommendations
- `small_group` recommendations

Surface the composer directly where the recommendation is already visible:

- `StudentInsightCard`
- `SmallGroupInsightCard`
- `StudentInsightDetail`

This keeps the interaction close to the recommendation itself and avoids forcing teachers into a separate review flow.

## Alternatives considered

### 1. Extend `recommendation_ack`

Pros:
- fewer endpoints

Cons:
- mixes “did the teacher act on it?” with “was the recommendation good?”
- pollutes acknowledgement semantics

Rejected.

### 2. Freeform teacher note only

Pros:
- fast to build

Cons:
- weak machine-readable signal
- hard to aggregate later

Rejected.

### 3. Dedicated feedback record with bounded labels

Pros:
- clean semantics
- future-proof for later analytics
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
- `feedback_label`
  - `practical`
  - `relevant`
  - `too_generic`
- `teacher_note`
- `created_at`
- `updated_at`

### Payload attachment

For students:

- attach `recommendation_feedback` to `TeacherInsightStudent`

For small groups:

- attach `recommendation_feedback` to each small-group card payload

### Semantics

`practical`
- teacher thinks the move is usable in real classroom action

`relevant`
- teacher thinks the move fits the student/group need

`too_generic`
- teacher thinks the move is vague or not tailored enough

This first pass allows only one latest feedback record per recommendation target pairing to be shown in the payload.

## UI design

### Student card

Inside the existing `Teacher move` section:

- add a `RecommendationFeedbackComposer`
- show summary:
  - `Recommendation feedback: {{label}}`
  - teacher note if present

### Small-group card

Inside the group recommendation card:

- add the same feedback capture flow
- show the latest feedback summary for the group recommendation

### Student detail

Inside the recommendation area:

- show the same composer
- show current latest recommendation feedback

### No new route

This slice stays inside existing dashboard surfaces only.

## Backend boundaries

Allowed backend change:

- add storage helper under `deeptutor/services/evidence/`
- add create/update endpoints in the dashboard router
- attach latest feedback summaries to teacher insights payloads

Not allowed:

- new analytics pipeline
- recommendation-engine retraining or policy changes
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
- intervention-effectiveness tracking logic
- class-roster or group-management systems

## Acceptance criteria

1. Teachers can create recommendation-quality feedback for student recommendations.
2. Teachers can create recommendation-quality feedback for small-group recommendations.
3. Feedback uses the bounded labels `practical`, `relevant`, and `too_generic`.
4. Student and small-group insight payloads include the latest recommendation feedback summary.
5. Student detail shows the latest recommendation feedback without introducing a new route.
6. Recommendation feedback remains semantically separate from acknowledgement and execution records.

## Testing

- backend tests for student recommendation feedback create/update round trip
- backend tests for small-group recommendation feedback attachment
- backend tests that payload returns the latest feedback summary
- `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `git diff --check`

## Risks

### Risk: overlap with recommendation acknowledgement

Mitigation:
- keep separate endpoint, separate label set, separate payload field

### Risk: labels still feel ambiguous

Mitigation:
- keep labels narrow and classroom-facing
- do not add more categories in this slice

### Risk: small-group semantics diverge from student semantics

Mitigation:
- reuse the same feedback object shape
- only vary `target_type` and `target_id`
