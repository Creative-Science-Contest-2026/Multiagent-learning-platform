# Task Packet: Playground Hide Mode Switcher

- Task ID: `UI-PLAYGROUND-HIDE-MODE-SWITCHER`
- Date: 2026-04-30
- Branch: `fix/playground-hide-mode-switcher`
- Status: Spec written

## Objective

Hide the right-panel chooser for `Năng lực / Công cụ` on `/playground` without deleting the underlying capability or tool logic.

## User-Approved Scope

- hide the visible mode/tool chooser in the right panel
- keep the underlying logic for later upgrades
- do not remove capabilities or tools from backend/runtime in this lane

## Owned Files

- `web/app/(workspace)/playground/page.tsx`
- `web/components/chat/home/PlaygroundRightPanel.tsx`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-playground-hide-mode-switcher.md`
- `docs/superpowers/specs/2026-04-30-playground-hide-mode-switcher-design.md`
- `docs/superpowers/pr-notes/2026-04-30-playground-hide-mode-switcher.md`

## Do-Not-Touch

- backend capability implementations
- session history bugfix lane
- unrelated untracked files

## Design Before Implementation

- `docs/superpowers/specs/2026-04-30-playground-hide-mode-switcher-design.md`

## Validation Plan

- `cd web && npx eslint "app/(workspace)/playground/page.tsx" "components/chat/home/PlaygroundRightPanel.tsx"`
- `cd web && npm run build`
- `cd /Users/nguyenhuuloc/Documents/Multiagent-learning-platform && git diff --check`
