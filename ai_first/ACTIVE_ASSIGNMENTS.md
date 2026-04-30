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
- Worktree: `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/fix-teacher-dashboard-decision-flow`
- Task: Refactor the teacher dashboard into a decision-first intervention workflow with non-technical teacher-facing copy
- Status: implemented, pending PR
- Branch: `fix/teacher-dashboard-decision-flow`
- Task packet: `docs/superpowers/tasks/2026-04-30-teacher-dashboard-decision-flow.md`
- Owned files: `web/app/(workspace)/dashboard/page.tsx`, `web/components/dashboard/TeacherInsightPanel.tsx`, `web/components/dashboard/StudentInsightCard.tsx`, `web/components/dashboard/dashboard-presenters.ts`, `web/locales/vi/app.json`, `web/locales/en/app.json`, `web/tests/teacher-dashboard-copy.test.ts`, any focused dashboard shell/decision-flow tests added during implementation, `ai_first/ACTIVE_ASSIGNMENTS.md`, `ai_first/daily/2026-04-30.md`, `docs/superpowers/tasks/2026-04-30-teacher-dashboard-decision-flow.md`, `docs/superpowers/specs/2026-04-30-teacher-dashboard-decision-flow-design.md`, `docs/superpowers/plans/2026-04-30-teacher-dashboard-decision-flow.md`, `docs/superpowers/pr-notes/2026-04-30-teacher-dashboard-decision-flow.md`
- PR: uncreated
- Last update: 2026-04-30
- Next action: stage the bounded dashboard/docs diff and open a draft PR if requested
- Blocker: none

### Assignment

- Owner: Codex session
- Machine: local desktop
- Worktree: `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/fix-sidebar-shell-rebalance`
- Task: Rebalance the shared sidebar shell so chat history owns the middle space and the shell is wider
- Status: implemented, pending PR
- Branch: `fix/sidebar-shell-rebalance`
- Task packet: `docs/superpowers/tasks/2026-04-30-sidebar-shell-rebalance.md`
- Owned files: `web/components/sidebar/SidebarShell.tsx`, `web/components/SessionList.tsx`, `web/components/sidebar/nav-groups.ts`, `web/tests/sidebar-nav-groups.test.ts`, `web/tests/sidebar-shell-layout.test.ts`, `ai_first/ACTIVE_ASSIGNMENTS.md`, `ai_first/daily/2026-04-30.md`, `docs/superpowers/tasks/2026-04-30-sidebar-shell-rebalance.md`, `docs/superpowers/specs/2026-04-30-sidebar-shell-rebalance-design.md`, `docs/superpowers/plans/2026-04-30-sidebar-shell-rebalance.md`, `docs/superpowers/pr-notes/2026-04-30-sidebar-shell-rebalance.md`
- PR: uncreated
- Last update: 2026-04-30
- Next action: stage the bounded shell/docs diff and open a draft PR if requested
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

### Assignment

- Owner: Codex session
- Machine: local desktop
- Worktree: `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/fix-class-tutor-pack-flow`
- Task: Make class tutor setup feel like step 2 of the Knowledge Pack flow and bind each class tutor to one active Knowledge Pack
- Status: writing spec
- Branch: `fix/class-tutor-pack-flow`
- Task packet: `docs/superpowers/tasks/2026-04-30-class-tutor-pack-flow.md`
- Owned files: `web/app/(workspace)/agents/page.tsx`, `web/components/agents/SpecPackAuthoringTab.tsx`, `web/components/agents/class-tutor-pack-presenters.ts`, `web/lib/agent-spec-api.ts`, `web/lib/knowledge-api.ts`, `web/locales/en/app.json`, `web/locales/vi/app.json`, `web/tests/contest-terminology.test.ts`, `web/tests/class-tutor-pack-presenters.test.ts`, `deeptutor/api/routers/agent_specs.py`, `deeptutor/services/agent_spec/service.py`, `tests/api/test_agent_specs_router.py`, `tests/services/agent_spec/test_service.py`, `ai_first/ACTIVE_ASSIGNMENTS.md`, `ai_first/daily/2026-04-30.md`, `docs/superpowers/tasks/2026-04-30-class-tutor-pack-flow.md`, `docs/superpowers/specs/2026-04-30-class-tutor-pack-flow-design.md`, `docs/superpowers/plans/2026-04-30-class-tutor-pack-flow.md`, `docs/superpowers/pr-notes/2026-04-30-class-tutor-pack-flow.md`
- PR: uncreated
- Last update: 2026-04-30
- Next action: finish the bounded runtime spec for linking each class tutor to one knowledge pack before implementation planning
- Blocker: none
