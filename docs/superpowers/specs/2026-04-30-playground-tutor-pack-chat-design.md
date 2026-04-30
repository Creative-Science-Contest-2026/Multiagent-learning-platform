# Playground Tutor Pack Chat Design

- Date: 2026-04-30
- Task ID: `UI-PLAYGROUND-TUTOR-PACK-CHAT`
- Branch: `fix/playground-tutor-pack-chat`

## Goal

Add `Gói gia sư` selection to `/playground` chat so each chat session is bound to exactly one imported marketplace tutor pack from the moment the session is created. The chat must restore that binding from history, show it in the UI, and block further sending if the bound pack is no longer available.

## Product framing

- User-facing term: `Gói gia sư`
- A `Gói gia sư` is broader than a plain knowledge base:
  - source knowledge
  - teacher-defined teaching method
  - tone, rules, and instructional behavior encoded in imported Markdown and pack metadata
- The current chat should speak in this product language even if the runtime still uses `knowledge_bases` under the hood.

## Current Behavior

- `/playground` chat currently relies on `UnifiedChatContext` session state and sends `knowledgeBases` as a list in each request snapshot.
- The right panel shows current `Knowledge source`, but that is still a technical knowledge-base selection surface, not a tutor-pack workflow.
- New chat sessions do not require selecting an imported marketplace pack.
- Session history currently restores:
  - capability
  - enabled tools
  - knowledge bases
  - language
- Session history does not currently expose a first-class `Gói gia sư` binding or its availability status.
- If a knowledge base disappears, the UI has no dedicated session-level behavior for “history remains readable but sending is blocked”.

## Intended Behavior Change

- Every `/playground` chat session in `Trò chuyện` mode must be bound to exactly one imported `Gói gia sư`.
- When the user starts a new chat:
  - if only one imported tutor pack is available, auto-bind it
  - if multiple imported tutor packs are available, the user must pick one before sending
- Once a session is created, the bound tutor pack cannot be changed inside that session.
- Session history must restore the exact bound tutor pack.
- The sidebar must show a compact tutor-pack badge under the session title.
- If the bound tutor pack is deleted or becomes unavailable:
  - history still opens
  - sending new messages is blocked
  - the UI explains that the bound tutor pack is no longer available

## Codebase Survey

### Entry points and handlers

- `web/app/(workspace)/playground/page.tsx`
  - current chat workspace shell and right-panel context for `/playground`
  - currently wires `UnifiedChatContext` state into the visible chat UI
- `web/components/sidebar/WorkspaceSidebar.tsx`
  - loads sessions from history and opens them
- `web/context/UnifiedChatContext.tsx`
  - source of truth for chat session state, request snapshots, hydration, and message sending
- `web/lib/session-api.ts`
  - FE session contracts for list/detail hydration
- `deeptutor/api/routers/sessions.py`
  - returns session summary/detail payloads
- `deeptutor/services/session/turn_runtime.py`
  - persists session preferences when a turn starts

### Primary service or use-case modules

- `web/lib/marketplace-api.ts`
  - marketplace pack listing/import API helpers
- `web/app/(utility)/knowledge/page.tsx`
  - current imported knowledge-base management surface
- `deeptutor/api/routers/marketplace.py`
  - import pipeline and marketplace metadata exposure

### Shared contracts, schemas, or types

- `web/context/UnifiedChatContext.tsx`
  - `ChatState`, `MessageRequestSnapshot`, `LOAD_SESSION` payload
- `web/lib/session-api.ts`
  - `SessionSummary.preferences`
  - `SessionDetail.preferences`
- `deeptutor/services/session/sqlite_store.py`
  - session `preferences_json` already supports additive metadata keys

### Adjacent or reused flows inspected

- history restore on `/playground` already rehydrates from `UnifiedChatContext`
- session preferences already carry `agent_spec_pin`, so the repo already uses additive preference metadata for runtime-adjacent binding
- dashboard and review flows read `preferences.knowledge_bases`, so the new field must not break existing readers

### Closest existing tests

- no focused test currently covers tutor-pack binding in `/playground`
- current validation path relies on targeted lint/build plus existing session and chat behavior smoke coverage

## Candidate Approaches

### Approach A: Infer `Gói gia sư` only from `knowledge_bases[0]`

