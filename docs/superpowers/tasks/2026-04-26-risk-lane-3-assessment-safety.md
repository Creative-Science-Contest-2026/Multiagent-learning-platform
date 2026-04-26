# Feature Pod Task: Risk Lane 3 Assessment Safety And Review

Task ID: `R3_ASSESSMENT_SAFETY`
Commit tag: `R3`
Owner: Session-specific
Branch: `docs-or-pod/assessment-safety`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Make the teacher-review and quality-control layer around assessment generation obvious, concrete, and demo-ready.

## User-visible outcome

- Reviewers see that AI-generated assessments are not blindly published.
- The demo flow clearly shows teacher review, approval, or editing before use.
- The project has a concrete answer for hallucination and pedagogy quality concerns.

## Owned files/modules

- `web/app/(workspace)/guide/`
- `web/components/quiz/`
- `web/app/(workspace)/dashboard/assessments/`
- `docs/contest/`
- `ai_first/competition/`
- `docs/superpowers/tasks/2026-04-26-risk-lane-3-assessment-safety.md`
- `docs/superpowers/pr-notes/*`

## Do-not-touch files/modules

- `deeptutor/services/runtime_policy/`
- `deeptutor/services/evidence/`
- `web/app/(workspace)/agents/`
- `web/app/(workspace)/dashboard/student/`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` unless the assessment-review flow changes materially

## API/data contract

- The selected proof slice must preserve teacher control between generation and publication.
- Do not claim automated assessment quality assurance beyond what the review flow actually supports.
- Safety positioning should rely on human review, not hidden assumptions about model quality.

## Acceptance criteria

- The demo path clearly shows:
  - generated assessment
  - teacher review or edit step
  - publish or accept step
- At least one reusable example exists showing how teacher intervention improves or validates the generated assessment.
- Contest wording is aligned with “human-in-the-loop safety layer”.

## Required tests

- Focused frontend or API checks for the selected review/edit slice if code changes are made
- `git diff --check`

## Manual verification

- Walk one Knowledge Pack through generation, review, and approval.
- Confirm the teacher can intervene before the assessment becomes part of the student flow.
- Confirm the demo can explain how hallucination risk is bounded in practice.

## Parallel-work notes

- This lane may be docs-and-demo heavy if the current UI already supports teacher review sufficiently.
- Avoid expanding into a new authoring system unless the current review step is genuinely invisible or missing.
- Coordinate with the evidence lane so screenshots or demo notes reflect the same review flow.

## PR architecture note

- Must include Mermaid diagram.
- Update `ai_first/architecture/MAIN_SYSTEM_MAP.md` only if the assessment publication flow changes materially.

## Handoff notes

- Primary attack being addressed: “How do you control quality when AI generates assessments?”
- Preferred defense: teacher review is the primary safety gate, not model infallibility.
