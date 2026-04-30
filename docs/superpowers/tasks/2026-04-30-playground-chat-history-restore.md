# Task Packet: Playground Chat History Restore

- Task ID: `BUG-PLAYGROUND-CHAT-HISTORY-RESTORE`
- Date: 2026-04-30
- Branch: `fix/playground-chat-history-restore`
- Status: Spec written

## Objective

Fix the regression where selecting a previous chat session in the sidebar no longer restores that conversation inside `/playground`.

## User-Approved Scope

- restore history loading for the standard `chat` mode on `/playground`
- do not hide or remove `Giải sâu`, `Nghiên cứu sâu`, or other capabilities in this lane
- capability hiding is deferred to the next task

## Owned Files

- `web/app/(workspace)/playground/page.tsx`
- `web/context/UnifiedChatContext.tsx`
- `web/components/chat/home/ChatMessages.tsx`
- `web/components/chat/home/ChatComposer.tsx`
- `web/components/sidebar/WorkspaceSidebar.tsx`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-playground-chat-history-restore.md`
- `docs/superpowers/specs/2026-04-30-playground-chat-history-restore-design.md`
- `docs/superpowers/pr-notes/2026-04-30-playground-chat-history-restore.md`

## Do-Not-Touch

- backend session APIs
- capability-hiding work for the next lane
- unrelated untracked files

## Design Before Implementation

- `docs/superpowers/specs/2026-04-30-playground-chat-history-restore-design.md`

## Validation Plan

- `cd web && npx eslint "app/(workspace)/playground/page.tsx"`
- `cd web && npm run build`
- `cd /Users/nguyenhuuloc/Documents/Multiagent-learning-platform && git diff --check`