- Do not add new session metadata.
- Treat the single selected knowledge base as the tutor pack.
- Pros:
  - smallest backend diff
  - reuse current request contract almost entirely
- Cons:
  - product language becomes leaky because the UI can only see a KB name
  - weak support for `unavailable` status and future pack-specific behavior
  - ambiguous if later the runtime allows pack metadata or teaching-method rules beyond raw KB identity

### Approach B: Add a thin `tutor_pack` binding to session preferences while still sending one `knowledge_base`

- Persist a first-class tutor-pack object in session preferences, for example:
  - `tutor_pack.name`
  - `tutor_pack.knowledge_base`
  - `tutor_pack.status`
- Keep runtime message execution mapped to `knowledge_bases: [knowledge_base]`.
- Pros:
  - correct user-facing language
  - stable history badge and unavailable-state handling
  - preserves the current chat runtime seam
  - easy to extend later with pack version, owner, or teaching-style metadata
- Cons:
  - requires additive session contract updates across FE and backend

### Approach C: Build a separate chat-profile runtime for tutor packs

- Introduce a new top-level runtime object distinct from session preferences and knowledge bases.
- Pros:
  - strongest long-term domain separation
- Cons:
  - too wide for this lane
  - touches runtime orchestration, import flow, and session model more deeply than needed

## Chosen Approach

Approach B.

The product needs a real `Gói gia sư` concept in session history and UI, but the current runtime already accepts `knowledge_bases` cleanly. A thin `tutor_pack` binding in session preferences gives the UI the right semantics while keeping orchestration changes bounded.

## Planned Changes

### Session preference contract

- Extend stored session preferences with a new additive field:
  - `tutor_pack`
    - `name: string`
    - `knowledge_base: string`
    - `status: "available" | "missing"`
- Keep existing `knowledge_bases` list for runtime compatibility.
- For a tutor-pack-bound chat session, `knowledge_bases` should still be exactly `[knowledge_base]`.

### New chat creation flow

- `/playground` chat mode must compute the list of imported tutor packs available to the user.
- If there is one available pack, auto-bind it on new-session creation.
- If there are multiple, show a pack-selection step before allowing the first send.
- The first real send persists both:
  - `preferences.knowledge_bases`
  - `preferences.tutor_pack`

### Session restore flow

- `UnifiedChatContext.loadSession()` must hydrate:
  - current pack binding
  - availability state
- `/playground` must render the restored pack in the main chat UI and right-panel context.

### Unavailable-pack behavior

- If a restored session points at a tutor pack whose underlying knowledge base no longer exists:
  - show historical messages normally
  - set the session pack state to `missing`
  - disable composer submission for that session
  - render a clear warning explaining that the bound `Gói gia sư` is no longer available

### Sidebar history

- Each session row in the workspace sidebar should show a compact tutor-pack badge below the title when available.
- If the pack is missing, the badge or helper text should reflect that degraded state in a compact way.

## Expected Impact Surface

### Likely to change

- `web/app/(workspace)/playground/page.tsx`
- `web/context/UnifiedChatContext.tsx`
- `web/components/sidebar/WorkspaceSidebar.tsx`
- `web/lib/session-api.ts`
- `deeptutor/api/routers/sessions.py`
- `deeptutor/services/session/turn_runtime.py`

### Reviewed but expected to remain unchanged unless implementation reveals a small adapter need

- `web/lib/marketplace-api.ts`
- `web/app/(utility)/knowledge/page.tsx`
- `deeptutor/api/routers/marketplace.py`
- `deeptutor/services/session/sqlite_store.py`

## Tests To Add or Run

- FE:
  - `cd web && npx eslint "app/(workspace)/playground/page.tsx" "context/UnifiedChatContext.tsx" "components/sidebar/WorkspaceSidebar.tsx" "lib/session-api.ts"`
  - `cd web && npm run build`
- Backend:
  - targeted session router/runtime validation if a suitable test seam exists
- Behavior checks:
  - single imported pack auto-binds on new chat
  - multiple imported packs force explicit selection before first send
  - history restore reopens the correct bound pack
  - deleted pack still shows history but blocks send
  - sidebar badge shows the bound tutor pack
- Final hygiene:
  - `git diff --check`

## Non-Goals

- No multi-pack selection in one session
- No in-session pack switching
- No marketplace prompt/preset sharing in this lane
- No broad marketplace authoring redesign
