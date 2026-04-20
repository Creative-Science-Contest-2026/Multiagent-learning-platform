# Feature Pod Task: AI-Powered Assessment Recommendations

Owner: Codex
Branch: `pod-a/t015-assessment-recommendations`
GitHub Issue: `#55`

## Goal

Generate the next recommended assessment focus for a student based on recent assessment performance and known weak topics.

## User-visible outcome

- A student or teacher can request the next suggested assessment focus instead of guessing the next topic manually.
- Recommendations are grounded in existing assessment analytics, not a second independent scoring model.
- The first version stays deterministic unless the current architecture clearly requires an LLM call.

## Owned files/modules

- `deeptutor/services/assessment/`
- `deeptutor/api/routers/`
- `tests/api/`
- `tests/services/`
- `docs/superpowers/tasks/2026-04-21-T015-assessment-recommendations.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-21.md`

## Do-not-touch files/modules

- `deeptutor/core/`
- `deeptutor/runtime/`
- Unrelated marketplace, settings, and dashboard UI files unless the task packet is updated first
- Root license and upstream attribution files

## API/data contract

- Prefer a small recommendation service under `deeptutor/services/assessment/`
- Reuse existing assessment review and dashboard analytics signals before adding new persistence
- Expose only the minimal API surface required for recommendation consumption

## Acceptance criteria

- The system can derive at least one next assessment recommendation from existing performance data.
- Recommendations explain the suggested focus topic or reason.
- Empty state is handled cleanly when there is not enough history.
- Backend behavior is covered by targeted tests.

## Required tests

- Targeted service and/or API tests for recommendation behavior
- Python compile or equivalent validation for touched backend files

## Manual verification

- Trigger recommendation generation with at least one weak-topic assessment history
- Confirm the recommendation points to an appropriate next topic or practice direction
- Confirm a user with no meaningful history gets a clean fallback response

## PR architecture note

- Must include Mermaid diagram.
- Must update `ai_first/architecture/MAIN_SYSTEM_MAP.md` if feature structure changes.

## Handoff notes

- `T014` is merged to `main` through PR `#54`.
- Start from the existing dashboard assessment analysis and review parsing before introducing any new recommendation logic.
