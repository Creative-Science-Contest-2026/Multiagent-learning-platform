# F102 Intervention Assignment Flow Design

Date: 2026-04-27
Status: Proposed
Task ID: `F102_INTERVENTION_ASSIGNMENT_FLOW`
Commit tag: `F102`
Branch: `pod-a/intervention-assignment-flow`

## Goal

Extend the merged `F101_TEACHER_ACTION_EXECUTION_LOOP` so a teacher can turn a bounded teacher action into a concrete remediation assignment or follow-up activity without opening a full LMS or classroom-operations subsystem.

This slice must make the dashboard loop stronger:

`Observed -> Inferred -> Recommended Action -> Teacher Action -> Intervention Assignment`

## Why This Slice Exists

`F101` proved that teachers can convert a recommendation into a structured teacher action. That still leaves a gap between:
- a teacher decision
- a concrete remediation artifact that can be referenced, reviewed, and reused

Without `F102`, the product still stops one step short of a usable execution loop. The teacher can say what they want to do, but not turn that decision into a bounded assignment/remediation shell inside the product.

## Scope

This design adds a lightweight `intervention_assignment` object linked to an existing `teacher_action`.

The assignment object is intentionally teacher-facing first:
- it records what follow-up activity the teacher intends to run
- it stays inside the dashboard/evidence boundary
- it does not become a student delivery contract yet

## Non-Goals

This first pass must not add:
- due dates
- student-facing delivery
- notifications
- submission/completion contracts
- grading
- class roster integration
- calendar/scheduling workflows

Those belong to later tasks such as classroom operations or richer intervention tracking.

## Approaches Considered

### 1. Expand `teacher_action` only

Add more fields directly onto the existing `teacher_action` record and treat it as both the decision and the assignment.

Pros:
- smallest backend delta
- lowest migration cost

Cons:
- blurs the boundary between teacher intent and teacher-created remediation artifact
- makes later assignment history and intervention tracking harder to model cleanly

### 2. Add a linked `intervention_assignment` shell

Keep `teacher_action` as the decision object, and add a second object linked to it for the assignment/remediation shell.

Pros:
- keeps product semantics clean
- creates a clear upgrade path for intervention history and effectiveness tracking
- still fits inside the teacher-facing dashboard slice

Cons:
- slightly more backend and UI work than option 1

### 3. Build a mini LMS flow

Create a more complete assignment system with delivery semantics, due dates, and completion tracking.

Pros:
- stronger long-term structure

Cons:
- too large for this slice
- immediately drags in classroom operations and student-facing contracts

## Recommended Approach

Choose **Approach 2: linked `intervention_assignment` shell**.

This keeps the product model clean:
- `teacher_action` = teacher intent / planned move
- `intervention_assignment` = concrete follow-up activity created from that move

It is the smallest approach that still creates a real product step beyond notes or status tags.

## Data Model

Add a new `intervention_assignment` record in the same bounded storage area currently used for dashboard teacher actions.

### Intervention Assignment Shape

- `id`
- `teacher_action_id`
- `target_type`
  - `student`
  - `small_group`
- `target_id`
- `assignment_type`
  - `practice_set`
  - `reteach_session`
  - `prerequisite_review`
  - `small_group_activity`
- `topic`
- `title`
- `teacher_note`
- `practice_note`
- `status`
  - `draft`
  - `planned`
  - `done`
  - `dismissed`
- `created_at`
- `updated_at`

### Boundary Rules

- Every intervention assignment must be linked to an existing `teacher_action`.
- A teacher action can exist without an intervention assignment.
- This slice does not require multiple assignments per action, but the model should not prevent that later.

## UI Flow

### Student Path

1. Teacher opens a student insight card or student detail view.
2. Teacher sees an existing `teacher_action`.
3. Teacher clicks `Convert to assignment`.
4. The system opens a compact assignment composer with prefills from the teacher action:
   - topic
   - likely assignment type
   - base teacher instruction
5. Teacher edits:
   - assignment type
   - title
   - teacher note
   - practice note
6. On save, the dashboard immediately shows the assignment summary under that action.

### Small-Group Path

1. Teacher creates or views a group action from the small-group card.
2. Teacher clicks `Convert to assignment`.
3. The assignment shell is created for the whole group with a group-appropriate default type.
4. The group card shows the assignment summary immediately.

## Teacher-Facing Surfaces

### Dashboard Overview

- Student cards continue to show the latest `teacher_action`.
- If an assignment exists for the newest action, show a compact summary:
  - assignment type
  - title
  - status

### Student Detail

Add a new section:
- `Intervention assignments`

Each record shows:
- assignment type
- title
- topic
- note summary
- status

### Small-Group Card

Show the latest linked assignment summary for the group action if one exists.

## API Contract

Add bounded dashboard endpoints:

- `POST /api/v1/dashboard/intervention-assignments`
- `PATCH /api/v1/dashboard/intervention-assignments/{assignment_id}`

The create route should:
- validate the linked `teacher_action_id`
- inherit `target_type` and `target_id` from the teacher action
- require non-empty assignment content fields

The update route should only support bounded status changes in this slice.

## Storage Boundary

Keep storage inside the current dashboard/evidence boundary next to `teacher_actions`.

Do not create a new classroom or delivery subsystem.

A dedicated helper module under `deeptutor/services/evidence/` is acceptable, for example:
- `intervention_assignments.py`

## Guardrails

### Guardrail: Do not build delivery

This slice produces an assignment shell only. It does not claim the student has received or completed anything.

### Guardrail: Do not replace teacher actions

Assignments are downstream artifacts from teacher actions. They should not bypass the `teacher_action` step.

### Guardrail: Keep the loop visible

If the created assignment does not appear back in the same dashboard flow immediately, the feature will not feel real.

## Testing Strategy

### Backend

Add tests for:
- create assignment from valid teacher action
- reject assignment when linked action does not exist
- list/attach assignment summaries back to student/group insight payloads
- update assignment status

### Frontend

Add targeted coverage or bounded validation for:
- assignment composer render and create flow
- student detail assignment summary render
- group assignment summary render

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
- bounded `deeptutor/services/evidence/`
- related dashboard tests
- `docs/superpowers/tasks/`
- `docs/superpowers/pr-notes/`

## Do-Not-Touch

- `deeptutor/services/runtime_policy/`
- `deeptutor/services/session/`
- `/agents` authoring UX
- broader classroom operations or roster systems
- assessment-generation internals outside bounded dashboard needs

## Acceptance Criteria

1. A teacher can convert a `teacher_action` into an `intervention_assignment`.
2. The flow works for both `student` and `small_group` targets.
3. The assignment appears immediately in the same dashboard flow after creation.
4. Student detail exposes intervention assignments as a separate teacher-facing section.
5. The feature does not introduce delivery, due dates, or completion semantics.
6. The backend and UI remain inside the dashboard/evidence boundary.

## Follow-On Tasks

If this lands cleanly, the most natural next tasks are:
- `F103_RECOMMENDATION_ACKNOWLEDGEMENT_AND_STATUS`
- `F107_INTERVENTION_HISTORY_VIEW`
- `F120_INTERVENTION_EFFECTIVENESS_TRACKING`
