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
- Worktree: `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/fix-backend-test-coverage-gate`
- Task: Publish the bounded task packet and design spec for a frontend `80%` coverage gate on the teacher-first contest path
- Status: spec written
- Branch: `docs/frontend-test-coverage-gate-task`
- Task packet: `docs/superpowers/tasks/2026-05-02-frontend-test-coverage-gate.md`
- Owned files: `docs/superpowers/tasks/2026-05-02-frontend-test-coverage-gate.md`, `docs/superpowers/specs/2026-05-02-frontend-test-coverage-gate-design.md`, `ai_first/TASK_REGISTRY.json`, `ai_first/ACTIVE_ASSIGNMENTS.md`, `ai_first/daily/2026-05-02.md`
- PR: uncreated
- Last update: 2026-05-02
- Next action: validate the new task artifacts, then hand off the packet for a dedicated frontend implementation lane
- Blocker: none

### Assignment

- Owner: Codex session
- Machine: local desktop
- Worktree: `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/fix-demo-seed-vietnamese-refresh`
- Task: Localize seeded demo content to Vietnamese and make the cleanup-before-reseed step explicit so repeated mock runs never accumulate duplicate demo data
- Status: implemented, pending PR
- Branch: `fix/demo-seed-vietnamese-refresh`
- Task packet: `docs/superpowers/tasks/2026-05-01-demo-seed-vietnamese-refresh.md`
- Owned files: `scripts/contest/reset_demo_data.py`, `tests/scripts/test_reset_demo_data.py`, `docs/contest/DEMO_DATA_RESET.md`, `docs/superpowers/tasks/2026-05-01-demo-seed-vietnamese-refresh.md`, `docs/superpowers/specs/2026-05-01-demo-seed-vietnamese-refresh-design.md`, `docs/superpowers/pr-notes/2026-05-01-demo-seed-vietnamese-refresh.md`, `ai_first/ACTIVE_ASSIGNMENTS.md`, `ai_first/daily/2026-05-01.md`
- PR: uncreated
- Last update: 2026-05-01
- Next action: stage the bounded seed/docs diff, commit, and open a draft PR if requested
- Blocker: none

### Assignment

- Owner: Codex session
- Machine: local desktop
- Worktree: `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/fix-demo-realistic-seed-data`
- Task: Expand the local contest demo seed so every core teacher-first screen has realistic, diverse, demo-safe data for video capture
- Status: implemented, pending PR
- Branch: `fix/demo-realistic-seed-data`
- Task packet: `docs/superpowers/tasks/2026-04-30-demo-realistic-seed-data.md`
- Owned files: `scripts/contest/reset_demo_data.py`, `tests/scripts/test_reset_demo_data.py`, `docs/contest/DEMO_DATA_RESET.md`, `docs/contest/SMOKE_RUNBOOK.md`, `docs/superpowers/tasks/2026-04-30-demo-realistic-seed-data.md`, `docs/superpowers/specs/2026-04-30-demo-realistic-seed-data-design.md`, `docs/superpowers/pr-notes/2026-04-30-demo-realistic-seed-data.md`, `ai_first/ACTIVE_ASSIGNMENTS.md`, `ai_first/daily/2026-04-30.md`, `ai_first/AI_OPERATING_PROMPT.md` only if repo-level operating guidance changes
- PR: uncreated
- Last update: 2026-04-30
- Next action: run final verification, commit the lane, open a draft PR, then merge once CI is green
- Blocker: none

### Assignment

- Owner: Codex session
- Machine: local desktop
- Worktree: `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/fix-marketplace-dashboard-fetch-recovery`
- Task: Recover marketplace and teacher-dashboard fetch paths, then harden the related error-state layout for the contest UI
- Status: implemented, pending PR
- Branch: `fix/marketplace-dashboard-fetch-recovery`
- Task packet: `docs/superpowers/tasks/2026-04-30-marketplace-dashboard-fetch-recovery.md`
- Owned files: `web/app/(utility)/marketplace/page.tsx`, `web/app/(workspace)/dashboard/page.tsx`, `web/components/agents/SpecPackAuthoringTab.tsx`, `web/lib/marketplace-api.ts`, `web/lib/dashboard-api.ts`, `deeptutor/api/routers/marketplace.py`, `deeptutor/api/routers/dashboard.py`, `web/tests/*marketplace*`, `web/tests/*dashboard*`, `web/tests/api-base-url.test.ts`, `web/tests/agents-boolean-field-layout.test.ts`, `tests/api/test_marketplace_router.py`, `tests/api/test_dashboard_router.py`, `ai_first/ACTIVE_ASSIGNMENTS.md`, `ai_first/daily/2026-04-30.md`, `docs/superpowers/tasks/2026-04-30-marketplace-dashboard-fetch-recovery.md`, `docs/superpowers/pr-notes/2026-04-30-marketplace-dashboard-fetch-recovery.md`
- PR: `#271`
- Last update: 2026-04-30
- Next action: wait for review or move the draft PR to Ready after any final self-review updates
- Blocker: none

