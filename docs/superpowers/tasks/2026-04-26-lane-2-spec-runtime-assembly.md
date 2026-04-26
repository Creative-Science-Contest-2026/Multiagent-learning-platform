# Feature Pod Task: Lane 2 Spec Runtime Assembly

Task ID: `L2_SPEC_RUNTIME_ASSEMBLY`
Commit tag: `L2`
Owner: Session-specific
Branch: `pod-a/spec-runtime-assembly`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Compile teacher policy into a predictable runtime contract shared by tutoring and assessment flows.

## User-visible outcome

- Tutor and assessment behavior can be shaped by the same teacher-defined spec pack.
- Runtime assembly uses explicit slices instead of a monolithic hidden prompt blob.
- The system is prepared for future multi-agent separation without redoing policy storage.

## Owned files/modules

- `deeptutor/services/runtime_policy/`
- `deeptutor/services/prompt/`
- `deeptutor/runtime/orchestrator.py`
- `deeptutor/capabilities/chat.py`
- `deeptutor/capabilities/deep_question.py`
- `tests/services/runtime_policy/`
- `tests/core/test_capabilities_runtime.py`
- `tests/services/test_prompt_manager.py`
- `docs/superpowers/tasks/2026-04-26-lane-2-spec-runtime-assembly.md`
- `docs/superpowers/pr-notes/*`

## Do-not-touch files/modules

- `deeptutor/services/evidence/`
- `deeptutor/api/routers/dashboard.py`
- `deeptutor/api/routers/assessment.py`
- `web/app/(workspace)/dashboard/`
- `web/components/dashboard/`
- `web/app/(utility)/knowledge/`

## API/data contract

- Runtime consumes a compiled teacher spec plus student/session state boundaries.
- Enforce source priority `teacher_kb > curriculum excerpt > teacher rules > llm prior knowledge`.
- Keep policy assembly separate from observation, diagnosis, and recommendation execution.

## Acceptance criteria

- Tutor and assessment code paths both consume the same runtime policy contract.
- `SOUL`, `RULES`, `WORKFLOW`, `ASSESSMENT`, and `KNOWLEDGE` influence runtime behavior through explicit slices.
- Runtime debug output can explain which slices were assembled for a request.
- No evidence or diagnosis logic is reimplemented inside prompt assembly.

## Required tests

- Focused capability/runtime tests for policy slice loading
- Prompt manager or runtime-policy service tests
- `git diff --check`

## Manual verification

- Run one tutoring session and one assessment session against the same authored pack.
- Verify policy changes alter runtime behavior in both paths.
- Verify knowledge-source priority behaves as documented.

## Parallel-work notes

- This lane depends on clear output contracts from Lane 1 but should not block on a polished authoring UI.
- If the spec format is unclear or unstable, ask the human for a contract decision rather than embedding a temporary assumption.
- Do not touch teacher insight UI or evidence storage in this lane.

## PR architecture note

- Must include Mermaid diagram.
- Must update `ai_first/architecture/MAIN_SYSTEM_MAP.md` because this lane changes runtime boundaries.

## Handoff notes

- This is Session = Lane 2.
- Coordinate with Lane 1 through documented compiled-pack format only.
- Coordinate with Lanes 3-5 through explicit `Teacher Spec / Student State / Session State` boundaries.
- Implemented runtime entry points now accept teacher policy through `teacher_spec`, `teacher_spec_compiled`, or `agent_spec_id` when those values are already present on the runtime context.
- Runtime prompt assembly now uses explicit named sections and keeps legacy behavior unchanged when no teacher policy is present.
