# Feature Pod Task: Risk Lane 1 Runtime Binding Proof

Task ID: `R1_RUNTIME_BINDING_PROOF`
Commit tag: `R1`
Owner: Session-specific
Branch: `docs-or-pod/runtime-binding-proof`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Produce bounded, convincing proof that teacher-authored spec packs affect live Tutor Agent behavior through the current runtime policy path.

## User-visible outcome

- Reviewers can see that `/agents` authoring is not just a static UI.
- The team has a repeatable demo or artifact showing behavior changes between at least two spec packs.
- Claims about runtime binding become specific and defensible instead of vague.

## Owned files/modules

- `deeptutor/services/runtime_policy/`
- `deeptutor/services/prompt/`
- `deeptutor/core/capabilities/`
- `deeptutor/services/session/turn_runtime.py` only if the selected proof slice truly needs request-path wiring
- `tests/services/runtime_policy/`
- `tests/core/`
- `docs/contest/`
- `docs/superpowers/tasks/2026-04-26-risk-lane-1-runtime-binding-proof.md`
- `docs/superpowers/pr-notes/*`

## Do-not-touch files/modules

- `deeptutor/services/evidence/`
- `deeptutor/api/routers/dashboard.py`
- `web/app/(workspace)/dashboard/`
- `web/components/dashboard/`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` unless runtime boundaries materially change

## API/data contract

- The proof must distinguish between:
  - compiled policy contract
  - request-path binding
  - user-visible behavior difference
- Do not claim universal end-to-end support unless the selected live request path is directly verified.
- Any debug trace added for proof must remain bounded and not leak unrelated session data.

## Acceptance criteria

- Two contrasting spec packs are defined for a single demo question or session.
- The team can show a stable behavior diff grounded in `SOUL`, `RULES`, or another teacher-authored policy slice.
- At least one explicit artifact exists:
  - runtime trace
  - test
  - screenshot/log bundle
  - repeatable demo script
- Final wording distinguishes “behavioral proof” from “full request-path coverage”.

## Required tests

- Focused runtime-policy or capability tests proving behavior differs under two compiled specs
- `git diff --check`

## Manual verification

- Run the same student prompt against two different spec packs.
- Confirm the output differs in a way the teacher can recognize:
  - tone
  - scaffolding
  - directness
  - guardrail behavior
- Verify any trace or debug output points back to the selected `agent_spec_id` or compiled policy slice.

## Parallel-work notes

- This lane exists to close a judge-risk, not to redesign the runtime stack.
- If full request-path wiring is still incomplete, ship bounded proof and explicit wording rather than expanding into a multi-week runtime refactor.
- Coordinate with the claim-calibration lane so demo wording matches the exact level of proof achieved.

## PR architecture note

- Must include Mermaid diagram.
- Update `ai_first/architecture/MAIN_SYSTEM_MAP.md` only if the selected proof work changes live runtime boundaries.

## Handoff notes

- Primary attack being addressed: “Does `agent_spec_id` actually affect Tutor Agent runtime behavior?”
- Preferred demo shape: two spec packs with one identical student question and a visible behavior difference.
- If full live binding cannot be completed safely in scope, the fallback is a narrower but honest behavioral proof.
