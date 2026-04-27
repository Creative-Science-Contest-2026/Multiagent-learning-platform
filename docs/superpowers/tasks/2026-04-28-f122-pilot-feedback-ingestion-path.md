# F122 Pilot Feedback Ingestion Path

- Task ID: `F122_PILOT_FEEDBACK_INGESTION_PATH`
- Commit tag: `F122`
- Status: `In Progress`
- Branch recommendation: `pod-b/pilot-feedback-ingestion-path`

## Goal

Prepare a bounded ingestion and status path for future external walkthrough or pilot feedback so the repository can store real feedback later without overstating what current evidence proves today.

## Owned Files

- `deeptutor/api/routers/system.py`
- `deeptutor/services/evidence/`
- `tests/api/test_system_router.py`
- `tests/services/evidence/`
- bounded `docs/contest/`
- bounded `ai_first/competition/`
- `docs/superpowers/specs/`
- `docs/superpowers/plans/`
- `docs/superpowers/pr-notes/`

## Do Not Touch

- teacher-facing dashboard presentation files
- `web/components/dashboard/`
- `web/app/(workspace)/dashboard/`
- tutoring runtime, capability binding, and agent-spec surfaces
- recommendation, diagnosis, and classroom workflow UX beyond bounded contest/ops wording

## Constraints

- preserve the explicit current stance that no pilot evidence is bundled yet unless real feedback is actually added
- avoid fabricated quotes, participant counts, outcomes, or classroom-validated wording
- keep the ingestion seam separate from teacher-facing product UX
- prefer a narrow validation-ops API or storage contract over broad workflow expansion
