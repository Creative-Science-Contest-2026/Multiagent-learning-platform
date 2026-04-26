# Feature Pod Task: Lane 1 Agent Spec Authoring

Task ID: `L1_AGENT_SPEC_AUTHORING`
Commit tag: `L1`
Owner: Session-specific
Branch: `pod-a/agent-spec-authoring`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Create the teacher-facing authoring layer for the Markdown Agent Spec Pack without collapsing policy into runtime code.

## User-visible outcome

- Teachers can author the high-leverage parts of a teaching agent through a narrow UI.
- The source of truth remains a versionable Markdown spec pack.
- Authoring output is ready for later runtime compilation rather than being trapped in UI state.

## Owned files/modules

- `web/app/(workspace)/agents/`
- `web/components/agents/`
- `web/lib/agent-spec-api.ts`
- `deeptutor/api/routers/agent_specs.py`
- `deeptutor/services/agent_spec/`
- `tests/api/test_agent_specs_router.py`
- `tests/services/agent_spec/`
- `docs/superpowers/tasks/2026-04-26-lane-1-agent-spec-authoring.md`
- `docs/superpowers/pr-notes/*`

## Do-not-touch files/modules

- `deeptutor/services/evidence/`
- `deeptutor/api/routers/assessment.py`
- `deeptutor/api/routers/dashboard.py`
- `deeptutor/services/session/`
- `web/app/(workspace)/dashboard/`
- `web/components/dashboard/`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` unless the authoring surface materially changes the system map

## API/data contract

- Define the canonical spec-pack storage contract under an `agent_specs/<agent_id>/` boundary.
- Keep Markdown as the persisted source of truth even if the UI edits structured subsets of the pack.
- Defer runtime assembly to Lane 2; this lane only produces clean authoring artifacts and metadata.

## Acceptance criteria

- `IDENTITY`, `SOUL`, and `RULES` have a narrow structured authoring surface.
- The remaining pack files can be edited without breaking Markdown fidelity.
- The authored pack is versionable and exportable.
- The lane does not hardcode tutoring or diagnosis behavior into the UI layer.

## Required tests

- Focused router/service tests for spec pack create, update, validate, and export flows
- Frontend lint/build checks for authoring screens
- `git diff --check`

## Manual verification

- Create one sample teacher agent pack end to end.
- Edit `IDENTITY`, `SOUL`, and `RULES`, then verify the stored Markdown remains readable and intact.
- Export the pack and verify the file set matches the agreed Markdown standard.

## Parallel-work notes

- This session owns only authoring and storage concerns for the teacher spec pack.
- Do not implement runtime prompt assembly here; hand off compiled-pack consumption to Lane 2.
- If authoring raises a runtime ambiguity, stop and ask the human rather than inventing a hidden contract.
- If another session is already editing the same authoring directories, ask the human to resolve the conflict before proceeding.

## PR architecture note

- Must include Mermaid diagram.
- Update `ai_first/architecture/MAIN_SYSTEM_MAP.md` only if the authoring surface becomes part of the shipped system map.

## Handoff notes

- This is Session = Lane 1.
- Read `docs/superpowers/specs/2026-04-26-contest-mvp-hybrid-lanes-design.md` before implementation.
- Coordinate with Lane 2 only through explicit file/API contracts, not by shared unstated assumptions.
- Current implementation path: `web/app/(workspace)/agents/page.tsx` now hosts a dedicated spec-pack authoring tab backed by `/api/v1/agent-specs`.
- Storage contract: save current Markdown files under `data/user/workspace/agent_specs/<agent_id>/` and snapshot each save into `versions/vNNNN/`.
