# Task Packet: Business Shell Focus

- Task ID: `UI_BUSINESS_SHELL_FOCUS`
- Commit tag: `UI-BIZ-SHELL`
- Date: 2026-04-30
- Branch: `fix/business-shell-focus`
- Worktree: `.worktrees/fix-business-shell-focus`
- Status: Implemented, pending PR

## Objective

Create a business-facing shell mode that keeps product navigation but removes chat history as the dominant sidebar middle area on non-chat routes such as `Gói kiến thức`, `Bảng điều khiển giáo viên`, and teacher-facing setup screens.

## User-Approved Scope

- keep the shared product sidebar
- preserve the chat-first shell on `/playground`
- make business/task pages visually focused and less chat-centric
- establish shared business-route shell primitives that downstream pages can reuse

## Owned Files

- `web/components/sidebar/SidebarShell.tsx`
- `web/components/sidebar/WorkspaceSidebar.tsx`
- any route-level shell selection point that decides chat mode vs business mode
- `web/tests/sidebar-shell-layout.test.ts`
- `web/tests/sidebar-nav-groups.test.ts`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-business-shell-focus.md`
- `docs/superpowers/specs/2026-04-30-business-shell-focus-design.md`
- `docs/superpowers/plans/2026-04-30-business-shell-focus.md`
- `docs/superpowers/pr-notes/2026-04-30-business-shell-focus.md`

## Do-Not-Touch

- `web/app/(utility)/knowledge/page.tsx` except for shell wiring if the chosen implementation requires a route-level mode flag
- `web/app/(workspace)/dashboard/page.tsx` except for shell wiring if required
- backend session/chat runtime
- unrelated `/playground` message or composer behavior
- lockfiles unless dependency changes are required

## Design before implementation

- Runtime behavior change: yes
- Approved spec:
  - `docs/superpowers/specs/2026-04-30-business-shell-focus-design.md`
- Current behavior:
  - business routes inherit a sidebar where chat history competes with the main task area
- Intended behavior change:
  - chat history remains dominant only on chat-first routes; business routes use a calmer, nav-first shell mode
- Candidate approach A:
  - route-local suppression of history
- Candidate approach B:
  - explicit shell distinction between chat workspace and business workspace
- Chosen approach and reason:
  - approach B; it creates the correct reusable boundary instead of page-by-page overrides

## Required code reading

- Entry points/handlers to inspect:
  - `web/components/sidebar/WorkspaceSidebar.tsx`
  - `web/components/sidebar/SidebarShell.tsx`
- Primary logic/service/use-case modules to inspect:
  - any current shell-mode or sidebar-layout selection logic
- Shared contracts/schemas/types to inspect:
  - shell props passed into `SidebarShell`
  - session-list integration points
- Adjacent or reused flows to inspect:
  - `/playground` shell behavior
  - any route already varying shell density or layout
- Existing tests to inspect:
  - `web/tests/sidebar-shell-layout.test.ts`
  - `web/tests/sidebar-nav-groups.test.ts`

## Impact surface and stop conditions

- Expected affected areas:
  - shared sidebar layout
  - history visibility rules
  - shell-mode selection for business routes
- Files/modules likely to change:
  - `SidebarShell`
  - `WorkspaceSidebar`
  - focused sidebar tests
- Files/modules that must be reviewed even if they remain unchanged:
  - business routes using the shared shell
  - `/playground` route shell behavior
- Minimum validation paths before the task can stop:
  - `/playground` still shows the chat-first shell
  - business routes no longer show a dominant history rail
  - route navigation remains usable and consistent
- What would count as a shallow fix for this task:
  - hiding one visual block in CSS without creating an explicit shell distinction

## Acceptance criteria

- non-chat business routes do not dedicate the sidebar middle area to chat history
- `/playground` still retains the chat-first sidebar behavior
- product navigation remains intact across both shell modes
- future business routes can opt into the calmer shell without ad hoc page hacks

## Required tests

- focused sidebar-shell regression tests
- targeted eslint on shell files
- `cd web && npm run build`

## Manual verification

- confirm `/playground` still behaves as chat workspace
- confirm business routes feel focused and no longer split attention with history
- confirm sidebar collapse/expand still works

## Parallel-work notes

- This task should start in its own dedicated worktree from `origin/main`.
- Add the lane to `ai_first/ACTIVE_ASSIGNMENTS.md` before runtime edits begin.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` likely does not need an update unless shell-mode differences become part of the documented primary product structure.

## Implementation notes

- The actual impact surface included `web/components/sidebar/UtilitySidebar.tsx` because utility routes were also forcing chat-history loading through the shared shell.
- The implementation used an explicit `shellMode` contract instead of a route-local CSS hide so the shell boundary is reusable.
- `/playground` remains the only route using the dominant chat-history mode in this lane.

## Validation results

- `cd web && node --test tests/sidebar-shell-layout.test.ts tests/sidebar-nav-groups.test.ts`
- `cd web && npx eslint 'components/sidebar/SidebarShell.tsx' 'components/sidebar/WorkspaceSidebar.tsx' 'components/sidebar/UtilitySidebar.tsx' 'tests/sidebar-shell-layout.test.ts' 'tests/sidebar-nav-groups.test.ts'`
- `cd web && npm run build`
- `git diff --check`
