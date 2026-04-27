# F118 Misconception Taxonomy Expansion

- Task ID: `F118_MISCONCEPTION_TAXONOMY_EXPANSION`
- Commit tag: `F118`
- Status: `Draft PR Open`
- Branch recommendation: `pod-b/misconception-taxonomy-expansion`

## Goal

Broaden the diagnosis taxonomy inside the evidence layer so teacher-reviewable hypotheses can distinguish more classroom-relevant misconception patterns without widening teacher-facing dashboard UX or relaxing the weak-evidence abstain gate.

## Owned Files

- `deeptutor/services/evidence/`
- bounded diagnosis payload contracts if taxonomy values expand
- `tests/services/evidence/`
- bounded `tests/api/test_assessment_router.py`
- bounded `tests/api/test_dashboard_router.py`
- `docs/superpowers/specs/`
- `docs/superpowers/plans/`
- `docs/superpowers/pr-notes/`

## Do Not Touch

- teacher-facing dashboard presentation files
- `web/components/dashboard/`
- `web/app/(workspace)/dashboard/`
- runtime-policy and agent-spec surfaces
- broad student-state schema changes beyond taxonomy-facing fields already present

## Constraints

- keep diagnoses teacher-reviewable hypotheses, not autonomous judgments
- preserve the `F119` abstain gate for thin, stale, or mixed evidence
- prefer bounded rule-based taxonomy expansion over semantic free-text inference
- avoid opening recommendation-feedback, override-log, or dashboard UX scope
