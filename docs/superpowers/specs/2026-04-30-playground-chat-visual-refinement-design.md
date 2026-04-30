# Spec: Playground Chat Visual Refinement

Date: 2026-04-30
Task ID: `UI_PLAYGROUND_CHAT_VISUAL_REFINEMENT`
Branch: `fix/playground-chat-visual-refinement`

## Goal

Make the `/playground` chat interface feel lighter, more minimal, and more refined without removing any of the trace and metadata surfaces that are still useful for product visibility.

## Current behavior

- The chat shell already works functionally, but the visual treatment feels raw.
- The user bubble is too dark and stands out in a heavy way against the rest of the page.
- Trace blocks such as `Thinking`, `Acting`, `Observing`, `Responding`, tool results, process logs, and metadata feel like stacked debug components instead of subtle supporting UI.
- The current presentation exposes too many hard boxes and strong boundaries, making the conversation area feel busy and coarse.

## Intended behavior

- Keep the conversation-first layout intact.
- Keep trace, process, and metadata surfaces available in the main chat flow.
- Make those technical surfaces calmer by default:
  - collapsed where possible
  - lighter background tones
  - smaller, subtler headers
  - softer borders and less card-like heaviness
- Change the user bubble from near-black to a lighter, same-family tone that still distinguishes it from assistant output.
- Ensure the overall visual language feels restrained, elegant, and minimal.

## Approaches considered

### Approach 1: Palette-only adjustment

Only change colors and leave all structural wrappers the same.

- Pros: minimal diff
- Cons: keeps the “raw component stack” feeling

### Approach 2: Visual refinement with same runtime structure

Keep the same data surfaces and same rendering order, but restyle bubbles, accordions, process logs, and metadata into a quieter, more integrated UI.

- Pros: best balance of impact and safety
- Pros: no backend or data-flow risk
- Cons: requires coordinated edits across several render surfaces

### Approach 3: Separate debug surfaces from the chat entirely

Move process and metadata out of the chat body into a separate panel or mode.

- Pros: cleanest conversation view
- Cons: conflicts with the requirement to keep those surfaces visible in the chat

## Chosen approach

Use approach 2.

The user explicitly wants the technical surfaces kept, just not rendered in a crude way. That makes a presentation-only refinement pass the right solution.

## Planned changes

### 1. Chat bubble refinement

- Soften the user bubble from dark charcoal to a much lighter neutral tone.
- Keep user and assistant bubbles distinguishable, but only with gentle contrast.
- Slightly reduce the sensation of stacked cards by using lighter fills and quieter shadows.

### 2. Trace surface refinement

- Keep `Thinking`, `Acting`, `Observing`, and `Responding`.
- Make them collapsed by default.
- Reduce border contrast and shift toward subtle accordion rows instead of obvious boxed panels.
- Tone down tool-call and tool-result sub-cards so they feel like annotations, not separate apps inside the chat.

### 3. Process log and metadata refinement

- Keep `Process` and `Metadata` visible and accessible.
- Make them default closed where possible.
- Use calmer typography and softer containers.
- Treat JSON-like metadata as supporting evidence, not a dominant content block.

### 4. Composer refinement

- Preserve the command-bar pattern added earlier.
- Reduce visual heaviness so it sits naturally in the page rather than appearing as another hard card.

## Files expected to change

- `web/app/(workspace)/playground/page.tsx`
- `web/components/common/AssistantResponse.tsx`
- `web/components/common/ProcessLogs.tsx`
- `web/components/chat/home/PlaygroundRightPanel.tsx`
- `docs/superpowers/tasks/2026-04-30-playground-chat-visual-refinement.md`
- `docs/superpowers/specs/2026-04-30-playground-chat-visual-refinement-design.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`

## Files reviewed but expected to remain unchanged

- backend stream contracts and execution logic
- route-selection logic inside the playground shell
- non-playground routes
- hidden Guided Learning and Co-Writer lanes

## Testing

- `cd web && npx eslint "app/(workspace)/playground/page.tsx" "components/common/AssistantResponse.tsx" "components/common/ProcessLogs.tsx" "components/chat/home/PlaygroundRightPanel.tsx"`
- `cd web && npm run build`

## Risks

- Too much visual softening can make technical surfaces hard to notice; the refinement must preserve discoverability.
- Default-collapsing traces changes first-glance behavior, so the summary headers need to remain clear enough to invite expansion.

## Out of scope

- Removing traces or metadata entirely
- Reworking capability execution flow
- Changing sidebar structure or route behavior