### Assignment

- Owner: Codex session
- Machine: local desktop
- Worktree: `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/fix-knowledge-progress-persistence`
- Task: Fix knowledge-pack progress persistence so status/index results survive config updates and recover from stale KB config entries
- Status: implemented, pending PR
- Branch: `fix/knowledge-progress-persistence`
- Task packet: `docs/superpowers/tasks/2026-04-30-knowledge-progress-persistence.md`
- Owned files: `deeptutor/services/config/knowledge_base_config.py`, `deeptutor/knowledge/manager.py`, `deeptutor/knowledge/progress_tracker.py`, `deeptutor/api/routers/knowledge.py`, `tests/api/test_knowledge_router.py`, `tests/knowledge/test_progress_tracker.py`, `ai_first/ACTIVE_ASSIGNMENTS.md`, `ai_first/daily/2026-04-30.md`, `docs/superpowers/tasks/2026-04-30-knowledge-progress-persistence.md`, `docs/superpowers/specs/2026-04-30-knowledge-progress-persistence-design.md`, `docs/superpowers/plans/2026-04-30-knowledge-progress-persistence.md`, `docs/superpowers/pr-notes/2026-04-30-knowledge-progress-persistence.md`
- PR: `#270`
- Last update: 2026-04-30
- Next action: sync the lane cleanly, then merge once CI is green
- Blocker: none

### Assignment

- Owner: Codex session
- Machine: local desktop
- Worktree: `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/fix-settings-hide-runtime-config`
- Task: Hide runtime LLM/embedding/search configuration from the end-user settings page and move active runtime values to local `.env`
- Status: implemented, pending PR
- Branch: `fix/settings-hide-runtime-config`
- Task packet: `docs/superpowers/tasks/2026-04-30-settings-hide-runtime-config.md`
- Owned files: `web/app/(utility)/settings/page.tsx`, `web/tests/settings-page-runtime-privacy.test.ts`, `ai_first/ACTIVE_ASSIGNMENTS.md`, `ai_first/daily/2026-04-30.md`, `docs/superpowers/tasks/2026-04-30-settings-hide-runtime-config.md`, `docs/superpowers/specs/2026-04-30-settings-hide-runtime-config-design.md`, `docs/superpowers/plans/2026-04-30-settings-hide-runtime-config.md`, `docs/superpowers/pr-notes/2026-04-30-settings-hide-runtime-config.md`, local-only `.env`
- PR: uncreated
- Last update: 2026-04-30
- Next action: self-review the settings shell diff, then open a draft PR
- Blocker: targeted eslint in this worktree cannot resolve `eslint-config-next`

### Assignment

- Owner: Codex session
- Machine: local desktop
- Worktree: `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/fix-agents-tutor-setup-cleanup`
- Task: Clean up only the `Gia sư lớp học / Tutor setup` tab on `/agents` for production-ready teacher UX
- Status: implemented, pending PR
- Branch: `fix/agents-tutor-setup-cleanup`
- Task packet: `docs/superpowers/tasks/2026-04-30-agents-tutor-setup-cleanup.md`
- Owned files: `web/components/agents/SpecPackAuthoringTab.tsx`, `web/components/agents/class-tutor-pack-presenters.ts`, `web/components/sidebar/WorkspaceSidebar.tsx`, `web/components/sidebar/SidebarShell.tsx`, `web/app/(workspace)/agents/page.tsx`, `web/locales/vi/app.json`, `web/locales/en/app.json`, `web/tests/contest-terminology.test.ts`, `ai_first/ACTIVE_ASSIGNMENTS.md`, `ai_first/daily/2026-04-30.md`, `docs/superpowers/tasks/2026-04-30-agents-tutor-setup-cleanup.md`, `docs/superpowers/specs/2026-04-30-agents-tutor-setup-cleanup-design.md`, `docs/superpowers/pr-notes/2026-04-30-agents-tutor-setup-cleanup.md`
- PR: `#268`
- Last update: 2026-04-30
- Next action: sync the lane cleanly, then merge once CI is green
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
