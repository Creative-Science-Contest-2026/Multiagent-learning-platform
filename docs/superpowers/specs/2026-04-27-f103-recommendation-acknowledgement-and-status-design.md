# F103 Recommendation Acknowledgement And Status Design

Date: 2026-04-27
Status: Proposed
Task ID: `F103_RECOMMENDATION_ACKNOWLEDGEMENT_AND_STATUS`
Commit tag: `F103`
Branch: `pod-a/recommendation-acknowledgement-status`

## Goal

Let teachers explicitly acknowledge a recommendation as:
- `accepted`
- `deferred`
- `dismissed`
- `completed`

without forcing them to create a `teacher_action` or `intervention_assignment` first.

This makes the dashboard reflect the real teacher workflow state, not just the presence or absence of downstream execution artifacts.

## Why This Slice Exists

The product now supports:
- `F101`: teacher actions
- `F102`: intervention assignments

But there is still no bounded place to capture the simplest question:

`What did the teacher decide about this recommendation?`

That decision may happen before any action or assignment exists. Without `F103`, the dashboard still cannot distinguish:
- the teacher saw the recommendation and agrees
- the teacher wants to postpone it
- the teacher explicitly rejects it
- the teacher considers it complete

## Scope

Add an explicit `recommendation_ack` object linked to a recommendation identifier and target.

This object is lightweight and teacher-facing:
- it records the teacher's response to the recommendation
- it is not an execution artifact
- it is not a delivery artifact
- it stays inside the dashboard/evidence boundary

## Non-Goals

This first pass must not add:
- full recommendation history timelines
- multi-actor collaboration
- analytics over acknowledgement patterns
- classroom delivery or due dates
- automatic coupling to `teacher_action` or `intervention_assignment` lifecycle

## Approaches Considered

### 1. Derive acknowledgement from existing action/assignment state

Infer recommendation status from:
- teacher action existence
- teacher action status
- intervention assignment existence

Pros:
- smallest data-model delta

Cons:
- cannot represent `accepted` or `deferred` before execution objects exist
- collapses teacher intent into downstream artifacts

### 2. Add explicit recommendation acknowledgement records

Store a separate acknowledgement object keyed by recommendation and target.

Pros:
- clean product semantics
- supports pre-action acknowledgement
- keeps later analytics and override work straightforward

Cons:
- adds one more bounded data model

### 3. Overload `teacher_action.status`

Use the `teacher_action` record as the acknowledgement object and extend its statuses.

Pros:
- low immediate surface area

Cons:
- mixes recommendation response with execution state
- breaks the boundary established by `F101`

## Recommended Approach

Choose **Approach 2: explicit recommendation acknowledgement records**.

This preserves the product model:
- `recommendation_ack` = teacher response to the AI suggestion
- `teacher_action` = teacher-owned execution move
- `intervention_assignment` = concrete remediation shell

## Data Model

Add a new `recommendation_ack` record under the same dashboard/evidence boundary.

### Recommendation Acknowledgement Shape

- `id`
- `source_recommendation_id`
- `target_type`
  - `student`
  - `small_group`
- `target_id`
- `status`
  - `accepted`
  - `deferred`
  - `dismissed`
  - `completed`
- `teacher_note`
- `created_at`
- `updated_at`

### Boundary Rules

- `source_recommendation_id` must come from an existing recommendation payload or a stable generated recommendation key.
- only one latest acknowledgement summary needs to be visible per recommendation in this slice
- this first pass does not require a multi-version history viewer

## UI Flow

### Student Card

1. Teacher sees the current recommendation.
2. Teacher can set a recommendation response directly from the card.
3. The card immediately shows:
   - acknowledgement badge
   - optional short teacher note summary

### Small-Group Card

The same acknowledgement flow applies to small-group recommendations.

### Student Detail

Add a bounded recommendation acknowledgement section or summary inside the teacher-move area showing:
- current status
- teacher note

This page does not need a full acknowledgement timeline yet.

## API Contract

Add bounded dashboard endpoints:

- `POST /api/v1/dashboard/recommendation-acks`
- `PATCH /api/v1/dashboard/recommendation-acks/{ack_id}`

The create route should:
- validate required fields
- allow overwrite semantics at the UI layer by showing only the latest record
- remain teacher-facing only

The update route should only support:
- status change
- note change if needed in the same bounded record

## Payload Attachment

Attach acknowledgement summaries back into:
- `TeacherInsightStudent`
  - `recommendation_ack?: RecommendationAckRecord | null`
- small-group insight rows
  - `recommendation_ack?: RecommendationAckRecord | null`

This keeps overview and detail views in sync.

## Storage Boundary

Keep storage alongside:
- `teacher_actions`
- `intervention_assignments`

Suggested helper:
- `deeptutor/services/evidence/recommendation_acks.py`

## Guardrails

### Guardrail: Do not replace teacher action flow

Acknowledgement is a separate layer. A teacher may acknowledge a recommendation without creating an action, and may create an action later.

### Guardrail: Do not infer semantics that were not recorded

`completed` must mean the teacher explicitly marked the recommendation complete, not that the system guessed it from another object.

### Guardrail: Keep UI compact

This slice should improve workflow clarity, not add a heavy management interface.

## Testing Strategy

### Backend

Add tests for:
- create acknowledgement for student recommendation
- create acknowledgement for small-group recommendation
- update acknowledgement status
- attach acknowledgement summary back to student/group payloads

### Frontend

Add targeted validation for:
- acknowledgement composer/control render
- student card acknowledgement summary
- small-group card acknowledgement summary
- student detail acknowledgement summary

### Validation Commands

- targeted `pytest` for dashboard router and evidence helpers
- targeted `eslint` for changed dashboard files
- `git diff --check`

## Owned Files

- `web/components/dashboard/`
- `web/app/(workspace)/dashboard/`
- `web/app/(workspace)/dashboard/student/`
- `web/lib/dashboard-api.ts`
- `deeptutor/api/routers/dashboard.py`
- bounded helper code under `deeptutor/services/evidence/`
- related dashboard tests
- `docs/superpowers/tasks/`
- `docs/superpowers/pr-notes/`

## Do-Not-Touch

- `deeptutor/services/runtime_policy/`
- `deeptutor/services/session/`
- `/agents` authoring UI
- class roster or delivery systems
- recommendation analytics or intervention effectiveness systems beyond bounded acknowledgement display

## Acceptance Criteria

1. A teacher can explicitly mark a recommendation as `accepted`, `deferred`, `dismissed`, or `completed`.
2. The flow works for both `student` and `small_group` recommendations.
3. The acknowledgement appears back in the same dashboard flow immediately.
4. Student detail shows the recommendation acknowledgement summary.
5. The feature does not require creating a teacher action or intervention assignment first.
6. The feature stays inside the dashboard/evidence boundary.

## Follow-On Tasks

If this lands cleanly, the most natural next tasks are:
- `F105_CLASS_INTERVENTION_QUEUE`
- `F108_DIAGNOSIS_FEEDBACK_CAPTURE`
- `F109_RECOMMENDATION_FEEDBACK_CAPTURE`
