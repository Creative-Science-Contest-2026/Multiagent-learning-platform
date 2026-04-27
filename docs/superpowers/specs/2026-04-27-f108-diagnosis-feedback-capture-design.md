# F108 Diagnosis Feedback Capture Design

Date: 2026-04-27
Status: Proposed
Task ID: `F108_DIAGNOSIS_FEEDBACK_CAPTURE`
Commit tag: `F108`
Branch: `pod-a/diagnosis-feedback-capture`

## Goal

Let a teacher record whether the current student diagnosis was:
- `helpful`
- `wrong`
- `incomplete`

with an optional note, so diagnosis quality can be reviewed later without mixing that signal into recommendation acknowledgement or teacher-action execution.

## Why This Slice Exists

The dashboard now supports:
- diagnosis display
- recommendation acknowledgement
- teacher actions
- intervention assignments

But there is still no bounded place to answer:

`Was the diagnosis itself useful or correct from the teacher's perspective?`

Without that signal, the system can only track what the teacher did next, not whether the diagnosis framing helped the teacher trust or challenge the underlying inference.

## Scope

Add a lightweight `diagnosis_feedback` object for the top student diagnosis currently shown in the teacher insight flow.

This first pass is:
- per-student only
- label-based
- note-optional
- dashboard/evidence bounded

## Non-Goals

This first pass must not add:
- small-group diagnosis feedback
- analytics over diagnosis feedback patterns
- model retraining logic
- teacher-review workflows for every historical diagnosis version
- auto-resolution of diagnosis quality from downstream actions

## Approaches Considered

### 1. Derive diagnosis feedback from recommendation acknowledgement or teacher action

Pros:
- fewer new objects

Cons:
- conflates trust in the diagnosis with reaction to the recommendation
- loses the teacher's direct judgment on diagnosis quality

### 2. Add explicit diagnosis feedback records

Pros:
- clean boundary
- directly captures teacher supervision on diagnosis quality
- keeps later evaluation and analytics straightforward

Cons:
- adds one more small dashboard-side data object

### 3. Freeform note only

Pros:
- easy UI

Cons:
- too weak for structured reuse
- does not give a stable quality signal for future reviews

## Recommended Approach

Choose **Approach 2: explicit diagnosis feedback records**.

This keeps the product model clean:
- `diagnosis_feedback` = teacher judgment on diagnosis quality
- `recommendation_ack` = teacher response to the recommendation
- `teacher_action` = teacher-owned execution move
- `intervention_assignment` = concrete remediation shell

## Scope Decision: Per-Student Only In The First Pass

Small-group diagnosis is currently an aggregate teaching signal. If feedback is added there too early, the system will mix:
- judgment on individual diagnosis quality
- judgment on grouping quality

So this first pass attaches diagnosis feedback only to `TeacherInsightStudent`.

## Data Model

Add a new `diagnosis_feedback` record under the dashboard/evidence boundary.

### Diagnosis Feedback Shape

- `id`
- `student_id`
- `source_topic`
- `source_diagnosis_type`
- `feedback_label`
  - `helpful`
  - `wrong`
  - `incomplete`
- `teacher_note`
- `created_at`
- `updated_at`

## Boundary Rules

- the record applies to the current top diagnosis shown in the payload
- this first pass only needs the latest visible summary, not a full history UI
- feedback does not modify the diagnosis payload itself
- feedback must not auto-change recommendation or action states

## UI Flow

### Student Card

The student card should let the teacher quickly mark the diagnosis as:
- helpful
- wrong
- incomplete

An optional note can be added in the same compact flow.

The card then shows the latest feedback summary directly on the diagnosis section.

### Student Detail

Student detail should show:
- the current diagnosis feedback label
- the optional teacher note

This should sit near the diagnosis section, not under recommendation acknowledgement or teacher actions.

## API Contract

Add bounded dashboard endpoints:

- `POST /api/v1/dashboard/diagnosis-feedback`
- `PATCH /api/v1/dashboard/diagnosis-feedback/{feedback_id}`

The create route should:
- validate required fields
- accept a feedback label and optional note
- remain teacher-facing only

The update route should only support:
- feedback label change
- note change

## Payload Attachment

Attach the latest diagnosis feedback summary back into:
- `TeacherInsightStudent`
  - `diagnosis_feedback?: DiagnosisFeedbackRecord | null`

This first pass does not attach diagnosis feedback to small-group payloads.

## Storage Boundary

Keep storage alongside:
- `recommendation_acks`
- `teacher_actions`
- `intervention_assignments`

Suggested helper:
- `deeptutor/services/evidence/diagnosis_feedback.py`

## Guardrails

### Guardrail: Do not treat diagnosis feedback as recommendation feedback

Feedback here is about the diagnosis quality, not whether the proposed action was practical.

### Guardrail: Do not auto-close anything

Marking a diagnosis as `helpful` or `wrong` must not automatically update recommendation acknowledgement, teacher actions, or assignments.

### Guardrail: Keep UI compact

This slice is a teacher-quality-control signal, not a new workflow board.

## Testing Strategy

### Backend

Add tests for:
- create diagnosis feedback for a student diagnosis
- update diagnosis feedback label and note
- attach diagnosis feedback summary back to student insight payload

### Frontend

Add targeted validation for:
- diagnosis feedback control render
- student card diagnosis feedback summary
- student detail diagnosis feedback summary

### Validation Commands

- targeted `pytest` for dashboard router and evidence helpers
- targeted `eslint` for changed dashboard files
- `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `git diff --check`

## Owned Files

- `web/components/dashboard/`
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
- group-management flows
- recommendation feedback and intervention-effectiveness systems
- `/agents` authoring UI

## Acceptance Criteria

1. A teacher can mark the current student diagnosis as `helpful`, `wrong`, or `incomplete`.
2. An optional teacher note can be recorded with that feedback.
3. The latest diagnosis feedback reappears in the same student insight flow immediately.
4. Student detail shows the diagnosis feedback summary.
5. The feature stays per-student only in this first pass.
6. The feature remains separate from recommendation acknowledgement, teacher actions, and intervention assignments.
