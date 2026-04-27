# F116 Student Model Enrichment

- Task ID: `F116_STUDENT_MODEL_ENRICHMENT`
- Commit tag: `F116`
- Status: `Ready for Review`
- Branch recommendation: `pod-b/student-model-enrichment`

## Goal

Expand student state beyond thin recency summaries into richer, evidence-backed mastery, support, and misconception signals that later diagnosis and teacher-insight work can reuse.

## Owned Files

- `deeptutor/services/evidence/`
- `deeptutor/services/session/`
- related backend tests for evidence/session contracts
- `docs/superpowers/specs/`
- `docs/superpowers/plans/`
- `docs/superpowers/pr-notes/`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` if shared student-state contracts change

## Do Not Touch

- teacher-facing dashboard presentation files
- `web/components/dashboard/`
- `web/app/(workspace)/dashboard/`
- broad `/agents` UX changes
- runtime-policy or agent-spec routes unless a bounded dependency is discovered

## Constraints

- keep the student model conservative and evidence-backed
- do not introduce opaque global mastery scores
- preserve observation-first diagnosis behavior
- prefer additive student-state fields over broad contract rewrites
