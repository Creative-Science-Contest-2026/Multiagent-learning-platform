# F107 Intervention History View Design

- Task ID: `F107_INTERVENTION_HISTORY_VIEW`
- Commit tag: `F107`
- Branch: `pod-a/intervention-history-view`
- Status: `Design approved for implementation`

## Goal

Let a teacher inspect what intervention-related steps have already happened for a student, in one place, without forcing the teacher to mentally merge recommendation acknowledgements, teacher actions, intervention assignments, and diagnosis feedback.

This slice is about **history visibility**, not intervention scoring. It should answer:

- what did the teacher or system record most recently?
- in what order did those records happen?
- what is the current latest execution state for the student?

## Non-goals

This slice does **not**:

- infer whether an intervention was effective
- add outcome scoring or intervention-quality analytics
- create a small-group history page
- redesign assignment or action creation flows
- add new teacher workflow objects beyond the existing records

Those belong later in:

- `F109_RECOMMENDATION_FEEDBACK_CAPTURE`
- `F120_INTERVENTION_EFFECTIVENESS_TRACKING`
- possible future group-history work

## Design Choice

### Recommended approach: unified timeline on student detail

Build a derived `intervention_history` feed for each student by combining existing records:

- `recommendation_ack`
- `teacher_actions`
- `intervention_assignments`
- `diagnosis_feedback`

Each entry is normalized into one history item with:

- item type
- timestamp
- headline
- supporting detail
- lightweight status metadata

The first UI surface is the student detail page. Dashboard overview cards stay unchanged in this slice.

### Why this approach

- It stays inside the owned files and existing contracts.
- It solves the teacher problem directly without inventing a new subsystem.
- It avoids collapsing into `F120`, where “what happened next” becomes true effectiveness tracking.

## Alternatives considered

### 1. Separate intervention-history object store

Pros:
- very explicit long-term model

Cons:
- duplicates data that already exists
- adds write-path complexity
- too heavy for this slice

### 2. UI-only stitching inside React

Pros:
- fast

Cons:
- duplicates business logic in the frontend
- harder to test
- makes future small-group or analytics extension messier

### 3. Derived history feed in dashboard backend

Pros:
- one clear normalization layer
- easy to test
- keeps frontend simple

Cons:
- requires small payload contract extension

This is the chosen approach.

## Data contract

Add a derived `intervention_history` array to `TeacherInsightStudent`.

Each item should follow this shape:

- `id`
- `item_type`
  - `recommendation_ack`
  - `teacher_action`
  - `intervention_assignment`
  - `diagnosis_feedback`
- `timestamp`
- `title`
- `detail`
- `status`
- `topic`
- `source_id`

### Mapping rules

`recommendation_ack`
- title: teacher response to recommendation
- detail: teacher note if present, else compact fallback text
- status: ack status

`teacher_action`
- title: teacher action type
- detail: teacher instruction
- status: action status

`intervention_assignment`
- title: assignment type or title
- detail: teacher note or practice note summary
- status: assignment status

`diagnosis_feedback`
- title: diagnosis feedback label
- detail: teacher note or compact fallback
- status: feedback label

Sort descending by timestamp so the most recent record appears first.

## UI design

### Student detail

Add a new section:

- eyebrow: `Intervention history`
- title:
  - `{{count}} recorded steps` if not empty
  - `No intervention history yet` if empty

Each history item card should show:

- item label
- title
- topic if available
- detail text
- compact timestamp/status row

### Empty state

If there is no history:

- explain that actions, acknowledgements, assignments, and diagnosis feedback will appear here once recorded

### Dashboard overview

Do not add a new intervention-history surface on overview in this slice.

The primary and only required UI deliverable is student detail.

## Backend boundaries

Allowed backend change:

- add a normalization helper inside the dashboard/evidence layer
- extend teacher insights payload to include `intervention_history`

Not allowed:

- new persistent intervention-history table
- changes to runtime policy
- changes to session orchestration

## File scope

### Owned files

- `web/components/dashboard/`
- `web/app/(workspace)/dashboard/student/`
- `web/lib/dashboard-api.ts`
- `deeptutor/api/routers/dashboard.py`
- bounded dashboard/evidence shaping helpers
- `tests/api/test_dashboard_router.py`
- `docs/superpowers/pr-notes/`

### Do-not-touch

- `deeptutor/services/runtime_policy/`
- `deeptutor/services/session/`
- `/agents` authoring UI
- class-roster or group-management systems
- intervention-effectiveness scoring logic

## Acceptance criteria

1. Student detail shows a unified intervention history section.
2. History includes existing recommendation acknowledgements, teacher actions, intervention assignments, and diagnosis feedback for that student.
3. Items are normalized and sorted by most recent timestamp.
4. No new persistent store is introduced for history.
5. Existing creation and status-update flows continue to work unchanged.
6. The slice remains clearly separate from effectiveness tracking.

## Testing

- backend tests for the normalized history feed on teacher insights payload
- backend tests that multiple record types appear in the expected order
- targeted UI wiring validation through existing frontend CI
- `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `git diff --check`

## Risks

### Risk: timeline semantics drift into “effectiveness”

Mitigation:
- keep labels descriptive only
- do not add success/failure judgment

### Risk: frontend duplicates record formatting logic

Mitigation:
- normalize titles and details in backend payload as much as practical

### Risk: small-group expectations creep into this slice

Mitigation:
- keep first pass strictly per-student
- leave group history to a later packet if still needed
