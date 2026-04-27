# F117 Confidence Calibration Refinement

- Task ID: `F117_CONFIDENCE_CALIBRATION_REFINEMENT`
- Commit tag: `F117`
- Status: `Ready for Review`
- Branch recommendation: `pod-b/confidence-calibration-refinement`

## Goal

Make diagnosis confidence tags more stable and more explicitly tied to evidence density, recency, and signal consistency, while preserving the teacher-review framing and avoiding any teacher-facing dashboard redesign.

## Owned Files

- `deeptutor/services/evidence/`
- bounded dashboard and assessment payload shaping if confidence-tag contracts need tightening
- `tests/services/evidence/`
- bounded `tests/api/test_dashboard_router.py`
- bounded `tests/api/test_assessment_router.py`
- `docs/superpowers/specs/`
- `docs/superpowers/plans/`
- `docs/superpowers/pr-notes/`

## Do Not Touch

- teacher-facing dashboard presentation files
- `web/components/dashboard/`
- `web/app/(workspace)/dashboard/`
- broad student-model schema changes beyond confidence calibration inputs
- runtime-policy and agent-spec surfaces

## Constraints

- keep confidence tags teacher-reviewable, not objective-scoring claims
- prefer bounded calibration rules over opaque statistical scoring
- preserve the new weak-evidence abstain gate from `F119`
- avoid widening into recommendation execution or feedback-capture scope
