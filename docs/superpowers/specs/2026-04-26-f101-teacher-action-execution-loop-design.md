# Teacher Action Execution Loop Design

Date: 2026-04-26
Task ID: F101_TEACHER_ACTION_EXECUTION_LOOP
Commit tag: F101
Status: Proposed

## Goal

Extend the teacher dashboard from recommendation-only behavior into the first executable teacher-action loop.

The first slice should let a teacher turn a recommendation into a structured remediation step directly inside the product for either:
- a single student
- a small group

This slice must stay intentionally narrower than a full assignment or classroom delivery system.

## Why This Slice Exists

The current product already supports:
- `Observed`
- `Inferred`
- `Recommended Action`

That still leaves a gap between insight and action. A teacher can see what the system suggests, but cannot yet convert that suggestion into a first-class in-product execution record. `F101` closes that gap without overreaching into due dates, LMS delivery, notifications, or class roster management.

## Scope

### In Scope

- create a structured `teacher action` from a student recommendation
- create a structured `teacher action` from a small-group recommendation
- show the created action back in the dashboard flow
- show student-linked actions in the student detail surface
- allow bounded status changes on created actions
- use a tight action catalog rather than a freeform assignment model

### Out Of Scope

- student-facing assignment delivery
- due dates or scheduling
- notifications
- class-level bulk assignment
- real grading or completion proof
- class roster system
- runtime policy changes
- learner-model redesign

## Action Model

The first slice uses a lightweight `teacher action` object.

Required fields:
- `id`
- `target_type`
  - `student`
  - `small_group`
- `target_id`
- `source_recommendation_id`
- `action_type`
  - `reteach_concept`
  - `scaffolded_practice`
  - `review_prerequisite`
  - `small_group_remediation`
- `topic`
- `teacher_instruction`
- `priority`
  - `low`
  - `medium`
  - `high`
- `status`
  - `draft`
  - `planned`
  - `done`
  - `dismissed`
- `created_at`
- `updated_at`

This object is a teacher execution record, not a student-facing assignment object.

## Product Behavior

### Dashboard Overview

Student cards should expose a `Create action` entry point.

Small-group cards should expose a `Create group action` entry point.

The action creation flow should open inline from the dashboard through a lightweight panel or modal rather than forcing a new route.

### Action Creation Flow

The form should be short and structured:
- `action_type`
- `topic`
- `teacher_instruction`
- `priority`

Prefilled values:
- `target_type`
- `target_id`
- `source_recommendation_id`
- default `topic` from the current recommendation when available

After submit:
- the recommendation should read as converted into a teacher action
- the action summary should be visible immediately in the dashboard flow

### Student Detail

The student detail surface should include a `Teacher actions` section.

Teachers should be able to:
- see actions linked to that student
- update action status between `planned`, `done`, and `dismissed`

### Small-Group Behavior

The first slice does not require a new group detail route.

A small-group action only needs to:
- be creatable from the overview card
- show a visible action summary back on that group card
- remain traceable through the recommendation linkage

## UI Rules

- use a tight catalog, not a freeform action system
- preserve the evidence-first hierarchy already established in the dashboard
- do not replace recommendations with actions silently; show both the recommendation context and the created action summary
- status changes should stay simple and clearly teacher-owned

## Storage And Backend Boundary

The storage path should stay inside the dashboard/evidence boundary rather than creating a separate assignment subsystem.

Preferred boundary:
- dashboard router for API surface
- evidence/dashboard service layer for persistence and retrieval helpers

The slice should avoid inventing a new broad domain unless persistence clearly demands a focused helper module.

## Session Ownership

### Owned Files

- `web/components/dashboard/`
- `web/app/(workspace)/dashboard/`
- `web/app/(workspace)/dashboard/student/`
- `web/lib/dashboard-api.ts`
- `deeptutor/api/routers/dashboard.py`
- bounded helper code in `deeptutor/services/evidence/` only if needed for action persistence or retrieval
- task packet, PR note, daily log, `ACTIVE_ASSIGNMENTS.md`, and `TASK_REGISTRY.json` updates for this task

### Do-Not-Touch

- `deeptutor/services/runtime_policy/`
- `deeptutor/services/session/`
- `/agents` authoring surfaces
- broader assessment generation flow
- class roster / classroom management subsystems
- notifications or student delivery systems

## Acceptance Criteria

1. A teacher can create a structured action from a student recommendation.
2. A teacher can create a structured action from a small-group recommendation.
3. The action uses the approved tight catalog.
4. The action appears back in the dashboard flow immediately after creation.
5. Student detail shows actions linked to that student.
6. A teacher can update action status in the bounded status set.
7. The implementation does not claim or behave like a full assignment-delivery system.
8. Tests cover the main create/read/update path for the new action loop.

## Architecture Notes

This slice extends the current `Observed -> Inferred -> Recommended Action` pipeline into:

`Observed -> Inferred -> Recommended Action -> Teacher Action`

That new step is intentionally teacher-owned and execution-oriented. It should not collapse into a generic notes feature, and it should not expand into a full classroom operations stack in this first pass.

## Risks And Guardrails

### Risk: Scope Drift Into Assignment System

Guardrail:
- no due date
- no delivery
- no scheduling
- no notification
- no student completion contract

### Risk: Overlap With Session B

Guardrail:
- stay out of runtime-policy and session-runtime internals
- only touch backend data shaping where required for dashboard action persistence

### Risk: Weak Visibility After Creation

Guardrail:
- the created action must appear back in the same dashboard flow immediately, or the loop will not feel real to the teacher

## Recommended Next Step After F101

If this slice lands cleanly, the natural next tasks are:
- `F102_INTERVENTION_ASSIGNMENT_FLOW`
- `F103_RECOMMENDATION_ACKNOWLEDGEMENT_AND_STATUS`
- `F108_DIAGNOSIS_FEEDBACK_CAPTURE`

Those follow-ups should build on the action object introduced here instead of replacing it.
