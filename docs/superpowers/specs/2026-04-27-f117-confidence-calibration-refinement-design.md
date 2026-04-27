# F117 Design: Confidence Calibration Refinement

## Problem

The current confidence tags are still relatively coarse. They react to evidence count and contradiction ratio, but they do not yet calibrate against recency decay or the richer student-state signals that now exist after `F116` and `F119`. That leaves confidence tags vulnerable to two distortions:

1. a recent but thin signal can look similar to a stronger multi-observation pattern
2. an older or support-heavy pattern can still present as too certain once a diagnosis clears the abstain gate

## Design Direction

Refine confidence-tag assignment inside `deeptutor/services/evidence/` without changing the teacher-review policy. The calibration should stay rule-based and inspectable:

- increase confidence only when evidence is recent, repeated, and internally consistent
- cap confidence when support burden remains high even if the dominant diagnosis is stable
- reduce confidence when student-state recency and contradiction signals indicate partial uncertainty, even if the payload is still strong enough to avoid abstaining

## Proposed Contract

1. Keep `abstain` as the hard gate from `F119`
2. Add a bounded calibration helper that derives `low` / `medium` / `high` from:
   - error-bearing evidence count
   - contradiction ratio
   - recency bucket mix from `student_state.recency_summary`
   - support burden from `student_state.support_signals`
3. Reuse the calibrated tag consistently in diagnosis payloads and teacher-insight grouping

## Scope Boundary

- in scope: evidence-layer confidence rules, bounded API payload proofs, teacher-insight grouping behavior if confidence thresholds shift
- out of scope: new UI affordances, teacher override workflows, or probabilistic confidence scoring systems

## Proof Plan

- service tests prove confidence changes across recent/repeated, support-heavy, and mixed-recency cases
- assessment and dashboard API tests prove the calibrated tags surface consistently without breaking the abstain gate
