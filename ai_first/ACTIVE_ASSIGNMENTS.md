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
- Worktree: `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform`
- Task: Hide the right-panel mode and tool switcher on `/playground` while keeping the underlying capability logic intact
- Status: implementation complete
- Branch: `fix/playground-hide-mode-switcher`
- Task packet: `docs/superpowers/tasks/2026-04-30-playground-hide-mode-switcher.md`
- Owned files: `web/app/(workspace)/playground/page.tsx`, `web/components/chat/home/PlaygroundRightPanel.tsx`, `ai_first/ACTIVE_ASSIGNMENTS.md`, `ai_first/daily/2026-04-30.md`, `docs/superpowers/tasks/2026-04-30-playground-hide-mode-switcher.md`, `docs/superpowers/specs/2026-04-30-playground-hide-mode-switcher-design.md`, `docs/superpowers/pr-notes/2026-04-30-playground-hide-mode-switcher.md`
- PR: uncreated
- Last update: 2026-04-30
- Next action: write the bounded spec for removing the visible mode/tool chooser from the right panel before implementation
- Blocker: none

### Assignment

- Owner: Codex session
- Machine: local desktop
- Worktree: `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/code-review-graph-integration`
- Task: Install and integrate `code-review-graph` into this repository for Codex, including committing generated repo-local artifacts if the tool creates them
- Status: writing spec
- Branch: `fix/code-review-graph-integration`
- Task packet: `docs/superpowers/tasks/2026-04-30-code-review-graph-integration.md`
- Owned files: `.gitignore`, `.claude/skills/`, `.code-review-graph/`, `ai_first/ACTIVE_ASSIGNMENTS.md`, `ai_first/daily/2026-04-30.md`, `docs/superpowers/tasks/2026-04-30-code-review-graph-integration.md`, `docs/superpowers/specs/2026-04-30-code-review-graph-integration-design.md`, `docs/superpowers/plans/2026-04-30-code-review-graph-integration.md`, `docs/superpowers/pr-notes/2026-04-30-code-review-graph-integration.md`
- PR: uncreated
- Last update: 2026-04-30
- Next action: stage the bounded integration files, commit the lane, and prepare review handoff
- Blocker: none
