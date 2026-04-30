# Task Packet: Playground Tutor Pack Chat

- Task ID: `UI-PLAYGROUND-TUTOR-PACK-CHAT`
- Date: 2026-04-30
- Branch: `fix/playground-tutor-pack-chat`
- Status: Spec written

## Objective

Add `Gói gia sư` selection and session binding to `/playground` chat so each chat session is locked to one imported marketplace tutor pack from creation through history restore.

## User-Approved Scope

- user-facing entity is `Gói gia sư`
- each chat session is locked to one tutor pack from the start
- if only one imported tutor pack exists, auto-select it
- if multiple exist, require explicit selection before first send
- session history must restore the same tutor pack
- if the pack later becomes unavailable, history stays visible but sending is blocked
- sidebar should show a small tutor-pack badge for each session

## Owned Files

- `web/app/(workspace)/playground/page.tsx`
- `web/context/UnifiedChatContext.tsx`
- `web/components/sidebar/WorkspaceSidebar.tsx`
- `web/lib/session-api.ts`
- `web/lib/marketplace-api.ts`
- `deeptutor/api/routers/sessions.py`
- `deeptutor/services/session/turn_runtime.py`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-playground-tutor-pack-chat.md`
- `docs/superpowers/specs/2026-04-30-playground-tutor-pack-chat-design.md`
- `docs/superpowers/pr-notes/2026-04-30-playground-tutor-pack-chat.md`

## Do-Not-Touch

- capability removal/hiding lane beyond what already exists
- marketplace authoring model
- unrelated untracked files in repo root

## Design Before Implementation

- `docs/superpowers/specs/2026-04-30-playground-tutor-pack-chat-design.md`

## Validation Plan

- `cd web && npx eslint "app/(workspace)/playground/page.tsx" "context/UnifiedChatContext.tsx" "components/sidebar/WorkspaceSidebar.tsx" "lib/session-api.ts"`
- `cd web && npm run build`
- backend-targeted verification if implementation touches session preference persistence
- `git diff --check`
