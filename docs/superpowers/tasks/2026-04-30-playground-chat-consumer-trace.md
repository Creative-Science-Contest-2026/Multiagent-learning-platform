# Task Packet: Playground Chat Consumer Trace

- Task ID: `UI-PLAYGROUND-CONSUMER-TRACE`
- Date: 2026-04-30
- Branch: `fix/playground-chat-consumer-trace`
- Status: Spec written

## Objective

Bring `/playground` chat turns back toward the original consumer-chat aesthetic while keeping stage traces visible in a compact, professional, non-debug presentation.

## User-Approved Scope

- Keep `Thinking / Acting / Observing / Responding` visible.
- Make those stages render compactly and professionally, closer to the original chat UI.
- Shrink the user bubble and keep it light gray.
- Hide metadata from end users.
- Remove duplicate or overly heavy visual blocks that make one chat turn consume too much screen height.

## Owned Files

- `web/app/(workspace)/playground/page.tsx`
- `web/components/common/AssistantResponse.tsx`
- `web/components/common/ProcessLogs.tsx`
- `web/components/chat/home/ChatMessages.tsx`
- `web/components/chat/home/TracePanels.tsx`
- `web/locales/en/app.json`
- `web/locales/vi/app.json`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-playground-chat-consumer-trace.md`
- `docs/superpowers/specs/2026-04-30-playground-chat-consumer-trace-design.md`
- `docs/superpowers/pr-notes/2026-04-30-playground-chat-consumer-trace.md`

## Do-Not-Touch

- Backend capability implementations
- Route structure outside `/playground`
- Hidden `guide` and `co-writer` work
- Untracked files outside this task scope

## Design Before Implementation

Reference spec:

- `docs/superpowers/specs/2026-04-30-playground-chat-consumer-trace-design.md`

## Codebase Survey Summary

- The current `/playground` page owns a local `TracePanel` that is heavier than the original chat UI.
- The original consumer-chat feel already exists in `ChatMessages.tsx` and `TracePanels.tsx`.
- The new implementation should adapt `/playground` toward those reference surfaces instead of inventing another styling system.

## Validation Plan

- `cd web && npx eslint "app/(workspace)/playground/page.tsx" "components/common/AssistantResponse.tsx" "components/common/ProcessLogs.tsx"`
- `cd web && npm run build`
- `cd /Users/nguyenhuuloc/Documents/Multiagent-learning-platform && git diff --check`

## Handoff Notes

- This lane is presentation-only.
- Do not remove trace data from runtime payloads.
- If implementation reveals duplicated answer rendering between final message content and result metadata, prefer collapsing it in the UI rather than mutating upstream data contracts.
