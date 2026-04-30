# Playground Hide Mode Switcher Design

- Date: 2026-04-30
- Task ID: `UI-PLAYGROUND-HIDE-MODE-SWITCHER`
- Branch: `fix/playground-hide-mode-switcher`

## Goal

Hide the right-panel mode and tool chooser on `/playground` for the current product version while preserving the underlying capability and tool logic for future reactivation.

## Current Behavior

- The right panel on `/playground` shows a large `Chuyển chế độ` block.
- That block includes:
  - the `Năng lực / Công cụ` toggle
  - the capability list (`Trò chuyện`, `Giải sâu`, `Tạo bài kiểm tra`, `Nghiên cứu sâu`, etc.)
  - the tool list (`Động não`, `RAG`, `Tìm kiếm web`, etc.)
- Even though the page already has a main chat workspace, this chooser keeps exposing internal product structure that the user wants hidden for the current release.

## Intended Behavior Change

- The right panel must no longer show the mode-switching chooser or the tool-switching chooser.
- No capability or tool implementation is removed.
- The active capability and tool state can continue to exist in code and storage.
- This is a presentation-only hide for the current version.

## Codebase Survey

### Entry points and handlers

- `web/app/(workspace)/playground/page.tsx`
  - constructs the `selectionPanel`
  - passes that panel into the right-side layout

### Primary service or use-case modules

- `web/components/chat/home/PlaygroundRightPanel.tsx`
  - generic right-panel shell for `/playground`

### Shared contracts, schemas, or types

- no backend or schema contract involved

### Adjacent or reused flows inspected

- current `/playground` shell already separates center conversation workspace from right-side contextual UI, so removing the chooser is bounded to the right panel content only

### Closest existing tests

- no focused test exists for right-panel chooser visibility
- validation will rely on ESLint, app build, and diff checks

## Candidate Approaches

### Approach A: Hide the chooser with CSS only

- Keep rendering the block but visually hide it.
- Pros:
  - smallest diff
- Cons:
  - leaves dead UI markup in the DOM
  - easier for the block to reappear accidentally

### Approach B: Stop rendering the chooser block in the right panel

- Remove the visible `selectionPanel` from the `/playground` right panel while keeping all state logic intact.
- Pros:
  - cleanest presentation result
  - no user-facing trace of internal mode switching
  - preserves logic for future reactivation
- Cons:
  - requires checking the right panel still reads well after the block is removed

### Approach C: Remove capability and tool switching logic entirely

- Delete the visible chooser and underlying state wiring.
- Pros:
  - strongest lock-down
- Cons:
  - broader than requested
  - conflicts with the requirement to keep the feature for later

## Chosen Approach

Approach B.

The user wants the chooser hidden from FE now, not deleted from the product. Removing the visible block while keeping state and runtime logic intact is the smallest correct change.

## Planned Changes

- In `web/app/(workspace)/playground/page.tsx`:
  - stop rendering the `selectionPanel` into the right panel
  - keep capability/tool state logic untouched unless dead imports or dead variables need cleanup
- In `web/components/chat/home/PlaygroundRightPanel.tsx`:
  - keep the shell unchanged unless spacing needs a small cleanup after the chooser is removed

## Expected Impact Surface

### Likely to change

- `web/app/(workspace)/playground/page.tsx`

### Reviewed but expected to remain unchanged unless implementation reveals a small layout cleanup need

- `web/components/chat/home/PlaygroundRightPanel.tsx`

## Tests To Run

- `cd web && npx eslint "app/(workspace)/playground/page.tsx" "components/chat/home/PlaygroundRightPanel.tsx"`
- `cd web && npm run build`
- `cd /Users/nguyenhuuloc/Documents/Multiagent-learning-platform && git diff --check`

## Non-Goals

- No capability hiding in the runtime layer
- No backend changes
- No route changes
