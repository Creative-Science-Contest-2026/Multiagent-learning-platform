# Feature Pod Task: Risk Lane 4 Teacher Value Proposition

Task ID: `R4_TEACHER_VALUE_PROP`
Commit tag: `R4`
Owner: Session-specific
Branch: `docs-or-pod/teacher-value-prop`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Translate the technical architecture into concrete teacher-facing value so non-technical judges and voters understand why the product matters.

## User-visible outcome

- `/agents` and the evidence loop are explained in teacher-benefit language rather than internal architecture language.
- The team can answer “why does a teacher need this?” without talking about compiler layers first.
- Demo materials foreground classroom value before engineering sophistication.

## Owned files/modules

- `docs/contest/`
- `ai_first/competition/`
- `web/app/(workspace)/agents/` only if copy-level clarification is needed
- `web/components/agents/` only if copy-level clarification is needed
- `docs/superpowers/tasks/2026-04-26-risk-lane-4-teacher-value-prop.md`
- `docs/superpowers/pr-notes/*`

## Do-not-touch files/modules

- `deeptutor/services/`
- `deeptutor/api/`
- `web/app/(workspace)/dashboard/`
- `web/components/dashboard/`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` unless shipped surface areas materially change

## API/data contract

- Do not change runtime or storage semantics just to improve positioning.
- If UI copy changes are made, they must stay truthful to the implemented behavior.
- Teacher-facing language should distinguish:
  - teacher-defined style/policy
  - evidence-backed insight
  - student-facing tutoring behavior

## Acceptance criteria

- At least 2-3 teacher use cases are documented in clear, non-technical language.
- The project has a short explanation for what `IDENTITY`, `SOUL`, and `RULES` let a teacher control.
- A behavior-diff example exists that a judge can understand without reading code.

## Required tests

- If copy changes touch UI files, run the smallest relevant lint/build check
- `git diff --check`

## Manual verification

- Rehearse the `/agents` demo without using terms like “compiler”, “contract”, or “runtime assembly” first.
- Confirm a non-technical listener can understand what changes when a teacher edits the spec.
- Confirm the demo still stays honest about current product limits.

## Parallel-work notes

- This lane is primarily narrative, evidence, and demo hardening.
- Avoid turning it into a broad marketing rewrite of the whole repo.
- Coordinate with runtime-binding and claim-calibration lanes so wording stays technically accurate.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` should remain unchanged unless shipped user flows materially change.

## Handoff notes

- Primary attack being addressed: “Why would a normal teacher care about `/agents` or spec authoring?”
- Preferred defense: simple teacher outcomes, not agent-system jargon.
