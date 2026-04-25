# Feature Pod Task: Smart Tutor Follow-Up Questions

Owner: Codex
Branch: `pod-a/t031-tutor-follow-ups`
GitHub Issue: `#83`

## Goal

Add a lightweight tutor follow-up slice so the tutoring flow can suggest 1-3 next questions when a student response shows likely misunderstanding.

## User-visible outcome

- Tutor responses can optionally include short follow-up questions that help the learner continue instead of stopping after a single answer.
- The first slice should stay compatible with the current tutoring chat flow when no follow-up is needed.
- Follow-up generation should be grounded in the latest learner response and current tutoring context.

## Owned files/modules

- `deeptutor/agents/chat/agentic_pipeline.py`
- `deeptutor/agents/chat/prompts/en/chat_agent.yaml`
- `deeptutor/agents/chat/prompts/vi/chat_agent.yaml` if the prompt contract changes
- `tests/agents/chat/` covering the selected tutor follow-up slice
- `docs/superpowers/tasks/2026-04-24-T031-tutor-follow-up-prompts.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-24.md`

## Do-not-touch files/modules

- Marketplace, knowledge-pack management, dashboard analytics, and assessment review flows
- Unrelated API routers and session-history code
- `deeptutor/core/`
- `deeptutor/runtime/` unless the task packet is updated first
- Root license and upstream attribution files

## API/data contract

- Preserve current tutoring behavior when follow-up prompts are absent.
- Keep the first slice inside the existing assistant response text and optional `result` metadata; do not introduce a new route family.
- Keep the first slice backend-only unless a contract gap forces a follow-up task.

## Acceptance criteria

- Tutor flow can emit 1-3 follow-up questions when the latest learner answer indicates confusion or partial understanding.
- Tutor flow remains clean when no follow-up is needed.
- Regression coverage exists for the chosen generation path.

## Required tests

- Tutor-agent regression coverage for follow-up generation
- Frontend production build verification only if UI/event typing changes are made

## Manual verification

- Run a tutoring exchange where the student gives an incomplete or incorrect answer
- Confirm the tutor output includes actionable follow-up questions instead of only a generic reply

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.

## Handoff notes

- `T030` merged to `main` through PR `#82`.
- Start by reading the current tutor response flow and narrow the owned-file set if the smallest useful slice can stay inside the tutor agent only.
