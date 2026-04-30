# Task Packet: Agents Tutor Setup Cleanup

- Task ID: `UI_AGENTS_TUTOR_SETUP_CLEANUP`
- Commit tag: `UI-AGENTS-TUTOR`
- Date: 2026-04-30
- Branch: `fix/agents-tutor-setup-cleanup`
- Worktree: `.worktrees/fix-agents-tutor-setup-cleanup`
- Status: Implemented

## Objective

Clean up only the `Gia sư lớp học / Tutor setup` tab on `/agents` so it feels production-ready for non-technical teachers, while leaving the other `/agents` tabs unchanged.

## User-Approved Scope

- only the `Gia sư lớp học / Tutor setup` tab
- fix items `1-10` from the reviewed UI audit
- do not redesign:
  - sticky section tabs
  - status-pill polish for `Phiên bản`
- do not expand into the other `/agents` tabs:
  - `Class tutors`
  - `Tutor files`
  - `Teaching styles`

## Owned Files

- `web/components/agents/SpecPackAuthoringTab.tsx`
- `web/components/agents/class-tutor-pack-presenters.ts`
- `web/components/sidebar/WorkspaceSidebar.tsx`
- `web/components/sidebar/SidebarShell.tsx`
- `web/app/(workspace)/agents/page.tsx`
- `web/locales/vi/app.json`
- `web/locales/en/app.json`
- `web/tests/contest-terminology.test.ts`
- any new focused `/agents` UI tests added for this cleanup
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-agents-tutor-setup-cleanup.md`
- `docs/superpowers/specs/2026-04-30-agents-tutor-setup-cleanup-design.md`
- `docs/superpowers/plans/2026-04-30-agents-tutor-setup-cleanup.md`
- `docs/superpowers/pr-notes/2026-04-30-agents-tutor-setup-cleanup.md`

## Do-Not-Touch

- `BotsTab`, `ProfilesTab`, and `SoulsTab` behavior except if copy/shell wiring absolutely requires a bounded route-level adjustment
- backend agent-spec APIs unless the HTML-entity bug is proven to come from the server payload path
- tutor runtime chat page under `/agents/[botId]/chat`
- knowledge-page and dashboard-page implementation lanes
- lockfiles unless dependency changes are required

## Design before implementation

- Runtime behavior change: yes
- Approved design source:
  - user-approved cleanup scope captured in the session and to be written into the dedicated spec below
- Current behavior:
  - the tutor-setup tab still exposes dev/runtime tooling, file-system terminology, a chat-history-heavy sidebar, duplicate pack summaries, weak empty states, and low-context actions
- Intended behavior change:
  - the tab should read like a production teacher-facing setup flow and remove internal/debug affordances from the default surface
- Candidate approach A:
  - fix only the visibly broken controls and strings
- Candidate approach B:
  - complete production UX cleanup for the tutor-setup tab only, covering items `1-10` while leaving tabs `11-12` for a later PR
- Chosen approach and reason:
  - approach B; it fixes the real teacher-facing problems without widening into a full `/agents` redesign

## Required code reading

- Entry points/handlers to inspect:
  - `web/app/(workspace)/agents/page.tsx`
- Primary logic/service/use-case modules to inspect:
  - `web/components/agents/SpecPackAuthoringTab.tsx`
  - `web/components/agents/class-tutor-pack-presenters.ts`
- Shared contracts/schemas/types to inspect:
  - linked-pack presenter and save/export button state logic
- Adjacent or reused flows to inspect:
  - `/agents` route shell behavior
  - sidebar history behavior on this route
  - current section-title and field-label patterns already used in the tab
- Existing tests to inspect:
  - `web/tests/contest-terminology.test.ts`
  - any existing `/agents` source-level tests

## Impact surface and stop conditions

- Expected affected areas:
  - tutor-setup section titles
  - linked-pack selector
  - field control types and labeling
  - empty state and action semantics
  - route sidebar behavior on `/agents`
  - dev-only runtime panel visibility
- Files/modules likely to change:
  - `SpecPackAuthoringTab`
  - `class-tutor-pack-presenters`
  - `SidebarShell` and/or `WorkspaceSidebar` only as needed for `/agents` route shell behavior
  - locale files and focused tests
- Files/modules that must be reviewed even if they remain unchanged:
  - `/agents` route container
  - the non-tutor tabs in `/agents`
  - backend payload path for the escaped curriculum content
- Minimum validation paths before the task can stop:
  - `/agents` no longer shows chat history in the sidebar
  - tutor setup no longer shows runtime-policy audit on production surface
  - section titles no longer leak file names like `IDENTITY.md`
  - `Không giải hộ trực tiếp` is a boolean toggle
  - linked-pack duplicate summary block is removed from the top form
  - save/export actions read clearly and have sensible disabled states
- What would count as a shallow fix for this task:
  - translating strings while leaving debug tooling, duplicate summary blocks, and broken control semantics visible

## Acceptance criteria

- the tutor-setup tab alone feels production-ready for a non-technical teacher
- items `1-10` from the reviewed audit are resolved
- items `11-12` remain explicitly out of scope for this lane
- the other `/agents` tabs remain functionally unchanged

## Required tests

- focused `/agents` source-level or presenter tests for the cleaned shell/text/control behavior
- targeted eslint on the touched `/agents` and sidebar files
- `cd web && npm run build`

## Manual verification

- open `/agents`
- stay only on `Gia sư lớp học / Tutor setup`
- confirm no chat history in the sidebar for this route
- confirm no dev/runtime audit panel on production surface
- confirm curriculum content no longer shows literal `&lt;br&gt;`
- confirm the pack selector, empty state, and actions read clearly

## Implementation notes

- `/agents` already inherited the business shell mode from the merged `business-shell-focus` lane, so this cleanup confirmed the route contract and intentionally left `WorkspaceSidebar` and `SidebarShell` unchanged.
- The runtime-policy audit panel is now development-only, which removes teacher-facing debug exposure without deleting the audit utility for local engineering work.
- `IDENTITY.md`, `SOUL.md`, and `RULES.md` are replaced by teacher-facing section labels, and manual markdown tabs/preview headings now translate the file names instead of leaking raw internals.
- `Không giải hộ trực tiếp` now uses an explicit boolean switch while preserving the existing serialized `yes` / `no` contract.
- The linked-pack flow now uses a searchable picker, a first-time-teacher empty state, clear `Xuất cấu hình` / `Lưu & tạo gia sư` actions, and decoded markdown content so escaped entities no longer show up literally.

## Verification run

- `cd web && node --test tests/contest-terminology.test.ts tests/class-tutor-pack-presenters.test.ts tests/sidebar-shell-layout.test.ts tests/sidebar-nav-groups.test.ts`
- `cd web && npx eslint 'app/(workspace)/agents/page.tsx' 'components/agents/SpecPackAuthoringTab.tsx' 'components/agents/class-tutor-pack-presenters.ts' 'components/sidebar/SidebarShell.tsx' 'components/sidebar/WorkspaceSidebar.tsx' 'tests/contest-terminology.test.ts' 'tests/class-tutor-pack-presenters.test.ts' 'tests/sidebar-shell-layout.test.ts' 'tests/sidebar-nav-groups.test.ts'`
- `cd web && npm run build`
- `git diff --check`

## Handoff notes

- The deferred out-of-scope items remain unchanged: sticky section tabs and status-pill polish for the version row.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` was reviewed and did not require an update because this lane only changes presentation within the existing `/agents` tutor-setup flow.

## Parallel-work notes

- This lane uses a dedicated worktree because the repo root is already occupied by the `/playground` tutor-pack lane.
- The merged `fix/class-tutor-pack-flow` lane is not reused because this cleanup has a different bounded scope and a different owned-file contract.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` likely does not need an update unless the teacher-facing route map or major workflow structure changes.
