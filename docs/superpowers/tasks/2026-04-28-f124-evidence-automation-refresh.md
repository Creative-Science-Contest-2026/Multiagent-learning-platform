# Task Packet: F124 Evidence Automation Refresh

- Task ID: `F124_EVIDENCE_AUTOMATION_REFRESH`
- Commit tag: `F124`
- Owner: `Codex`
- Status: `brainstorming`

## Objective

Automate the command-backed evidence refresh path so contest validation status is easier to regenerate and review without overstating what remains manual.

## Owned Files

- `scripts/contest/`
- `docs/contest/`
- `ai_first/evidence/`
- bounded `tests/` for automation helpers
- `docs/superpowers/tasks/2026-04-28-f124-evidence-automation-refresh.md`
- `docs/superpowers/specs/2026-04-28-f124-evidence-automation-refresh-design.md`
- `docs/superpowers/plans/2026-04-28-f124-evidence-automation-refresh.md`
- `docs/superpowers/pr-notes/2026-04-28-f124-evidence-automation-refresh.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-28.md`

## Do-Not-Touch

- runtime product code
- screenshot capture automation
- video capture automation
- dashboard or tutoring UX
- control-plane files outside those listed above

## Acceptance Criteria

1. A bounded evidence-refresh helper exists under `scripts/contest/`.
2. The helper can produce a machine-readable evidence status artifact under `ai_first/evidence/`.
3. Contest docs clearly distinguish auto-refreshed command evidence from manual screenshot/video evidence.
4. A bounded test validates helper output shape or execution-plan assembly.
5. AI-first tracking reflects scope, validation, and handoff status.

## Validation

- bounded helper test or artifact validation
- `python -m json.tool` for generated JSON artifact if used
- `git diff --check`
