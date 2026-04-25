# T051 Session Context Quality Pass

## Objective

Improve tutoring and assessment session payload quality without changing route families or touching lane 1 UI files.

## Scope

- Add additive `context_support` fields to session and assessment review payloads.
- Emit compact `session_context` metadata from the tutoring pipeline result event.
- Extend session client types and targeted tests for the new payload depth.

## Steps

1. Add bounded session context helpers in `deeptutor/api/routers/sessions.py`.
2. Add result-event `session_context` metadata in `deeptutor/agents/chat/agentic_pipeline.py`.
3. Extend `web/lib/session-api.ts` types for the new context payload.
4. Add regression coverage in session-review and follow-up prompt tests.
5. Run the required pytest, py_compile, and diff checks.
