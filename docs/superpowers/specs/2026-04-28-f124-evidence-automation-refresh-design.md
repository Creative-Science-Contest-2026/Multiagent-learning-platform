# F124 Design: Evidence Automation Refresh

## Goal

Automate the command-backed portion of contest evidence refresh so the validated-prototype claim is easier to maintain without pretending screenshots or video can be fully automated.

## Approach

Chosen approach: `wrapper script + generated status artifact`.

Why:

- a wrapper alone still leaves humans and AI workers to manually summarize status
- full screenshot or video automation is out of scope and not reliable in this environment
- a status artifact gives later docs lanes and AI workers one structured source for evidence freshness

## Scope

### In scope

- add a bounded orchestration helper under `scripts/contest/`
- run the existing demo-reset path plus selected command-backed checks
- generate a machine-readable artifact under `ai_first/evidence/`
- update contest docs to use the artifact as the source-of-truth for command-backed evidence refresh
- add a bounded test for helper output shape or execution-plan assembly

### Out of scope

- browser screenshot automation
- optional video automation
- changing proof level or product claims
- modifying runtime product behavior

## Artifact Set

- `scripts/contest/refresh_evidence_status.py`
- `ai_first/evidence/evidence_status.json`
- bounded test under `tests/`
- doc refresh in `docs/contest/`

## Command Coverage

The first automation pass should cover:

- demo reset command
- system status endpoint
- knowledge list endpoint
- dashboard overview endpoint
- dashboard recent endpoint
- contest assessment session fetch
- contest tutor session fetch
- optional frontend build check behind an explicit flag

## Data Shape

The generated artifact should include:

- `generated_at`
- `api_base`
- `project_root`
- `checks`
- per-check fields:
  - `name`
  - `command`
  - `status`
  - `summary`
  - `manual_followup_required`

## Documentation Behavior

Contest docs should explain:

- command-backed evidence can be refreshed with the helper
- screenshot and video evidence remain manual
- the helper updates operational repeatability, not the product's proof level

## Architecture Impact

- no runtime architecture change
- no `ai_first/architecture/MAIN_SYSTEM_MAP.md` update expected unless the helper becomes part of a broader persistent ops architecture later
