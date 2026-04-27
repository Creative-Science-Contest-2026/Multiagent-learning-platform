# F123 Casepack And Evaluation Dataset Expansion

- Task ID: `F123_CASEPACK_AND_EVALUATION_DATASET_EXPANSION`
- Commit tag: `F123`
- Status: `In Progress`
- Branch recommendation: `pod-b/casepack-evaluation-dataset-expansion`

## Goal

Grow the current judge-safe diagnosis and evidence examples into a reusable validation casepack so future model, dashboard, and automation work can rely on one bounded dataset instead of scattered narrative examples.

## Owned Files

- `ai_first/evidence/`
- bounded `docs/contest/`
- `tests/services/evidence/`
- bounded `tests/api/`
- `docs/superpowers/specs/`
- `docs/superpowers/plans/`
- `docs/superpowers/pr-notes/`

## Do Not Touch

- teacher-facing dashboard presentation files
- `web/components/dashboard/`
- `web/app/(workspace)/dashboard/`
- tutoring/runtime-policy/agent-spec implementation files
- diagnosis or evidence business rules unless a bounded validator helper is strictly needed

## Constraints

- keep the pack judge-safe and derived from existing merged behavior, not fabricated benchmark claims
- prefer structured docs/data assets over new product runtime
- if tests are added, they should validate pack structure or consistency, not redefine diagnosis behavior
- preserve current contest claim calibration and teacher-review framing
