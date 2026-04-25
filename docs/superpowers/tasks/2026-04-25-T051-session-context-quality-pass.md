# Feature Pod Task: Tutor and Assessment Session Context Quality Pass

Owner:
Branch: `pod-b/t051-session-context-quality`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Improve session review and tutoring context quality so the contest learning loop feels less thin while staying inside the current session and reply flows.

## User-visible outcome

- Tutoring session context becomes easier to understand downstream.
- Assessment review has cleaner contextual support data.
- The learning loop feels more grounded without introducing a separate subsystem.

## Owned files/modules

- `deeptutor/api/routers/sessions.py`
- `deeptutor/agents/chat/agentic_pipeline.py`
- `web/lib/session-api.ts`
- `tests/api/test_assessment_router.py`
- `tests/api/test_session_review_router.py`
- `tests/agents/chat/test_agentic_followup_prompts.py`

## Do-not-touch files/modules

- `web/app/(workspace)/dashboard/`
- `web/components/assessment/`
- `web/locales/vi/`
- `ai_first/`

## API/data contract

This slice may refine session and tutoring payload detail, but it must stay within the existing session/review/reply flow families.

## Acceptance criteria

- Session review and tutoring traces expose cleaner context for downstream UI.
- Follow-up behavior remains grounded and testable.
- No new route family is introduced.

## Required tests

- `python3 -m pytest tests/api/test_assessment_router.py tests/api/test_session_review_router.py tests/agents/chat/test_agentic_followup_prompts.py -q`
- `python3 -m py_compile deeptutor/api/routers/sessions.py deeptutor/agents/chat/agentic_pipeline.py`
- `git diff --check`

## Manual verification

- Confirm session payloads remain consumable by the existing frontend client.
- Confirm the tutoring path still returns stable response structure.

## Parallel-work notes

- Confirm `ai_first/ACTIVE_ASSIGNMENTS.md` is updated before code starts.
- Do not modify Lane 1 screen files in this slice.
- If frontend exposure is needed, document the contract and hand off the UI work instead of widening scope here.

## PR architecture note

- Must include Mermaid diagram.
- Update `ai_first/architecture/MAIN_SYSTEM_MAP.md` only if session workflow structure changes materially.

## Handoff notes
