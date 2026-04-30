# Feature Task: Playground Chat Workspace Refresh

Task ID: `UI_PLAYGROUND_CHAT_WORKSPACE`
Commit tag: `UI-CHAT-WORKSPACE`
Owner: Frontend workspace lane
Branch: `fix/playground-chat-workspace`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Replace the current card-based `Playground` experience with a full-screen, three-column, chat-first workspace that feels closer to OpenAI and VS Code. The route remains `/playground`, but its information architecture becomes a primary conversational workspace instead of a technical capability demo page.

## User-visible outcome

- `Playground` opens as a full-height conversational workspace instead of a centered demo card.
- The layout uses three columns:
  - left rail for navigation plus conversation history;
  - center canvas for large chat messages and the main composer;
  - right panel for tools, context, trace, and capability controls.
- Users can collapse or expand side panels, rely on icon-first actions with Vietnamese tooltips, and keep the message area visually dominant.
- User-facing copy on the route and its directly reused chat controls is Vietnamese-first.

## Owned files/modules

- `web/app/(workspace)/playground/page.tsx`
- `web/components/chat/home/ChatComposer.tsx`
- `web/components/chat/home/ChatMessages.tsx`
- `web/components/chat/home/TracePanels.tsx`
- `web/components/SessionList.tsx`
- `web/components/sidebar/WorkspaceSidebar.tsx`
- `web/components/sidebar/SidebarShell.tsx`
- `web/components/sidebar/nav-groups.ts`
- `web/locales/vi/app.json`
- `web/locales/en/app.json`
- `web/tests/contest-vietnamese-coverage.test.ts`
- `web/tests/sidebar-nav-groups.test.ts`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-playground-chat-workspace.md`
- `docs/superpowers/specs/2026-04-30-playground-chat-workspace-design.md`
- `docs/superpowers/pr-notes/2026-04-30-playground-chat-workspace.md`

## Do-not-touch files/modules

- `deeptutor/`
- `web/app/(workspace)/dashboard/**`
- `web/app/(workspace)/guide/**`
- `web/app/(workspace)/agents/**`
- `web/app/(utility)/**`
- `.github/workflows/**`
- `requirements/**`
- `package-lock.json`
- `web/package-lock.json`
- `.env*`
- committed `data/` files

## Design before implementation

### Current behavior

`web/app/(workspace)/playground/page.tsx` renders a centered playground surface with capability cards on the left and a configuration/testing card on the right. The route behaves like a capability lab, not like a primary conversation workspace. Several labels and helper strings still surface English copy or mixed-language wording.

### Intended behavior change

The route becomes a full-screen chat workspace with a persistent shell:

- left column for navigation and session history
- center column for large conversation messages and a roomy composer
- right column for contextual controls, enabled tools, knowledge-base selection, and trace or process insight

The experience must support icon-first controls, hover tooltips, and panel collapse/expand interactions while keeping the chat canvas dominant. User-facing copy on the route and reused components in scope should be Vietnamese-first.

### Candidate approaches

1. Keep the current playground card layout and restyle it in place.
   - Fastest, but likely leaves the route feeling like a retrofitted demo.
2. Keep the route and existing data flow, but rebuild the screen into a chat-first shell using reused chat/session components.
   - Chosen approach because it preserves current backend and state seams while allowing a decisive UI reset.
3. Build a mostly new route-local UI and duplicate chat behavior just for playground.
   - Higher visual freedom, but unnecessary logic duplication and regression risk.

### Chosen approach

Use approach 2. Preserve the route, capability/tool state, and streaming flow, but restructure the page around a shell with explicit left, center, and right columns. Reuse existing chat components where possible, adjust them for larger message density and panel-driven controls, and localize route-visible strings in the same pass.

### Codebase survey

- Entry point/handler:
  - `web/app/(workspace)/playground/page.tsx`
- Primary UI modules:
  - `web/components/chat/home/ChatComposer.tsx`
  - `web/components/chat/home/ChatMessages.tsx`
  - `web/components/chat/home/TracePanels.tsx`
  - `web/components/SessionList.tsx`
- Shared shell/navigation modules:
  - `web/components/sidebar/WorkspaceSidebar.tsx`
  - `web/components/sidebar/SidebarShell.tsx`
  - `web/components/sidebar/nav-groups.ts`
- Shared contracts/types/state:
  - `web/lib/playground-config.ts`
  - `web/lib/session-api.ts`
  - `web/lib/unified-ws.ts`
  - `web/locales/vi/app.json`
  - `web/locales/en/app.json`
- Closest tests:
  - `web/tests/contest-vietnamese-coverage.test.ts`
  - `web/tests/sidebar-nav-groups.test.ts`

### Expected impact surface

- Likely to change:
  - playground route structure and local UI state
  - chat composer and message presentation classes/copy
  - session list presentation for the left rail
  - sidebar labels/tooltips if needed for icon-first behavior
  - localization strings and focused tests
- Reviewed but expected to remain unchanged:
  - backend runtime under `deeptutor/`
  - dashboard, guide, and agents routes
  - utility routes outside the workspace shell
- Validation paths:
  - focused frontend tests for Vietnamese coverage and navigation labels
  - type-safe frontend build or lint/test command scoped to affected files if available
  - manual inspection of full-height layout, collapse/expand controls, and localized text

## Acceptance criteria

- The `/playground` route is visually a full-height three-column workspace.
- The center chat area is clearly the primary visual surface.
- Left and right panels can collapse or visually compress without breaking the main chat flow.
- Actions that can be icon-only expose readable Vietnamese tooltip or `aria-label` text.
- Directly visible route copy is Vietnamese-first, with no obvious leftover English product labels in the touched surface.
- Existing chat send/stream/session behavior on this route still works.

## Required tests

- `cd web && npm test -- --runInBand tests/contest-vietnamese-coverage.test.ts tests/sidebar-nav-groups.test.ts`
- Additional focused frontend validation command if the implementation introduces new route-specific tests

## Manual verification

- Open `/playground` and confirm three-column shell at desktop width.
- Collapse and expand side panels.
- Start a new chat and confirm messages render large and readable.
- Hover icon-only actions and confirm Vietnamese tooltip or accessible label.
- Verify visible text on the route is Vietnamese.

## Handoff notes

- Keep styling changes bounded to the workspace chat experience and directly reused components.
- If new shared primitives are needed, keep them narrow and document why they are shared.
- Update `ai_first/architecture/MAIN_SYSTEM_MAP.md` only if the shell or primary user flow meaningfully changes beyond visual layout.
