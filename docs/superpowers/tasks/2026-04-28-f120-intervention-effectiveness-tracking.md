# F120 Intervention Effectiveness Tracking

- Task ID: `F120_INTERVENTION_EFFECTIVENESS_TRACKING`
- Commit tag: `F120`
- Status: `Implementation`
- Branch recommendation: `pod-b/intervention-effectiveness-tracking`

## Goal

Measure whether teacher interventions appear to help after they are acknowledged, executed, or assigned, and feed that bounded signal back into teacher insights without pretending to prove causal impact.

## Owned Files

- `deeptutor/services/evidence/`
- bounded dashboard payload shaping if effectiveness summaries attach to existing student or small-group records
- `tests/services/evidence/`
- bounded `tests/api/test_dashboard_router.py`
- `docs/superpowers/specs/`
- `docs/superpowers/plans/`
- `docs/superpowers/pr-notes/`

## Do Not Touch

- teacher-facing dashboard presentation files
- `web/components/dashboard/`
- `web/app/(workspace)/dashboard/`
- runtime-policy and agent-spec surfaces
- new classroom roster or ownership primitives

## Constraints

- effectiveness must remain observational and teacher-reviewable, not a causal score
- use only existing execution/feedback/observation records unless the packet is revised
- preserve Session A ownership of dashboard UX and workflow copy
- keep any new payload additions bounded and optional
