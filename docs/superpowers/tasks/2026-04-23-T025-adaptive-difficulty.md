# Feature Pod Task: Assessment Difficulty Adaptive Adjustment

Owner: Codex
Branch: `pod-a/t025-adaptive-difficulty`
GitHub Issue: `#73`

## Goal

Add an MVP adaptive difficulty flow for `deep_question` so auto-selected quizzes react to the learner's recent quiz performance instead of always staying static.

## User-visible outcome

- A quiz request with difficulty set to `auto` adjusts toward easier, medium, or harder questions based on recent quiz performance recorded in the same session context.
- Explicit difficulty requests such as `easy`, `medium`, or `hard` still win and bypass the adaptive logic.
- Generated quiz summaries record which difficulty was selected and why, so follow-up debugging is possible.

## Owned files/modules

- `deeptutor/agents/question/coordinator.py`
- `tests/agents/question/test_coordinator.py`
- `docs/superpowers/tasks/2026-04-23-T025-adaptive-difficulty.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-23.md`

## Do-not-touch files/modules

- Frontend quiz UI and dashboard files in this slice
- `deeptutor/core/`
- `deeptutor/runtime/`
- Root license and upstream attribution files

## API/data contract

- Keep the public `deep_question` request contract backward-compatible.
- Treat adaptive difficulty as a coordinator-side inference when the request difficulty is blank or `auto`.
- Persist the selected difficulty decision inside the generation summary trace instead of introducing a new storage model in this slice.

## Acceptance criteria

- `generate_from_topic()` derives a difficulty for auto mode from recent `[Quiz Performance]` context.
- A strong recent score selects a harder difficulty; a weak recent score selects an easier one; mixed performance keeps medium.
- Explicit request difficulty still overrides any inferred adaptive difficulty.
- Summary metadata exposes the adaptive difficulty decision for inspection.

## Required tests

- Coordinator unit coverage for adaptive difficulty selection and explicit override behavior

## Manual verification

- Start a quiz session and record quiz results into the same session history
- Generate a new quiz with difficulty `auto`
- Confirm the resulting summary trace shows the inferred difficulty level

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.

## Handoff notes

- `T024` merged to `main` through PR `#72`.
- Keep the first slice backend-only and session-context-driven; do not expand into new frontend controls or a new persistence table unless this MVP slice proves insufficient.
