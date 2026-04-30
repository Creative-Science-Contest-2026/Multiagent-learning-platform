# Feature Task: Playground Chat Workspace Polish

Task ID: `UI_PLAYGROUND_CHAT_WORKSPACE_POLISH`
Commit tag: `UI-CHAT-WORKSPACE-POLISH`
Owner: Frontend workspace polish lane
Branch: `fix/playground-chat-workspace-polish`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Polish the merged `/playground` workspace so the visible UI is more clearly Vietnamese-first, the right inspector panel is easier to understand and choose from, the chat header becomes much smaller, and the conversation input stays compact at the bottom.

## User-visible outcome

- Obvious English strings still visible on `/playground` are replaced or mapped to Vietnamese.
- The right inspector panel is grouped into clearer functional blocks instead of a long, visually flat list.
- The chat header uses a much smaller vertical footprint.
- The composer/input area is shorter and anchored neatly to the bottom.

## Owned files/modules

- `web/app/(workspace)/playground/page.tsx`
- `web/components/chat/home/PlaygroundRightPanel.tsx`
- `web/components/chat/home/PlaygroundWorkspaceShell.tsx`
- `web/components/sidebar/SidebarShell.tsx`
- `web/locales/vi/app.json`
- `web/locales/en/app.json`
- `web/tests/contest-vietnamese-coverage.test.ts`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-playground-chat-workspace-polish.md`
- `docs/superpowers/pr-notes/2026-04-30-playground-chat-workspace-polish.md`

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

The merged `/playground` route already uses a chat-first shell, but the visible surface still has three polish gaps:

- some English descriptions and labels still render directly from capability metadata or shared labels
- the right panel mixes mode selection and context in one long stack, so the active choice is not obvious
- the center header and input block both consume too much vertical space for a chat-first canvas
- the conversation area still does not separate user turns versus assistant turns strongly enough, so the chat feels flatter than an OpenAI-style workspace

### Intended behavior change

Keep the overall three-column shell, but tighten and clarify it:

- translate or map the remaining visible English copy on this route
- turn the right panel into clearly separated groups such as current mode, switch mode, tools, and knowledge source
- reduce the center header height to roughly 40% of the current vertical footprint
- make the input/composer shorter and pin it cleanly to the bottom
- increase message hierarchy so user and assistant turns are easier to distinguish at a glance
- make selected and active states in the right panel more explicit through icon/state treatment without reopening route structure
- let the right panel move between a few readable width presets so the workspace feels closer to an editor shell instead of a fixed demo layout
- make the bottom composer read more like a command bar than a floating textbox

### Candidate approaches

1. Patch strings only and leave the structure intact
   - low risk, but does not solve the discoverability problem
2. Keep the merged shell but reorganize the right panel into grouped cards while shrinking the center header and composer
   - chosen approach because it directly addresses clarity without reopening the full layout
3. Move capability selection out of the right panel entirely and rebuild the workspace navigation again
   - too broad for a polish lane

### Chosen approach

Use approach 2. Preserve the merged route structure and state seams, but retune presentation around clearer grouping and less chrome. Add frontend-side translation mapping for visible capability descriptions where the backend still returns English text.

### Codebase survey

- Entry point/handler:
  - `web/app/(workspace)/playground/page.tsx`
- Primary presentational modules:
  - `web/components/chat/home/PlaygroundRightPanel.tsx`
  - `web/components/chat/home/PlaygroundWorkspaceShell.tsx`
- Shared shell surface:
  - `web/components/sidebar/SidebarShell.tsx`
- Shared copy/tests:
  - `web/locales/vi/app.json`
  - `web/locales/en/app.json`
  - `web/tests/contest-vietnamese-coverage.test.ts`

### Expected impact surface

- Likely to change:
  - `/playground` header sizing and right-panel grouping
  - route-local translation mapping for capability descriptions
- right-panel card hierarchy, selected-state treatment, and bottom composer sizing
- right-panel width-preset controls and command-bar composer chrome
  - conversation bubble hierarchy for user versus assistant turns
  - locale keys and one focused Vietnamese-coverage test
- Reviewed but expected to remain unchanged:
  - backend capability metadata
  - dashboard, guide, agents, and utility routes beyond shared locale/sidebar strings already reused here
  - sidebar route grouping logic outside label display
- Validation paths:
  - focused locale test
  - targeted lint on touched files
  - production frontend build
  - manual browser inspection of panel grouping, smaller header, and smaller composer

## Acceptance criteria

- The `/playground` surface no longer shows obvious English strings in the touched UI path.
- The right panel has distinct groups that make current mode versus available choices easier to understand.
- The center header is visibly much shorter than before.
- The composer stays smaller and cleaner at the bottom.
- User and assistant turns are visually easier to distinguish without harming readability.
- The right panel can switch between at least a few width presets without leaving the route.

## Required tests

- `cd web && npx --yes tsx --test tests/contest-vietnamese-coverage.test.ts`
- `cd web && npx eslint "app/(workspace)/playground/page.tsx" "components/chat/home/PlaygroundRightPanel.tsx" "components/chat/home/PlaygroundWorkspaceShell.tsx" "components/sidebar/SidebarShell.tsx"`
- `cd web && npm run build`

## Manual verification

- Open `/playground` and check for visible English leaks.
- Confirm the right panel makes mode selection and current state easier to scan.
- Confirm the center header is much smaller.
- Confirm the input area is shorter and pinned neatly to the bottom.

## Handoff notes

- Keep this lane visual and copy-focused only.
- Do not reopen the previous shell-routing change or capability execution flow.
