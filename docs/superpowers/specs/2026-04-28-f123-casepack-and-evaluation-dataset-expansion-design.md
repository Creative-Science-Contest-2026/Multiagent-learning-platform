# F123 Design: Casepack And Evaluation Dataset Expansion

## Problem

The repository already has useful contest artifacts such as diagnosis case studies, smoke evidence, and service tests, but those examples are scattered across docs and test files. That makes later validation work harder: future workers have to reconstruct a reusable dataset from prose, code, and screenshots instead of extending one explicit validation pack.

## Design Direction

Keep this slice in validation-ops. The system should package a small, explicit casepack that reuses existing merged evidence patterns without claiming benchmark accuracy or classroom outcome proof. The pack should be readable by humans, stable for tests, and easy to extend later by `F124` automation.

Recommended casepack structure:

- case id and short label
- validation objective
- observation payloads derived from existing evidence patterns
- optional student-state context
- expected bounded outcome such as diagnosis type, abstain code, confidence band, or teacher-review framing
- links back to contest docs or test sources for traceability

## Proposed Contract

1. Add a dedicated structured dataset under `ai_first/evidence/` for a small number of high-signal validation cases.
2. Cover at least the current credibility-critical patterns already used in docs and tests:
   - concept gap
   - careless error
   - thin evidence abstain
   - mixed evidence abstain
   - stale evidence abstain
3. Add a lightweight validation test that proves the pack remains internally consistent and aligned with existing expected diagnosis outcomes.
4. Add one bounded contest-facing doc or readme that explains how to use the casepack without turning it into a public benchmark claim.

## Approach Options

### Option A — Keep prose case studies only

Pros:
- smallest change

Cons:
- not reusable as structured validation input
- future automation still has to reconstruct data manually

### Option B — Add a structured validation casepack plus consistency tests

Pros:
- reusable for future automation and smoke-adjacent checks
- keeps proof explicit and bounded
- stays outside product runtime

Cons:
- introduces one more evidence asset to maintain

### Option C — Build a broader benchmark harness now

Pros:
- more ambitious evaluation story

Cons:
- exceeds bounded scope
- risks overclaiming model quality

## Recommendation

Use **Option B**. It creates a reusable evaluation asset without broadening into benchmarking or product behavior changes.

## Scope Boundary

- in scope: structured validation casepack, traceability/readme doc, consistency tests, bounded contest doc linkage
- out of scope: new diagnosis logic, dashboard UX, benchmark scoring claims, or broad automation tooling

## Proof Plan

- tests prove the casepack is structurally valid and mapped to expected bounded outcomes
- docs prove where the pack fits in the contest and AI-first evidence read path
- PR note explains that the casepack is a reusable validation artifact, not a benchmark leaderboard
