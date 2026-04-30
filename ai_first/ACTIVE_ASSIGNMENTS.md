# Active Assignments

Use this file as the short-lived coordination board for active work.

Rules:

- Add an assignment before starting code work.
- One person should hold one active task at a time.
- Keep entries short and factual.
- Update the entry when blocked, paused, moved to review, or merged.
- Remove merged lanes from this board after merge. Keep merged history in `ai_first/daily/` plus task packets and PR notes.
- Docs-only terminal-state repair lanes do not need entries here; track them in their packet and daily log instead.

## Template

### Assignment

- Owner:
- Machine:
- Worktree:
- Task:
- Status:
- Branch:
- Task packet:
- Owned files:
- PR:
- Last update:
- Next action:
- Blocker:

## Active

### Assignment

- Owner: Codex session
- Machine: local desktop
- Worktree: `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/fix-chat-reasoning-wrap`
- Task: Fix `/playground` trace rendering so streamed `Reasoning` text no longer breaks into one-word-per-line blocks
- Status: ready for handoff
- Branch: `fix/chat-reasoning-wrap`
- Task packet: `docs/superpowers/tasks/2026-04-30-playground-reasoning-wrap-fix.md`
- Owned files: `web/app/(workspace)/playground/page.tsx`, `web/lib/playground-trace.ts`, `web/tests/playground-trace.test.ts`, `ai_first/ACTIVE_ASSIGNMENTS.md`, `ai_first/daily/2026-04-30.md`, `docs/superpowers/tasks/2026-04-30-playground-reasoning-wrap-fix.md`, `docs/superpowers/specs/2026-04-30-playground-reasoning-wrap-fix-design.md`, `docs/superpowers/pr-notes/2026-04-30-playground-reasoning-wrap-fix.md`
- PR: uncreated
- Last update: 2026-04-30
- Next action: stage the bounded diff and open a draft PR from the isolated worktree
- Blocker: none

### Assignment

- Owner: Codex session
- Machine: local desktop
- Worktree: `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform`
- Task: Add `Gói gia sư` selection and session binding for `/playground` chat using imported marketplace packs
- Status: writing spec
- Branch: `fix/playground-tutor-pack-chat`
- Task packet: `docs/superpowers/tasks/2026-04-30-playground-tutor-pack-chat.md`
- Owned files: `web/app/(workspace)/playground/page.tsx`, `web/context/UnifiedChatContext.tsx`, `web/components/sidebar/WorkspaceSidebar.tsx`, `web/lib/session-api.ts`, `web/lib/marketplace-api.ts`, `deeptutor/api/routers/sessions.py`, `deeptutor/services/session/turn_runtime.py`, `ai_first/ACTIVE_ASSIGNMENTS.md`, `ai_first/daily/2026-04-30.md`, `docs/superpowers/tasks/2026-04-30-playground-tutor-pack-chat.md`, `docs/superpowers/specs/2026-04-30-playground-tutor-pack-chat-design.md`, `docs/superpowers/pr-notes/2026-04-30-playground-tutor-pack-chat.md`
- PR: uncreated
- Last update: 2026-04-30
- Next action: write the bounded spec for binding each chat session to one imported `Gói gia sư`
- Blocker: none
