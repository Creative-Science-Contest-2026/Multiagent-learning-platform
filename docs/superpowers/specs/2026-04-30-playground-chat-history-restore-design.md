# Playground Chat History Restore Design

- Date: 2026-04-30
- Task ID: `BUG-PLAYGROUND-CHAT-HISTORY-RESTORE`
- Branch: `fix/playground-chat-history-restore`

## Goal

Restore the ability to click an existing chat session in the sidebar and have `/playground` show that historical conversation again for the standard `chat` capability.

## Current Behavior

- `WorkspaceSidebar` still calls `loadSession(sessionId)` from `UnifiedChatContext`.
- `UnifiedChatContext` still fetches the session and hydrates the real message history into context state.
- `/playground` no longer reads that context for its `chat` mode.
- Instead, `CapabilityTester` and the other playground testers keep their own local `messages` arrays with `useState`.
- Result: selecting a prior session updates context, but the center chat panel stays on its local state and appears broken.

## Intended Behavior Change

- When the active playground mode is `chat`, the center chat panel must render from `UnifiedChatContext`.
- Clicking a previous session in the sidebar must immediately show that session’s messages in `/playground`.
- Sending a new chat message from `/playground` chat mode must continue through `UnifiedChatContext` so history and live chat stay on the same source of truth.
- Non-chat capability testers (`deep_solve`, `deep_question`, `deep_research`) remain unchanged in this lane.

## Codebase Survey

### Entry points and handlers

- `web/app/(workspace)/playground/page.tsx`
  - owns the `/playground` shell and currently chooses which tester surface to render
- `web/components/sidebar/WorkspaceSidebar.tsx`
  - dispatches `loadSession(sessionId)` on history click

### Primary service or use-case modules

- `web/context/UnifiedChatContext.tsx`
  - authoritative session hydration, message streaming, selected session state

### Shared contracts, schemas, or types

- `MessageItem`, `ChatState`, `SendMessageOptions` in `UnifiedChatContext`
- `StreamEvent` in the existing chat rendering pipeline

### Adjacent or reused flows inspected

- `web/components/chat/home/ChatMessages.tsx`
  - existing history-aware message list already wired for hydrated sessions
- `web/components/chat/home/ChatComposer.tsx`
  - existing composer behavior for context-backed chat flows

### Closest existing tests

- No focused `/playground` history test currently exists.
- Existing validation will rely on ESLint, build, and targeted manual code-path inspection unless a narrow test seam is practical.

## Candidate Approaches

### Approach A: Keep `/playground` local state and add a second session-fetch path

- On session click, call the session API again directly inside `/playground` and sync local tester state.
- Pros:
  - minimal reshaping of current page structure
- Cons:
  - duplicates session hydration logic
  - creates two competing sources of truth for the same chat route
  - likely to regress again

### Approach B: Reconnect `/playground` chat mode to `UnifiedChatContext`

- Use context state for the `chat` capability only, while keeping the other capability testers local.
- Pros:
  - matches the original architecture
  - fixes sidebar selection and history replay at the source
  - avoids duplicate loading logic
- Cons:
  - requires careful split between `chat` mode and non-chat testers inside `/playground`

### Approach C: Move all playground capabilities into shared context immediately

- Broaden `UnifiedChatContext` to own every playground tester mode.
- Pros:
  - one long-term model
- Cons:
  - too broad for this bugfix
  - conflicts with the user’s request to defer capability cleanup to the next task

## Chosen Approach

Approach B.

The bug is caused by `/playground` chat mode drifting away from the existing session source of truth. Reconnecting only `chat` mode to `UnifiedChatContext` fixes the regression directly without broadening scope to the other capability testers.

## Planned Changes

- In `web/app/(workspace)/playground/page.tsx`:
  - detect when the active capability is `chat`
  - render the main chat surface from `useUnifiedChat().state.messages`
  - route send/cancel behavior through `sendMessage` and `cancelStreamingTurn`
- Reuse the existing message/composer components where practical instead of maintaining a second local chat implementation.
- Keep `deep_solve`, `deep_question`, and `deep_research` on their current local tester state in this lane.

## Expected Impact Surface

### Likely to change

- `web/app/(workspace)/playground/page.tsx`

### Reviewed but expected to remain unchanged unless implementation reveals a hard dependency

- `web/context/UnifiedChatContext.tsx`
- `web/components/chat/home/ChatMessages.tsx`
- `web/components/chat/home/ChatComposer.tsx`
- `web/components/sidebar/WorkspaceSidebar.tsx`

## Tests To Run

- `cd web && npx eslint "app/(workspace)/playground/page.tsx"`
- `cd web && npm run build`
- `cd /Users/nguyenhuuloc/Documents/Multiagent-learning-platform && git diff --check`

## Non-Goals

- No hiding or removing capabilities in this lane.
- No backend changes.
- No session schema changes.
