# Feature Pod Task: Tutoring Session Replay Feature

Owner: Codex
Branch: `pod-a/t021-session-replay`
GitHub Issue: `#67`

## Goal

Add a replay view for tutoring sessions so teachers can review conversation flow with timestamps and context.

## User-visible outcome

- Teachers can open a tutoring session replay from dashboard data.
- Replay shows the message timeline in order with timestamps.
- Existing dashboard and assessment review flows remain unchanged when replay is not used.

## Owned files/modules

- `web/app/(workspace)/dashboard/`
- `web/lib/dashboard-api.ts`
- `deeptutor/api/routers/dashboard.py` only if replay-specific API shaping is needed
- `tests/api/test_dashboard_router.py` if backend changes are required
- `docs/superpowers/tasks/2026-04-21-T021-session-replay.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-21.md`

## Do-not-touch files/modules

- Marketplace, knowledge, settings, and prompt files
- `deeptutor/core/`
- `deeptutor/runtime/`
- Root license and upstream attribution files

## API/data contract

- Prefer reusing existing session/dashboard APIs where possible.
- If new replay-specific data shaping is needed, keep existing dashboard payloads backward-compatible.

## Acceptance criteria

- Dashboard exposes a way to review tutoring session conversation flow.
- Replay view shows ordered user/tutor messages with timestamps.
- Replay remains scoped to teacher review and does not break assessment review routes.

## Required tests

- Backend regression coverage only if API changes are required
- Frontend build verification after replay UI wiring

## Manual verification

- Open dashboard
- Select a tutoring session
- Confirm replay shows the conversation timeline with readable ordering and timestamps

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.

## Handoff notes

- `T020` merged to `main` through PR `#66`.
- Start by inspecting current dashboard activity detail/session APIs before deciding whether replay needs a new route or only frontend rendering work.
