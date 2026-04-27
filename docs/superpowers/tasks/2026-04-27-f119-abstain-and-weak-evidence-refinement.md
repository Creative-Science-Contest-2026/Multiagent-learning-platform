# F119 Abstain And Weak-Evidence Refinement

- Task ID: `F119_ABSTAIN_AND_WEAK_EVIDENCE_REFINEMENT`
- Commit tag: `F119`
- Status: `Ready for Review`
- Branch recommendation: `pod-b/abstain-weak-evidence-refinement`

## Goal

Refine the evidence layer so diagnosis and recommendation payloads hold back more reliably when signals are too thin, stale, or internally mixed, while preserving the teacher-review framing and avoiding teacher-facing UX rewrites.

## Owned Files

- `deeptutor/services/evidence/`
- bounded payload shaping in `deeptutor/api/routers/dashboard.py` and assessment routes if contracts need tightening
- `tests/services/evidence/`
- bounded `tests/api/test_dashboard_router.py`
- bounded `tests/api/test_assessment_router.py`
- `docs/superpowers/specs/`
- `docs/superpowers/plans/`
- `docs/superpowers/pr-notes/`
- `docs/contest/*.md` only if external claims must be recalibrated

## Do Not Touch

- teacher-facing dashboard presentation files
- `web/components/dashboard/`
- `web/app/(workspace)/dashboard/`
- broad student-model schema changes beyond evidence gating
- runtime-policy and agent-spec surfaces

## Constraints

- keep the refinement conservative and evidence-backed
- prefer explicit abstain reason codes or bounded gating metadata over vague heuristics
- avoid shipping UI-only explanations without runtime proof
- preserve observation-first diagnosis behavior and teacher-review-required framing
