# F118 Implementation Plan

## Objective

Expand the evidence-layer diagnosis taxonomy to represent a few more classroom-relevant misconception patterns while preserving the current teacher-review framing and weak-evidence abstain gate.

## Steps

1. Add failing tests first
   - extend `tests/services/evidence/test_diagnosis.py` with cases for `procedure_breakdown`, `support_dependency`, and `fluency_gap`
   - add bounded assessment/dashboard assertions showing the new `diagnosis_type` values survive payload shaping
2. Isolate taxonomy rules
   - extract diagnosis scoring into a dedicated helper under `deeptutor/services/evidence/`
   - expand `DiagnosisType` in `contracts.py`
   - wire in optional support from `student_state.misconception_signals` without requiring new state fields
3. Keep downstream behavior bounded
   - map the new labels onto the existing action set unless a genuinely missing action becomes unavoidable
   - preserve `F119` abstain gating and `F117` confidence calibration unchanged except where taxonomy scoring feeds them
4. Update docs proof
   - add a PR note with Mermaid diagram
   - update `MAIN_SYSTEM_MAP.md` only if the taxonomy helper becomes a distinct architectural seam worth naming
5. Verify
   - run targeted service and API tests
   - run `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
   - run a registry consistency check
   - run `git diff --check`
