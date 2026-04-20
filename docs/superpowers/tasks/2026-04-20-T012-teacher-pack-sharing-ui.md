# Feature Pod Task: Teacher Knowledge Pack Sharing UI

Owner: Codex
Branch: `pod-a/t012-pack-sharing-ui`
GitHub Issue: `#50`

## Goal

Add teacher-facing controls to mark knowledge packs as `private`, `team`, or `public`, and persist those sharing settings through the existing knowledge metadata update flow.

## User-visible outcome

- Teachers can inspect and edit sharing visibility from the Knowledge Pack page.
- Sharing status changes persist and become visible to the marketplace flow.
- Validation and save errors are surfaced in the page instead of failing silently.

## Owned files/modules

- `web/app/(utility)/knowledge/page.tsx`
- `web/lib/knowledge-api.ts`
- `deeptutor/api/routers/knowledge.py`
- `docs/superpowers/tasks/2026-04-20-T012-teacher-pack-sharing-ui.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-20.md`

## Do-not-touch files/modules

- `deeptutor/core/`
- `deeptutor/runtime/`
- Unrelated marketplace, dashboard, and tutoring files
- Root license and upstream attribution files

## API/data contract

- Reuse the existing knowledge config update path:
  - `PUT /api/v1/knowledge/{kb_name}/config`
- Keep `sharing_status` restricted to `private`, `team`, or `public`
- Preserve existing teacher pack metadata fields:
  - `subject`
  - `grade`
  - `curriculum`
  - `learning_objectives`
  - `owner`

## Acceptance criteria

- Knowledge Pack UI shows the current sharing status for an editable pack.
- Teacher can save `private`, `team`, or `public` from the edit flow.
- Save path uses the existing metadata update API client and backend validation.
- Page shows success/error feedback for sharing updates.
- Relevant task tracking mirrors are updated before implementation continues.

## Required tests

- Frontend validation/build checks for touched files
- Backend syntax or targeted route validation for touched Python files

## Manual verification

- Open Knowledge Pack page.
- Edit a pack with metadata.
- Change sharing status and save.
- Reload list and confirm the new sharing status persists.

## PR architecture note

- Must include Mermaid diagram.
- Must update `ai_first/architecture/MAIN_SYSTEM_MAP.md` if feature structure changes.
- Expected: update the system map only if the sharing UI introduces a new user-facing workflow node.

## Handoff notes

- This task follows merged PR `#44` and continues strict registry order on `main`.
- Backend validation for `sharing_status` already exists; the likely gap is user-facing editability and save-state handling in the knowledge page.
