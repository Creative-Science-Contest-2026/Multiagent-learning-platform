# Playground Chat Consumer Trace Design

- Date: 2026-04-30
- Task ID: `UI-PLAYGROUND-CONSUMER-TRACE`
- Branch: `fix/playground-chat-consumer-trace`

## Goal

Realign `/playground` chat turns with the lighter, more consumer-facing chat presentation already proven in the original chat surfaces, while preserving visible trace stages for end users in a compact and product-like form.

## Current Behavior

- `/playground` renders assistant turns with a custom local `TracePanel` that wraps `Thinking`, `Acting`, `Observing`, and `Responding` inside large bordered accordions.
- User messages use a softened palette already, but the bubble width and padding still make a short prompt look oversized.
- Assistant turns can stack multiple heavy blocks in one pass:
  - a full trace card
  - the assistant content card
  - process-log card
  - metadata card
- The combination makes a single round occupy too much vertical space and feel closer to a debug console than a consumer AI chat product.
- The original chat surfaces in `web/components/chat/home/ChatMessages.tsx` and `web/components/chat/home/TracePanels.tsx` already implement the preferred interaction language: compact trace rows, restrained chrome, and response-first hierarchy.

## Intended Behavior Change

- `/playground` should borrow the visual language of the original chat UI for each conversation turn.
- `Thinking`, `Acting`, `Observing`, and `Responding` must remain visible, but they should look like subtle trace rows instead of standalone debug cards.
- User messages should render as compact light-gray bubbles with narrower maximum width and smaller vertical padding.
- `Metadata` must not be shown in the end-user chat flow.
- Duplicate or low-value technical surfaces inside one assistant turn should be collapsed or removed so that a normal exchange reads as one user bubble, one compact trace region, and one assistant answer.

## Codebase Survey

### Entry points and handlers

- `web/app/(workspace)/playground/page.tsx`
  - owns the `/playground` chat shell
  - currently defines the local `TracePanel`
  - currently renders user/assistant turns, process logs, and result surfaces inline

### Primary service or use-case modules

- `web/components/common/AssistantResponse.tsx`
  - shared assistant markdown renderer and text presentation
- `web/components/common/ProcessLogs.tsx`
  - shared process log surface currently available to `/playground`

### Shared contracts, schemas, or types

- `StreamEvent` usage in `/playground` and `TracePanels.tsx`
  - determines which stage and tool-call events are available for trace summarization

### Adjacent or reused flows inspected

- `web/components/chat/home/ChatMessages.tsx`
  - reference consumer-chat composition already used elsewhere
- `web/components/chat/home/TracePanels.tsx`
  - reference trace treatment with lightweight rows and restrained expandable details

### Closest existing tests

- No dedicated unit test currently targets `/playground` trace rendering.
- Existing validation for this surface currently relies on TypeScript, ESLint, app build, and locale coverage where touched.

## Candidate Approaches

### Approach A: Keep local `/playground` structure and restyle it heavily

- Rework the existing `TracePanel`, message wrappers, and metadata blocks in place.
- Pros:
  - smallest structural diff
  - lower risk of runtime wiring regressions
- Cons:
  - easier to keep accidental baggage from the current boxed-debug layout
  - more likely to preserve duplicate surfaces

### Approach B: Reuse the original chat composition patterns as the styling source of truth

- Refactor `/playground` turn rendering to follow the structure and visual language already established in `ChatMessages.tsx` and `TracePanels.tsx`.
- Pros:
  - best match for the user’s stated preference
  - reuses a proven presentation language instead of inventing another variant
  - naturally pushes trace UI toward compact rows instead of cards
- Cons:
  - requires careful adaptation so the original chat components fit the 3-column `/playground` shell without pulling in unrelated logic

### Approach C: Hide nearly all trace UI and show only the final response

- Keep only a single status line or answer card for each assistant turn.
- Pros:
  - simplest and smallest visual footprint
- Cons:
  - conflicts with the approved requirement that stage traces remain visible

## Chosen Approach

Approach B.

The requirement is not simply “make it smaller”; it is “make it feel like the original chat UI again.” The safest way to hit that target is to use the original consumer-chat and trace components as the design reference and move `/playground` toward that composition, while still keeping the shell, right panel, and workspace routing introduced in previous work.

## Planned Changes

### `/playground` turn layout

- Remove the current heavy trace-card treatment from `web/app/(workspace)/playground/page.tsx`.
- Replace it with a compact trace presentation patterned after `CallTracePanel`:
  - small rows
  - low-contrast chrome
  - minimal borders
  - no large outer card around the entire trace stack

### User message treatment

- Reduce user bubble max width so short prompts no longer stretch into oversized capsules.
- Keep only a light gray background with subtle border separation.
- Reduce padding and whitespace to align with consumer AI chat norms.

### Assistant turn treatment

- Keep the answer as the primary visual payload.
- Reduce or remove unnecessary wrapper cards around the assistant text where they add no value.
- Preserve lightweight success/status hints only if they do not dominate the turn.

### Debug-oriented surfaces

- Hide metadata from the end-user chat surface.
- Review process-log and tool-result rendering in `/playground`; remove or collapse any layers that duplicate the visible answer or read like debug panels for non-technical users.

## Expected Impact Surface

### Likely to change

- `web/app/(workspace)/playground/page.tsx`
- `web/components/common/AssistantResponse.tsx`
- `web/components/common/ProcessLogs.tsx`

### Reviewed but expected to remain unchanged unless implementation reveals a hard dependency

- `web/components/chat/home/ChatMessages.tsx`
- `web/components/chat/home/TracePanels.tsx`
- `web/locales/en/app.json`
- `web/locales/vi/app.json`

## Tests To Run

- `cd web && npx eslint "app/(workspace)/playground/page.tsx" "components/common/AssistantResponse.tsx" "components/common/ProcessLogs.tsx"`
- `cd web && npm run build`
- `cd /Users/nguyenhuuloc/Documents/Multiagent-learning-platform && git diff --check`

## Non-Goals

- No route or capability changes.
- No backend or WebSocket protocol changes.
- No removal of trace data from runtime payloads; only presentation changes for end users.
