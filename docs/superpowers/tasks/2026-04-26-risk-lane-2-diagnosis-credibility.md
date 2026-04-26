# Feature Pod Task: Risk Lane 2 Diagnosis Credibility

Task ID: `R2_DIAGNOSIS_CREDIBILITY`
Commit tag: `R2`
Owner: Session-specific
Branch: `docs-or-pod/diagnosis-credibility`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Strengthen the credibility of diagnosis and recommendation outputs by making their logic, examples, and teacher-review framing explicit.

## User-visible outcome

- The team can explain how diagnosis works without bluffing benchmark accuracy.
- Reviewers see examples where observation, diagnosis, and recommendation line up clearly.
- The project can defend “teacher-in-the-loop” as a deliberate safety and pedagogy choice.

## Owned files/modules

- `deeptutor/services/evidence/`
- `tests/services/evidence/`
- `docs/contest/`
- `ai_first/competition/`
- `docs/superpowers/tasks/2026-04-26-risk-lane-2-diagnosis-credibility.md`
- `docs/superpowers/pr-notes/*`

## Do-not-touch files/modules

- `deeptutor/services/runtime_policy/`
- `deeptutor/services/session/`
- `web/app/(workspace)/agents/`
- `web/components/agents/`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` unless diagnosis boundaries materially change

## API/data contract

- Diagnosis outputs must remain framed as:
  - evidence-backed
  - confidence-tagged
  - teacher-reviewable
- Do not introduce fabricated numeric accuracy claims.
- Example packs, cases, or comparison tables must stay demo-safe and non-private.

## Acceptance criteria

- At least 2-3 diagnosis case studies are documented or test-backed.
- Each case shows:
  - observed inputs
  - inferred diagnosis
  - recommended action
  - teacher-review framing or commentary
- Final project wording explicitly states that the system is rule-assisted plus teacher-reviewed, not a benchmarked autonomous assessor.

## Required tests

- Focused diagnosis/recommendation tests for the selected case patterns
- `git diff --check`

## Manual verification

- Walk through the prepared cases as if answering a judge.
- Confirm that every diagnosis can be traced back to observations.
- Confirm that weak or ambiguous evidence is either downgraded or abstained on rather than overstated.

## Parallel-work notes

- This lane can ship purely as examples, docs, and framing improvements if engine behavior is already adequate.
- If engine behavior itself is weak, keep the change bounded to the smallest slice that materially improves credibility.
- Coordinate with the dashboard-actionability lane so case studies can double as story cards.

## PR architecture note

- Must include Mermaid diagram.
- Update `ai_first/architecture/MAIN_SYSTEM_MAP.md` only if the diagnosis pipeline structure changes materially.

## Handoff notes

- Primary attack being addressed: “How accurate or trustworthy is your diagnosis layer?”
- Preferred defense: transparent reasoning, bounded confidence, teacher-in-the-loop.
- Do not overcorrect by inventing fake evaluation metrics.
