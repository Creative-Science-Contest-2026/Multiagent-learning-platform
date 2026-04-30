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
- Task: Hide the right-panel mode and tool switcher on `/playground` while keeping the underlying capability logic intact
- Status: writing spec
- Branch: `fix/playground-hide-mode-switcher`
- Task packet: `docs/superpowers/tasks/2026-04-30-playground-hide-mode-switcher.md`
- Owned files: `web/app/(workspace)/playground/page.tsx`, `web/components/chat/home/PlaygroundRightPanel.tsx`, `ai_first/ACTIVE_ASSIGNMENTS.md`, `ai_first/daily/2026-04-30.md`, `docs/superpowers/tasks/2026-04-30-playground-hide-mode-switcher.md`, `docs/superpowers/specs/2026-04-30-playground-hide-mode-switcher-design.md`, `docs/superpowers/pr-notes/2026-04-30-playground-hide-mode-switcher.md`
- PR: uncreated
- Last update: 2026-04-30
- Next action: write the bounded spec for removing the visible mode/tool chooser from the right panel before implementation
- Blocker: none
