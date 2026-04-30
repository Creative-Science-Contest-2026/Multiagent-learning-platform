# Business Shell Focus Design

- Date: 2026-04-30
- Task ID: `UI_BUSINESS_SHELL_FOCUS`
- Branch: `docs/business-ui-specs`

## Goal

Reframe the shared business-facing shell so pages like `Gói kiến thức` and `Bảng điều khiển giáo viên` feel like focused web-app work surfaces instead of mixed chat-plus-dashboard canvases.

## Current Behavior

- Business pages still inherit a shell where chat history competes with the main task area.
- The left-side shell is trying to serve two jobs at once:
  - product navigation
  - conversation browsing
- On dashboard-style routes, this makes the page feel noisier than necessary and weakens the visual priority of the main content.
- The product currently lacks a clean distinction between:
  - chat-first routes such as `/playground`
  - business/task routes such as `/knowledge`, `/dashboard`, and `/agents`

## Intended Behavior

- Chat history should remain dominant only on chat-first workspaces.
- Business/task routes should keep the product nav, but should not let conversation history compete with the primary page surface.
- Shared visual primitives across business routes should become more consistent:
  - card shells
  - section spacing
  - heading rhythm
  - badges/status pills
  - filter bars

## User-Approved Direction

- Keep the app-shell model with a product sidebar.
- Do not let chat history occupy high-value visual space on business pages.
- Use a calmer dashboard/web-app visual language:
  - neutral background
  - compact headings
  - clear card containers
  - one primary action per major block

## Candidate Approaches

### Approach A: Hide chat history per page with route-local overrides

- Add page-specific wrappers or props that selectively suppress history on `knowledge` and `dashboard`.
- Pros:
  - smallest code diff
  - low risk for chat routes
- Cons:
  - spreads shell rules across multiple pages
  - makes future business routes repeat the same override logic

### Approach B: Introduce an explicit shell distinction between chat routes and business routes

- Keep one shared navigation system, but add a first-class shell mode:
  - `chat workspace`
  - `business workspace`
- Pros:
  - correct architecture boundary
  - makes future pages easier to classify
  - keeps history available where it matters and out of the way elsewhere
- Cons:
  - requires a deliberate shell contract change

### Approach C: Remove history from the sidebar entirely

- Keep only route navigation in the sidebar, and move chat history somewhere else product-wide.
- Pros:
  - simplest mental model
- Cons:
  - weakens the chat experience on `/playground`
  - too broad for the current problem

## Chosen Approach

Approach B.

The product already has both chat-first and business-first routes. The clean fix is to formalize that distinction in the shell instead of patching each page individually.

## Proposed Design

### 1. Shell Modes

- Add a shared shell distinction:
  - `chat workspace`
  - `business workspace`
- `chat workspace` keeps:
  - route nav
  - large chat-history area
  - new-chat action
- `business workspace` keeps:
  - route nav
  - compact supporting actions only
  - no dominant chat-history block

### 2. Business Shell Layout

- The left sidebar remains visible for product navigation.
- The main content column becomes visually dominant.
- History should not appear as a large middle rail inside the sidebar on business pages.
- If conversation access is still needed, expose it as:
  - a small icon/button
  - or a secondary drawer/panel
  - but not as the primary shell middle area

### 3. Shared Visual Primitives

- Define a business-page visual baseline:
  - page header with short helper text
  - section cards with moderate radius and neutral borders
  - compact section headings
  - status pills for state
  - compact filter toolbar patterns
- Treat this as the design substrate for both `Gói kiến thức` and `Bảng điều khiển giáo viên`.

### 4. Route Ownership

- `playground` remains the chat-first route.
- `knowledge`, `dashboard`, and teacher-facing setup routes should opt into the business shell mode.
- This spec does not redesign those pages by itself; it only defines the shell and shared visual constraints they should inherit.

## Files Expected To Change During Implementation

- `web/components/sidebar/SidebarShell.tsx`
- `web/components/sidebar/WorkspaceSidebar.tsx`
- any route-level shell selection point that decides how the sidebar/history layout is composed
- shared shell tests if they already cover history visibility and layout mode behavior

## Files Reviewed But Expected To Remain Mostly Unchanged

- page-level `knowledge` logic
- page-level `dashboard` logic
- backend contracts
- session/chat runtime flows

## Validation Expectations

- business routes no longer display chat history as the dominant sidebar middle area
- `/playground` keeps the current chat-first shell behavior
- route navigation remains consistent across modes
- the shell clearly supports downstream dashboard-style pages without introducing route-specific hacks

## Notes For Follow-On Specs

- `2026-04-30-knowledge-pack-dashboard-shell-design.md` should assume this business shell exists.
- `2026-04-30-teacher-dashboard-decision-flow-design.md` should also assume this business shell exists.
