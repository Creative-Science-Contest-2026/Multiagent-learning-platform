# Task Packet: Playground Reasoning Wrap Fix

- Task ID: `UI-PLAYGROUND-REASONING-WRAP`
- Date: 2026-04-30
- Branch: `fix/chat-reasoning-wrap`
- Status: Spec written

## Objective

Fix `/playground` trace rendering so streamed `Reasoning` text displays as normal sentences instead of one word or token per line, while keeping `Acting`, `Tool call`, and the rest of the trace surface intact.

## User-Approved Scope

- Use a separate worktree for this lane.
- Fix the chat UI issue where `Reasoning` content wraps into many short lines because each streamed chunk is rendered separately.
- Keep the existing trace sections and overall playground UI behavior.

## Owned Files

- `web/app/(workspace)/playground/page.tsx`
- `web/lib/playground-trace.ts`
- `web/tests/playground-trace.test.ts`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-playground-reasoning-wrap-fix.md`
- `docs/superpowers/specs/2026-04-30-playground-reasoning-wrap-fix-design.md`
- `docs/superpowers/pr-notes/2026-04-30-playground-reasoning-wrap-fix.md`

## Do-Not-Touch

- Backend streaming protocol and capability implementations
- Shared trace panel UX outside `/playground`
- Existing active lanes in other worktrees
- Untracked files from the repo-root checkout

## Design Before Implementation

Reference spec:

- `docs/superpowers/specs/2026-04-30-playground-reasoning-wrap-fix-design.md`

## Codebase Survey Summary

- `/playground` still owns a local `TracePanel` implementation inside `web/app/(workspace)/playground/page.tsx`.
- That local panel renders each `thinking` event as its own paragraph, which is incompatible with token-streamed reasoning chunks.
- The shared chat trace renderer in `web/components/chat/home/TracePanels.tsx` already reconstructs trace text by joining chunks before markdown rendering, so the bug is bounded to the local playground trace surface.

## Validation Plan

- `cd web && node --test tests/playground-trace.test.ts`
- `cd web && npx eslint "app/(workspace)/playground/page.tsx" "lib/playground-trace.ts" "tests/playground-trace.test.ts"`
- `cd /Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.worktrees/fix-chat-reasoning-wrap && git diff --check`

## Handoff Notes

- Prefer a local UI-layer fix over backend stream changes unless new evidence disproves the root cause.
- Preserve the existing stage grouping and tool/result cards in the playground trace.
