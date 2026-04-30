# Feature Task: Playground Chat Visual Refinement

Task ID: `UI_PLAYGROUND_CHAT_VISUAL_REFINEMENT`
Commit tag: `UI-CHAT-VISUAL-REFINEMENT`
Owner: Frontend visual refinement lane
Branch: `fix/playground-chat-visual-refinement`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Refine the `/playground` chat presentation so the conversation feels lighter, more minimal, and more product-like while still keeping traces, metadata, and tool-call visibility available inside the main flow.

## User-visible outcome

- User and assistant bubbles use softer, lighter tones instead of harsh dark contrast.
- `Thinking`, `Acting`, `Observing`, `Responding`, `Process`, and `Metadata` remain visible but default to a more compact, collapsed, and subtle presentation.
- Technical trace surfaces no longer read like raw debug components; they feel integrated into the same visual language as the chat.
- The command-bar composer looks calmer and more refined.

## Owned files/modules

- `web/app/(workspace)/playground/page.tsx`
- `web/components/common/AssistantResponse.tsx`
- `web/components/common/ProcessLogs.tsx`
- `web/components/chat/home/PlaygroundRightPanel.tsx`
- `web/locales/en/app.json`
- `web/locales/vi/app.json`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-playground-chat-visual-refinement.md`
- `docs/superpowers/specs/2026-04-30-playground-chat-visual-refinement-design.md`
- `docs/superpowers/pr-notes/2026-04-30-playground-chat-visual-refinement.md`

## Do-not-touch files/modules

- `deeptutor/**`
- `web/app/(workspace)/guide/**`
- `web/app/(workspace)/co-writer/**`
- `web/app/(workspace)/agents/**`
- `web/app/(workspace)/dashboard/**`
- `web/app/(utility)/**`
- `.github/workflows/**`
- `requirements/**`
- `package-lock.json`
- `web/package-lock.json`
- `.env*`

## Design before implementation

### Current behavior

- The `/playground` chat shell is functional but visually harsh.
- User bubbles rely on a dark fill that feels too heavy relative to the rest of the workspace.
- Trace sections, process logs, and metadata still read like raw technical cards or debug output rather than subtle supporting UI.
- Several sub-panels remain too boxy and component-like, with stronger borders and contrast than the main conversation needs.

### Intended behavior change

- Keep all current trace and metadata visibility, but move them into a gentler default state.
- Default trace and metadata sections to collapsed.
- Use softer background values, lighter contrast, and calmer spacing for user bubbles, assistant content, process logs, and tool-result surfaces.
- Make the whole chat area feel simplified and refined rather than “debug-first”.

### Candidate approaches

1. Only lighten colors and keep structure unchanged.
   - low risk, but the trace surfaces still feel too raw
2. Keep the existing data model and flow, but restyle bubbles, accordions, logs, and result cards into a subtler presentation
   - chosen approach because it improves tone without reopening runtime logic
3. Move all traces into a separate side panel
   - cleaner, but conflicts with the explicit requirement to keep them visible in the chat flow

### Chosen approach

Use approach 2. Preserve the same runtime surfaces and information hierarchy, but re-style them into a lighter visual system with softer tones, less contrast, and collapsed-by-default debug-like sections.

### Codebase survey

- Entry point/handler:
  - `web/app/(workspace)/playground/page.tsx`
- Primary presentation modules:
  - `web/components/common/AssistantResponse.tsx`
  - `web/components/common/ProcessLogs.tsx`
  - `web/components/chat/home/PlaygroundRightPanel.tsx`
- Closest reused surfaces:
  - trace accordion rendering in `TracePanel`
  - capability/tool result cards in `CapabilityResultPanel`
- Shared copy/tests:
  - `web/locales/en/app.json`
  - `web/locales/vi/app.json`

### Expected impact surface

- Likely to change:
  - user and assistant bubble styling
  - trace accordion defaults and visual chrome
  - process-log card styling and default openness
  - metadata/result surface styling
  - command-bar presentation
- Reviewed but expected to remain unchanged:
  - backend stream events and payload structure
  - capability execution logic
  - playground route selection/state logic
  - non-playground routes
- Validation paths:
  - targeted lint on touched files
  - production frontend build
  - manual browser inspection of calmer tones, collapsed trace defaults, and refined command bar

## Acceptance criteria

- Chat bubbles are visually lighter and more refined.
- Technical trace sections remain available but default to collapsed and visually subdued.
- Metadata and process surfaces no longer dominate the conversation.
- The overall `/playground` conversation area feels calmer, lighter, and more consistent.

## Required tests

- `cd web && npx eslint "app/(workspace)/playground/page.tsx" "components/common/AssistantResponse.tsx" "components/common/ProcessLogs.tsx" "components/chat/home/PlaygroundRightPanel.tsx"`
- `cd web && npm run build`

## Manual verification

- Confirm user bubble is no longer solid black.
- Confirm `Thinking`, `Acting`, `Observing`, `Responding`, `Process`, and `Metadata` are present but default closed where appropriate.
- Confirm the trace and metadata surfaces read as supporting UI rather than raw debug panels.

## Handoff notes

- Keep trace visibility; do not remove these sections in this lane.
- Stay inside `/playground` presentation only.
