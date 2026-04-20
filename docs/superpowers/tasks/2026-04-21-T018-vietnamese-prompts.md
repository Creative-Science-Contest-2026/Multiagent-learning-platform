# Feature Pod Task: Vietnamese LLM Prompt Variants

Owner: Codex
Branch: `pod-a/t018-vietnamese-prompts`
GitHub Issue: `#61`

## Goal

Add Vietnamese prompt variants for the main agent prompt families so Vietnamese UI flows produce Vietnamese AI responses.

## User-visible outcome

- When the UI language is `vi`, agent prompt loading resolves to Vietnamese prompt content where variants exist.
- The first version covers the main agent prompt families used in the MVP path.
- Existing fallback behavior remains intact for prompt files that do not yet have a Vietnamese variant.

## Owned files/modules

- `deeptutor/agents/*/prompts/vi/`
- `deeptutor/services/prompt/` only if prompt discovery or fallback wiring requires it
- `tests/` covering prompt loading or prompt selection if needed
- `docs/superpowers/tasks/2026-04-21-T018-vietnamese-prompts.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-21.md`

## Do-not-touch files/modules

- `deeptutor/core/`
- `deeptutor/runtime/`
- Unrelated marketplace, dashboard, notebook, and settings files unless task scope expands
- Root license and upstream attribution files

## API/data contract

- Prefer adding prompt files over code changes wherever possible
- Preserve current `vi -> en` fallback chain
- Keep the first pass focused on MVP-critical agent prompt families

## Acceptance criteria

- Vietnamese prompt variants exist for the MVP-relevant agent prompt families.
- Prompt resolution still falls back safely when a Vietnamese file is absent.
- Validation covers prompt discovery or at least verifies file presence and loading path.

## Required tests

- Prompt loading/discovery validation for touched families, or explain if only file-level validation is available
- Any targeted backend validation needed for changed prompt-loading code

## Manual verification

- Set UI language to Vietnamese
- Trigger representative solve/question/tutor flows
- Confirm generated AI responses use Vietnamese prompts instead of English defaults

## PR architecture note

- Must include Mermaid diagram.
- Must update `ai_first/architecture/MAIN_SYSTEM_MAP.md` if feature structure changes.

## Handoff notes

- `T017` is merged to `main` through PR `#60`.
- Start from existing prompt family layout and fallback rules before changing prompt manager behavior.
