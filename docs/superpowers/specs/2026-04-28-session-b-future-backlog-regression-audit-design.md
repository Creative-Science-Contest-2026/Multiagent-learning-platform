# Session B Future Backlog Regression Audit Design

## Goal

Review the merged Session B future-backlog slices for correctness and contract compliance, then either fix concrete regressions or produce a bounded audit note that explains why the shipped scope is still sound.

## Approach

Chosen approach: `packet-to-code audit + grouped validation reruns + fix-on-finding`.

Why:

- a pure test rerun can miss requirement drift if a task shipped the wrong shape but tests were too narrow
- a pure document review can miss live integration breakage after later merges
- a grouped audit lets the lane stay narrow while still covering the highest-risk Session B runtime/data surfaces

## Review Units

### Unit 1: Runtime policy and binding path

- `F113`
- `F114`
- `F115`

Audit focus:

- runtime binding coverage remains bounded and truthful
- per-session spec pinning still preserves version metadata correctly
- runtime policy audit endpoints still expose the intended trace surface

### Unit 2: Evidence, diagnosis, and student-model path

- `F116`
- `F117`
- `F118`
- `F119`
- `F120`

Audit focus:

- signal enrichment remains observational and bounded
- confidence and abstain logic stay consistent across later taxonomy additions
- intervention-effectiveness summaries do not overclaim causality

### Unit 3: Validation-ops and roster path

- `F121`
- `F122`
- `F123`
- `F124`

Audit focus:

- roster scoping remains bounded to backend/data ownership
- pilot-feedback ingestion still preserves the explicit "no pilot evidence yet" claim when empty
- casepack and evidence-refresh artifacts still match current docs and tests

## Output Strategy

- If the audit finds defects, patch only the affected bounded Session B files and their tests.
- If the audit finds no defects, add one PR note summarizing the reviewed units, commands rerun, residual risk, and why no fix was needed.
- Keep frontend teacher UX untouched unless a backend contract defect forces a matching UI correction, which is not expected for this audit.

## Architecture Impact

- no intended architecture expansion
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` should change only if an audit-discovered defect requires a real behavior correction
