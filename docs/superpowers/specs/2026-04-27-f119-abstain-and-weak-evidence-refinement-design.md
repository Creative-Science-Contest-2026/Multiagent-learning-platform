# F119 Design: Abstain And Weak-Evidence Refinement

## Problem

The current evidence layer can already abstain for some narrow single-topic cases, but the abstain seam is not yet centralized or consistently reused when recommendation payloads are shaped for assessment and dashboard consumers. That leaves two gaps:

1. weak or mixed evidence can still produce recommendation-looking payloads if downstream code only looks for the top inferred action
2. abstain reasons are too coarse to distinguish thin evidence, stale evidence, and mixed evidence in bounded runtime proofs

## Design Direction

Introduce a shared evidence-sufficiency seam inside `deeptutor/services/evidence/` that determines whether diagnosis-backed recommendations should be emitted at all. The seam should stay conservative:

- thin evidence: too few recent error-bearing observations
- stale evidence: observations exist but the recency rollup marks the topic as too old to support a fresh recommendation
- mixed evidence: contradiction patterns are high enough that a dominant hypothesis is not trustworthy

The diagnosis builder remains observation-first and teacher-reviewable, but it should return a more structured abstain explanation so downstream consumers can honor it without re-deriving policy from presentation logic.

## Proposed Contract

1. Add a bounded evidence-sufficiency helper in `deeptutor/services/evidence/`
2. Teach `build_student_diagnosis` to surface a stable abstain classification such as:
   - `thin_evidence`
   - `stale_evidence`
   - `mixed_evidence`
3. Gate `recommended_actions` on that helper so abstained payloads stay empty for both assessment and dashboard paths
4. Keep teacher insight aggregation from forming small-group recommendation cards when all contributing student payloads are abstained or weak-gated

## Scope Boundary

- in scope: evidence policy, diagnosis payload structure, recommendation emission, bounded API-test proofs
- out of scope: dashboard copy redesign, new teacher controls, new class-management flows, or broad student-model scoring

## Proof Plan

- service tests prove each abstain class suppresses recommendations
- assessment API tests prove weak/stale evidence sessions return empty `recommended_actions`
- dashboard API tests prove weak-evidence students do not surface actionable recommendation cards or false-confidence small groups
