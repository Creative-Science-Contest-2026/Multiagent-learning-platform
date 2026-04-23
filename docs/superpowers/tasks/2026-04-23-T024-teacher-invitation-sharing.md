# Feature Pod Task: Teacher Team Invitation & Sharing

Owner: Codex
Branch: `pod-a/t024-teacher-invitation-sharing`
GitHub Issue: `#71`

## Goal

Add an MVP team-sharing workflow so teachers can record collaborators and pending invitations for a knowledge pack from the existing teacher workspace.

## User-visible outcome

- Teachers can add team members and pending invite emails while creating or editing a knowledge pack.
- Team-sharing details are visible in the knowledge pack management UI.
- Existing private/team/public sharing controls remain intact.

## Owned files/modules

- `web/app/(utility)/knowledge/page.tsx`
- `web/lib/knowledge-api.ts`
- `deeptutor/api/routers/knowledge.py`
- `tests/api/test_knowledge_router.py`
- `docs/superpowers/tasks/2026-04-23-T024-teacher-invitation-sharing.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-23.md`

## Do-not-touch files/modules

- Marketplace, dashboard, tutor, and settings files
- `deeptutor/core/`
- `deeptutor/runtime/`
- Root license and upstream attribution files

## API/data contract

- Extend the existing knowledge-base config metadata contract instead of introducing a new backend route family in this slice.
- Keep current knowledge-base config updates backward-compatible.
- Treat team members and pending invites as metadata lists stored with the teacher pack config.

## Acceptance criteria

- Teachers can record collaborator names and invite emails for a team-shared knowledge pack.
- Knowledge pack details clearly display current collaborators and pending invitations.
- Existing sharing status flows continue to work with the new metadata fields.

## Required tests

- Knowledge router regression coverage for the new metadata fields
- Frontend production build verification

## Manual verification

- Create or edit a knowledge pack with sharing status `team`
- Add team members and invitation emails
- Save the pack and confirm the values persist in the UI

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.

## Handoff notes

- `T023` merged to `main` through PR `#70`.
- Start from the existing teacher-pack metadata flow in `web/app/(utility)/knowledge/page.tsx` and `deeptutor/api/routers/knowledge.py`.
- Keep this slice lightweight: model collaboration state first, not outbound email delivery or full access-control enforcement.
