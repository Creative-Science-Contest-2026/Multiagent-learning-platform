# F111 Assessment Review Rubric Controls Design

## Summary

`F111` adds a bounded teacher-review record to the existing assessment review flow so teachers can rate question wording, distractor quality, and explanation clarity with an explicit reuse decision. The design strengthens the current safety-gate messaging without opening a publishing workflow or changing student-facing behavior.

## Problem

The current assessment review page already tells teachers to review AI-generated assessments before reuse, but the page only provides static guidance. There is no structured way to record whether the assessment is ready, what dimension is weak, or why the teacher would block reuse. That makes the review step hard to repeat, hard to prove, and easy to lose on refresh.

## Recommended Approach

Use a structured review record keyed by `session_id`.

This approach is preferred because it:
- stays on the existing `/api/v1/sessions/{session_id}/assessment-review` path
- preserves the current teacher-reviewed framing from `R3_ASSESSMENT_SAFETY`
- adds persistence without expanding into publishing, assignment, or dashboard analytics

## Data Model

Create a bounded `teacher_review` record with:

- `id`
- `session_id`
- `wording_quality`
  - `strong`
  - `acceptable`
  - `weak`
- `distractor_quality`
  - `strong`
  - `acceptable`
  - `weak`
- `explanation_clarity`
  - `strong`
  - `acceptable`
  - `weak`
- `overall_decision`
  - `approved_for_reuse`
  - `needs_edit_before_reuse`
  - `not_ready`
- `teacher_note`
- `created_at`
- `updated_at`

This record is teacher-authored quality control metadata. It is not a publishing flag and must not be treated as student-facing release state.

## API Contract

Keep the existing session review route and add bounded write endpoints:

- `GET /api/v1/sessions/{session_id}/assessment-review`
  - extend the response with `teacher_review`
- `POST /api/v1/sessions/{session_id}/assessment-rubric-review`
  - create a review record when none exists
- `PATCH /api/v1/sessions/{session_id}/assessment-rubric-review`
  - update the stored record

The GET response remains the main page bootstrap payload. The new `teacher_review` field must be optional so old sessions still load without data migration work.

## UI Design

Keep all changes on the existing assessment review page.

Add one new section directly below the existing `Teacher Review Safety Gate`:

- title: `Teacher Review Rubric`
- three rubric inputs:
  - `Question wording`
  - `Distractor quality`
  - `Explanation clarity`
- one overall decision input:
  - `Approved for reuse`
  - `Needs edit before reuse`
  - `Not ready`
- one optional note field
- one save/update action

When a record already exists, the page must load it into the form and render a compact review summary card beneath the controls.

## Boundaries

This slice does not:
- create a publish button
- create question-level rubric evaluation
- add dashboard rollups
- generate teacher actions automatically
- change AI runtime or diagnosis logic

This slice only records structured teacher review state for a single assessment session.

## Testing

Add API tests that prove:
- a review record can be created for a valid assessment session
- a saved review record is returned by `GET /assessment-review`
- an existing record can be updated
- missing sessions still return `404`

Frontend verification should focus on:
- correct bootstrap rendering from the extended payload
- update flow calling the correct endpoint
- persisted state surviving refresh

## Acceptance Criteria

- teachers can save a structured rubric review on the assessment review page
- the review persists by `session_id`
- the assessment review GET payload returns the saved review
- the page shows saved values after refresh
- the product still frames this as teacher review, not automated approval
