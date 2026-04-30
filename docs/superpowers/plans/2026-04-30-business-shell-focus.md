# Implementation Plan: Business Shell Focus

## Objective

Introduce an explicit business-shell mode that removes dominant chat history from non-chat routes while preserving the current chat-first shell on `/playground`.

## Steps

1. Update the active lane contract
   - record the runtime lane in `ai_first/ACTIVE_ASSIGNMENTS.md`
   - confirm the actual impact surface includes `UtilitySidebar` in addition to `SidebarShell` and `WorkspaceSidebar`

2. Refactor the sidebar shell contract
   - replace the old `showSessions` toggle with an explicit `shellMode`
   - keep `chat` mode rendering the existing chat-history block
   - keep `business` mode rendering route nav without the dominant history section

3. Wire route-specific sidebars
   - keep `WorkspaceSidebar` in `chat` mode only for `/playground`
   - switch other workspace routes to `business`
   - simplify `UtilitySidebar` to business mode without session fetching

4. Lock behavior with focused regression tests
   - extend source-level shell tests for explicit mode support
   - verify utility/workspace sidebars wire the expected modes

5. Validate and document
   - run focused node tests
   - run eslint on touched sidebar files
   - run `web` build
   - update daily log and PR note
