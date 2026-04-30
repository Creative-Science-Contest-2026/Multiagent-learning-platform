# Sidebar Shell Rebalance

- Date: 2026-04-30
- Task ID: `UI_SIDEBAR_SHELL_REBALANCE`
- Branch: `docs/sidebar-shell-rebalance`

## Goal

Improve the shared expanded sidebar so it feels structurally consistent and more usable for chat-heavy work: the conversation list should become the main middle content area, `Trò chuyện mới` should belong to the chat section instead of floating above the whole nav, and the expanded shell should be about 20% wider.

## Current Behavior

- The expanded sidebar width is `220px`, which is too narrow for Vietnamese labels such as `Bảng điều khiển giáo viên`.
- `Trò chuyện mới` is rendered as a top-level action above all route groups, but the actual session list lives much lower inside the `Trò chuyện` item in the secondary tool section.
- The session list viewport is artificially capped (`max-h-[112px]`), so the conversation history feels like a short afterthought instead of a primary working surface.
- The visible hierarchy reads as:
  - logo
  - detached new-chat action
  - route groups
  - a small chat history pocket
  - settings
- This makes the sidebar feel cramped and internally inconsistent.

## User-Approved Product Direction

- Keep the route nav at the top.
- Make the route nav more compact so it does not consume excessive height.
- Move `Trò chuyện mới` into the `Trò chuyện` section header.
- Make the conversation list the primary middle area of the sidebar.
- Keep `Cài đặt` at the bottom.
- Prefer changing `SidebarShell` directly and only adjust `SessionList` if the rows still feel too weak after the shell rebalance.

## Codebase Survey

### Entry points

- `web/components/sidebar/WorkspaceSidebar.tsx`
  - loads sessions and passes them into the shell
  - should remain mostly unchanged for this task if the shell contract stays stable
- `web/components/sidebar/SidebarShell.tsx`
  - owns expanded/collapsed layout
  - currently places `New Chat` above route groups
  - currently nests `SessionList` inside the `/playground` route item with a short viewport

### Adjacent shared UI

- `web/components/SessionList.tsx`
  - may need row-density or empty-state adjustments if the wider shell exposes weak list presentation
- `web/components/sidebar/nav-groups.ts`
  - may need only minor copy/group verification, not a structural rewrite

### Existing tests

- `web/tests/sidebar-nav-groups.test.ts`
  - currently validates route group behavior and should be extended only if nav grouping changes materially

## Candidate Approaches

### Approach A: Widen only

- Increase sidebar width and raise the conversation-list viewport height.
- Pros:
  - very small diff
  - low risk
- Cons:
  - does not solve the hierarchy problem
  - keeps `Trò chuyện mới` detached from the place where conversations actually live
  - still feels like a patched version of the old layout

### Approach B: Rebalance the expanded shell hierarchy

- Keep the same route shell, but change the structure to:
  - header
  - compact route nav
  - dedicated `Trò chuyện` section with section header and inline `+`
  - large scrollable session list
  - bottom settings footer
- Pros:
  - matches the user’s reference and approved direction
  - fixes both spacing and ownership of actions
  - keeps the diff bounded to the shared shell
- Cons:
  - requires a more opinionated layout change than simple width tuning

### Approach C: Chat-first sidebar

- Promote sessions above most route nav and make the sidebar primarily a conversation browser.
- Pros:
  - very strong chat-first UX
- Cons:
  - shifts the whole information architecture too far for a product that still depends on top-level routes like Knowledge, Dashboard, Tutor, and Marketplace

## Chosen Approach

Approach B.

It is the smallest change that actually fixes the current mismatch between action placement and content ownership, while preserving the product’s route-first navigation model.

## Proposed Layout

### 1. Header

- Keep the `DeepTutor` logo/title on the left.
- Keep the collapse toggle on the right.
- Slightly relax horizontal spacing so the top row breathes better in the wider shell.

### 2. Primary route nav

- Keep the route groups at the top of the expanded sidebar.
- Make items slightly denser so they consume less vertical space.
- Increase shell width from `220px` to about `264px`.
- Use that extra width to reduce awkward line wrapping, especially for Vietnamese labels.
- Preserve active-state clarity, but avoid heavy “button slab” styling.

### 3. Dedicated `Trò chuyện` section

- Introduce a section header row:
  - left: `Trò chuyện`
  - right: icon-only `+` action for creating a new chat
- Remove the old detached `New Chat` row above the route nav.
- Remove the tiny capped session viewport attached to the route item.
- Replace it with a dedicated chat-history area that uses the remaining vertical space (`flex-1`) and scrolls independently.
- Empty state should live inside this section, not as dead space across the entire sidebar.

### 4. Footer

- Keep `Cài đặt` anchored at the bottom behind a light top border.
- Do not let the footer compete with the session area.

## Interaction Model

- Clicking the `+` in the `Trò chuyện` section creates a new chat and routes to `/playground`, preserving the current action semantics.
- Clicking a session still selects and loads that session through the existing `SidebarShell` callback contract.
- Collapsed mode stays conceptually the same:
  - top-level icon rail
  - new-chat icon
  - route icons
  - footer icons
- The main change is in expanded mode only.

## Expected UI Outcome

- The sidebar feels wider and less cramped.
- `Bảng điều khiển giáo viên` is less likely to wrap awkwardly.
- The relationship between `Trò chuyện mới` and the chat list becomes obvious.
- The conversation history becomes the dominant middle surface instead of a short embedded box.
- The shell feels closer to modern chat sidebars, while still respecting this repo’s multi-route product structure.

## Files expected to change during implementation

- `web/components/sidebar/SidebarShell.tsx`
- `web/components/SessionList.tsx` only if shell changes reveal weak row spacing or empty-state presentation
- `web/tests/sidebar-nav-groups.test.ts` only if grouping or related shell expectations need explicit regression coverage

## Files reviewed but expected to remain unchanged

- `web/components/sidebar/WorkspaceSidebar.tsx`
  - it should continue providing sessions and callbacks without needing a new contract
- `web/components/sidebar/nav-groups.ts`
  - unless final implementation needs a minor label/group cleanup

## Validation expectations

- expanded sidebar is visibly about 20% wider
- nav items remain readable and better aligned
- `Trò chuyện mới` is no longer detached above the entire nav
- conversation list occupies the main middle area with real scroll room
- `Cài đặt` stays pinned at the bottom
- collapsed sidebar still works without layout regressions
