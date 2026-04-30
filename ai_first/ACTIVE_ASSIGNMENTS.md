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
- Task: Add `Gói gia sư` selection and session binding for `/playground` chat using imported marketplace packs
- Status: writing spec
- Branch: `fix/playground-tutor-pack-chat`
- Task packet: `docs/superpowers/tasks/2026-04-30-playground-tutor-pack-chat.md`
- Owned files: `web/app/(workspace)/playground/page.tsx`, `web/context/UnifiedChatContext.tsx`, `web/components/sidebar/WorkspaceSidebar.tsx`, `web/lib/session-api.ts`, `web/lib/marketplace-api.ts`, `deeptutor/api/routers/sessions.py`, `deeptutor/services/session/turn_runtime.py`, `ai_first/ACTIVE_ASSIGNMENTS.md`, `ai_first/daily/2026-04-30.md`, `docs/superpowers/tasks/2026-04-30-playground-tutor-pack-chat.md`, `docs/superpowers/specs/2026-04-30-playground-tutor-pack-chat-design.md`, `docs/superpowers/pr-notes/2026-04-30-playground-tutor-pack-chat.md`
- PR: uncreated
- Last update: 2026-04-30
- Next action: write the bounded spec for binding each chat session to one imported `Gói gia sư`
- Blocker: none


### Assignment

- Owner: Codex session
- Machine: local desktop
- Worktree: `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/code-review-graph-integration`
- Task: Install and integrate `code-review-graph` into this repository for Codex, including committing generated repo-local artifacts if the tool creates them
- Status: writing spec
- Branch: `fix/code-review-graph-integration`
- Task packet: `docs/superpowers/tasks/2026-04-30-code-review-graph-integration.md`
- Owned files: `.gitignore`, `.claude/skills/`, `ai_first/ACTIVE_ASSIGNMENTS.md`, `ai_first/daily/2026-04-30.md`, `docs/superpowers/tasks/2026-04-30-code-review-graph-integration.md`, `docs/superpowers/specs/2026-04-30-code-review-graph-integration-design.md`, `docs/superpowers/plans/2026-04-30-code-review-graph-integration.md`, `docs/superpowers/pr-notes/2026-04-30-code-review-graph-integration.md`
- PR: uncreated
- Last update: 2026-04-30
- Next action: stage the bounded integration files, commit the lane, and prepare review handoff
- Blocker: none

### Assignment

- Owner: Codex session
- Machine: local desktop
- Worktree: `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/fix-knowledge-pack-wizard-redesign`
- Task: Redesign the `Gói kiến thức` screen into a wizard-first Vietnamese flow with FE notebook removal, hidden provider/model selection, and OpenAI-default indexing status
- Status: implemented, pending PR
- Branch: `fix/knowledge-pack-wizard-redesign`
- Task packet: `docs/superpowers/tasks/2026-04-30-knowledge-pack-wizard-redesign.md`
- Owned files: `web/app/(utility)/knowledge/page.tsx`, `web/locales/vi/app.json`, `web/locales/en/app.json`, `web/lib/notebook-api.ts`, `web/tests/contest-vietnamese-coverage.test.ts`, `ai_first/ACTIVE_ASSIGNMENTS.md`, `ai_first/daily/2026-04-30.md`, `docs/superpowers/tasks/2026-04-30-knowledge-pack-wizard-redesign.md`, `docs/superpowers/specs/2026-04-30-knowledge-pack-wizard-redesign-design.md`, `docs/superpowers/plans/2026-04-30-knowledge-pack-wizard-redesign.md`, `docs/superpowers/pr-notes/2026-04-30-knowledge-pack-wizard-redesign.md`
- PR: uncreated
- Last update: 2026-04-30
- Next action: stage the bounded runtime/docs diff and open the draft PR after optional FE dependency install for lint/build verification
- Blocker: none
