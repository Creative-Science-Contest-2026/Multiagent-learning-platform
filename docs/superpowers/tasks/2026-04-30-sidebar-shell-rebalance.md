# Task Packet: Sidebar Shell Rebalance

- Task ID: `UI_SIDEBAR_SHELL_REBALANCE`
- Date: 2026-04-30
- Branch: `docs/sidebar-shell-rebalance`
- Status: Writing spec

## Objective

Rebalance the shared expanded sidebar so the conversation list becomes the primary middle content area, the new-chat action sits inside the chat section, and the sidebar is about 20% wider.

## User-Approved Scope

- increase expanded sidebar width by roughly 20%
- keep the main route nav at the top, but make it more compact
- move `Trò chuyện mới` into the `Trò chuyện` section header
- let the session list use most of the remaining sidebar height
- keep `Cài đặt` anchored at the bottom
- prefer editing `SidebarShell` directly and touch `SessionList` only if row density still needs refinement

## Owned Files

- `web/components/sidebar/SidebarShell.tsx`
- `web/components/SessionList.tsx`
- `web/components/sidebar/nav-groups.ts`
- `web/tests/sidebar-nav-groups.test.ts`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-sidebar-shell-rebalance.md`
- `docs/superpowers/specs/2026-04-30-sidebar-shell-rebalance-design.md`

## Do-Not-Touch

- the live `/playground` tutor-pack lane files outside shared sidebar scope
- unrelated marketplace, knowledge-pack, and dashboard runtime lanes
- global machine configuration

## Design before implementation

- Runtime behavior change: yes
- Current behavior:
  - `New Chat` is detached above the route nav
  - the session list sits inside the `Trò chuyện` route item with a very short viewport
  - the expanded sidebar is too narrow and causes awkward wrapping
- Intended behavior change:
  - shared expanded sidebar has clearer hierarchy and a larger, chat-owned session area
- Candidate approach A:
  - widen the sidebar and only raise the session viewport cap
- Candidate approach B:
  - rebalance the shell hierarchy inside `SidebarShell` so chat actions and chat history belong to the same section
- Chosen approach and reason:
  - approach B; it fixes both spacing and hierarchy instead of only making the old layout larger

## Validation paths

- expanded sidebar width feels materially wider
- nav labels avoid awkward wrapping
- `Trò chuyện mới` is owned by the chat section
- session list uses the remaining middle height and scrolls independently
- collapsed mode still behaves sensibly
