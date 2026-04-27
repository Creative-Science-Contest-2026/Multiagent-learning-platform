# F119 Implementation Plan

## Objective

Implement bounded weak-evidence gating for diagnosis-derived recommendations without broadening into dashboard UX or student-model scoring work.

## Steps

1. Add failing tests first
   - extend `tests/services/evidence/test_diagnosis.py` for thin, stale, and mixed evidence abstain classes
   - extend bounded assessment/dashboard API tests so abstained payloads do not emit recommendation actions
2. Centralize evidence-sufficiency policy
   - add a helper in `deeptutor/services/evidence/` that classifies evidence sufficiency from observations plus available student-state recency signals
   - thread the classification into diagnosis payloads
3. Tighten downstream recommendation shaping
   - keep `recommended_actions` empty on abstained payloads
   - keep teacher-insight small-group aggregation from synthesizing recommendation cards when contributing student payloads are all abstained
4. Update docs proof
   - add a bounded PR note with architecture diagram
   - update contest docs only if an external claim about recommendation confidence must change
5. Verify
   - run targeted service and API tests
   - run `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
   - run `git diff --check`
