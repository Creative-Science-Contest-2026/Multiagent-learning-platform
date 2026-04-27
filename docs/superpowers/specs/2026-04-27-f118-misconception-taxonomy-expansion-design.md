# F118 Design: Misconception Taxonomy Expansion

## Problem

The current diagnosis layer only emits four labels: `concept_gap`, `needs_scaffold`, `careless_error`, and `low_confidence`. That is enough for MVP proof, but it compresses several classroom-distinct patterns into the same bucket. In practice, a student who is repeatedly correct only with heavy hints, a student who starts correctly but breaks down mid-procedure, and a student who is slow but mostly consistent can all look too similar once they clear the abstain gate.

## Design Direction

Expand taxonomy only where the current observation contract already provides usable evidence. The safer move is a bounded rule-based taxonomy inside `deeptutor/services/evidence/`, not a new prompt-driven classifier. The diagnosis engine should keep the same teacher-review posture and the same abstain behavior, but distinguish a few more interpretable patterns before action selection.

Recommended additions:

- `procedure_breakdown`
  - for repeated incorrect attempts with retries and support, where the student appears to engage but fails to sustain a multi-step procedure
- `support_dependency`
  - for correct-or-near-correct performance that consistently requires heavy hints or retries, indicating the student is not yet independent on the topic
- `fluency_gap`
  - for slow, repeated effort on a topic without strong contradiction, where the issue looks closer to automaticity or retrieval than to a prerequisite concept miss

## Proposed Contract

1. Keep `abstain` as the outer gate from `F119`.
2. Expand `DiagnosisType` in `contracts.py` and diagnosis payloads to include the new bounded labels.
3. Isolate taxonomy scoring from generic diagnosis assembly:
   - keep topic selection and confidence calibration where they are
   - add a focused taxonomy helper that scores candidate labels from existing observation fields and optional `student_state.misconception_signals`
4. Keep action selection bounded:
   - `procedure_breakdown` should still map to existing scaffold-oriented actions
   - `support_dependency` should emphasize `increase_scaffold` or `small_group_support`
   - `fluency_gap` should bias toward `retry_easier` or another already-shipped action, unless a new action is strictly necessary
5. Preserve backward compatibility for existing stored observations that still use the original four labels.

## Approach Options

### Option A — Alias-only expansion

Add new display labels but collapse them back to the old action buckets immediately.

Pros:
- low risk
- minimal downstream changes

Cons:
- taxonomy gains are mostly cosmetic
- little proof that the engine is reasoning more precisely

### Option B — Rule-based expansion with existing actions

Add a few new labels, score them from current observation fields, and map them onto the existing recommendation action set.

Pros:
- meaningful improvement in diagnosis precision
- bounded surface area
- compatible with current teacher payloads

Cons:
- requires clearer scoring and tie-break rules

### Option C — Expansion plus new actions

Add new labels and introduce new recommendation actions to match each one.

Pros:
- highest semantic fidelity

Cons:
- likely widens scope into teacher workflow and UX
- increases downstream contract risk

## Recommendation

Use **Option B**. It gives real taxonomy depth without opening new workflow surfaces. The evidence engine can become more classroom-legible while the dashboard and assessment APIs stay structurally stable.

## Scope Boundary

- in scope: evidence-layer taxonomy scoring, expanded diagnosis labels, bounded assessment/dashboard proof, action remapping if it stays inside existing action types
- out of scope: new teacher controls, new dashboard UI treatments, open-ended misconception ontologies, or probabilistic/LLM-based classifiers

## Proof Plan

- service tests prove each new label wins under an intended observation pattern
- assessment/dashboard tests prove expanded `diagnosis_type` values survive payload shaping without breaking abstain behavior
- PR note documents the taxonomy seam and confirms no teacher-facing UX change
