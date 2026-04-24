# Feature Pod Task: Knowledge Pack Versioning System

Owner: Codex
Branch: `pod-a/t032-kb-versioning`
GitHub Issue: `#85`

## Goal

Add a lightweight versioning slice for knowledge packs so teachers can update pack content without losing visibility into what changed.

## User-visible outcome

- Knowledge packs can preserve a simple version marker or revision history when updated.
- Existing pack creation, editing, and import flows remain backward-compatible when version history is absent.
- The first slice should be small enough to avoid schema churn beyond what is required for meaningful change tracking.

## Owned files/modules

- `deeptutor/knowledge/`
- `deeptutor/api/routers/knowledge.py` only if the existing metadata/update flow needs a small extension
- `web/app/(utility)/knowledge/` only if the first useful slice needs explicit teacher-facing version visibility
- `web/lib/knowledge-api.ts` only if API typing changes are required
- `tests/` covering the selected versioning slice
- `docs/superpowers/tasks/2026-04-24-T032-knowledge-pack-versioning.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-24.md`

## Do-not-touch files/modules

- Marketplace, dashboard, tutor follow-up, and assessment review flows
- Unrelated API routers and session history code
- `deeptutor/core/`
- `deeptutor/runtime/`
- Root license and upstream attribution files

## API/data contract

- Preserve current knowledge pack behavior when version history does not exist.
- Prefer extending existing pack metadata/update contracts over introducing a separate versioning route family for this first slice.
- Keep the first slice compatible with imported marketplace packs and existing teacher-managed packs.

## Acceptance criteria

- Updating a knowledge pack can record at least one useful version/revision marker.
- Existing pack flows remain clean when no version history exists.
- Regression coverage exists for the chosen versioning behavior.

## Required tests

- Knowledge-pack regression coverage for the selected versioning path
- Frontend production build verification only if teacher UI or API typing changes are made

## Manual verification

- Update a knowledge pack twice and confirm the selected version marker/history reflects the change
- Confirm older packs without version metadata still load and edit cleanly

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.

## Handoff notes

- `T031` merged to `main` through PR `#84`.
- Start by reading the existing knowledge metadata/update flow and keep the first slice as small as possible before considering any UI work.
