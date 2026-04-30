# Playground Reasoning Wrap Fix Design

- Date: 2026-04-30
- Task ID: `UI-PLAYGROUND-REASONING-WRAP`
- Branch: `fix/chat-reasoning-wrap`

## Goal

Make `/playground` trace `Reasoning` content render as continuous readable text during and after streaming, without changing the underlying stream payloads or removing the existing trace sections.

## Current Behavior

- The local `TracePanel` in `web/app/(workspace)/playground/page.tsx` groups events by stage.
- Inside each stage, it renders every `thinking` event as a separate paragraph.
- The chat pipeline streams reasoning in many small `thinking` chunks, often one token or short phrase at a time.
- As a result, the UI shows one short fragment per line, which looks like a width or wrapping bug even though the real problem is per-chunk block rendering.

## Intended Behavior Change

- Consecutive streamed `thinking` chunks in the same stage should be coalesced into one readable reasoning block before rendering.
- `progress`, `tool_call`, `tool_result`, and `error` rendering should keep their existing visual treatment unless a small compatibility adjustment is needed.
- No backend stream contract, event shape, or stage labeling changes.

## Codebase Survey

### Entry points and handlers

- `web/app/(workspace)/playground/page.tsx`
  - owns the local `TracePanel`
  - appends stream events into assistant messages in real time

### Primary service or use-case modules

- `web/lib/unified-ws.ts`
  - defines the frontend `StreamEvent` contract

### Shared contracts, schemas, or types

- `StreamEvent` carries tokenized `thinking` chunks and full tool/progress metadata

### Adjacent or reused flows inspected

- `web/components/chat/home/TracePanels.tsx`
  - reconstructs trace text by joining event chunks before rendering
- `web/context/UnifiedChatContext.tsx`
  - accumulates assistant content progressively but leaves event arrays untouched

### Closest existing tests

- `web/tests/markdown-display.test.ts`
  - shows the lightweight `node:test` pattern used by frontend utility tests

## Candidate Approaches

### Approach A: Widen the `Reasoning` container with CSS

- Pros:
  - very small diff
- Cons:
  - does not fix the actual problem because every streamed chunk is still a separate block
  - tool and progress rows are already rendering acceptably

### Approach B: Coalesce streamed `thinking` chunks in the local playground trace renderer

- Pros:
  - fixes the real root cause in the affected UI surface
  - preserves existing backend payloads and trace structure
  - easy to test with a small pure helper
- Cons:
  - requires a small utility extraction so the grouping logic is testable

### Approach C: Change backend streaming so reasoning arrives as larger chunks

- Pros:
  - could improve multiple consumers at once
- Cons:
  - broader runtime risk
  - touches server behavior outside the requested scope
  - unnecessary because the shared trace UI already handles chunked reasoning correctly

## Chosen Approach

Approach B.

The bug is local to `/playground` and comes from rendering tokenized `thinking` events one-by-one. Coalescing those chunks in the local trace renderer is the smallest correct fix with the lowest runtime risk.

## Planned Changes

- Add a small helper in `web/lib/playground-trace.ts` that converts a stage event list into render rows, merging consecutive `thinking` chunks into one combined text block.
- Update `web/app/(workspace)/playground/page.tsx` to render the local `TracePanel` from those normalized rows instead of raw event-by-event paragraphs.
- Add a focused test in `web/tests/playground-trace.test.ts` covering:
  - multiple streamed `thinking` chunks becoming one readable block
  - `tool_call` and `tool_result` rows staying distinct
  - non-thinking rows preserving order around the merged reasoning block

## Expected Impact Surface

### Likely to change

- `web/app/(workspace)/playground/page.tsx`
- `web/lib/playground-trace.ts`
- `web/tests/playground-trace.test.ts`

### Reviewed but expected to remain unchanged

- `web/components/chat/home/TracePanels.tsx`
- `web/context/UnifiedChatContext.tsx`
- `web/lib/unified-ws.ts`

## Tests To Run

- `cd web && node --test tests/playground-trace.test.ts`
- `cd web && npx eslint "app/(workspace)/playground/page.tsx" "lib/playground-trace.ts" "tests/playground-trace.test.ts"`
- `cd /Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/fix-chat-reasoning-wrap && git diff --check`

## Non-Goals

- No backend streaming changes
- No redesign of the shared chat trace components
- No changes to capability logic, tool execution, or message persistence
