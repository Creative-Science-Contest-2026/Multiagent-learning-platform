# F117 Implementation Plan

## Objective

Calibrate diagnosis confidence tags more conservatively and more consistently using existing evidence and student-state signals.

## Steps

1. Add failing tests first
   - extend `tests/services/evidence/test_diagnosis.py` for recency-aware and support-burden-aware confidence cases
   - add bounded API assertions in assessment/dashboard tests where confidence tags should downgrade or stabilize
2. Isolate calibration logic
   - extract or refine a helper in `deeptutor/services/evidence/` for confidence-tag derivation
   - thread in recency and support signals from `student_state`
3. Keep downstream consistency
   - ensure teacher-insight grouping still uses the calibrated tags consistently
   - verify that `F119` abstain behavior stays intact
4. Update docs proof
   - add a PR note with Mermaid diagram
   - update `MAIN_SYSTEM_MAP.md` only if the confidence-calibration seam becomes a distinct architecture node
5. Verify
   - run targeted service and API tests
   - run `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
   - run `git diff --check`
