# Two-Session Future Backlog

- Task ID: `OPS_TWO_SESSION_BACKLOG`
- Commit tag: `OPS-BACKLOG`
- Status: `Ready for future session startup`
- Branch recommendation:
  - `pod-a/teacher-action-loop`
  - `pod-b/runtime-binding-coverage`

## Goal

Provide a stable AI-first startup contract for future product work after the contest MVP and risk-hardening lanes are complete.

This packet does not start a new implementation lane by itself. It explains how a human or AI worker should choose work from the `F101-F124` backlog already recorded in `ai_first/TASK_REGISTRY.json`.

## Current Truth

- No AI implementation task is active by default on `main`.
- Human review and final submission work remain separate from this packet.
- If new product work is opened, this packet is the preferred starting point for a two-session split.

## Session Buckets

### Session A — Teacher-Facing Workflow

Primary layers:
- `teacher-workflow`
- `teacher-insight`
- `teacher-quality-control`

Typical task IDs:
- `F101` through `F112`

Recommended first task:
- `F101_TEACHER_ACTION_EXECUTION_LOOP`

Typical owned files:
- `web/components/dashboard/`
- `web/app/(workspace)/dashboard/`
- `web/app/(workspace)/dashboard/student/`
- `web/components/assessment/` for bounded teacher-review controls
- `docs/superpowers/pr-notes/`

Do not touch by default:
- `deeptutor/services/runtime_policy/`
- `deeptutor/services/session/`
- student-model schema or evidence internals owned by Session B
- `ai_first/TASK_REGISTRY.json` unless the packet is being explicitly revised

### Session B — Runtime, Evidence, And Data Contracts

Primary layers:
- `runtime-policy`
- `student-model`
- `validation-ops`

Typical task IDs:
- `F113` through `F124`

Recommended first task:
- `F113_CAPABILITY_WIDE_RUNTIME_BINDING_COVERAGE`

Typical owned files:
- `deeptutor/services/runtime_policy/`
- `deeptutor/services/evidence/`
- `deeptutor/services/session/`
- related backend routers and tests for bounded contract updates
- `ai_first/evidence/` and bounded validation docs when required by the task

Do not touch by default:
- teacher-facing dashboard presentation files owned by Session A
- broad `/agents` UX copy or teacher workflow surfaces unless the task packet explicitly expands scope
- `ai_first/TASK_REGISTRY.json` unless the packet is being explicitly revised

## First-Start Order

If exactly two sessions are open, start with:

1. `Session A`
   `F101_TEACHER_ACTION_EXECUTION_LOOP`
2. `Session B`
   `F113_CAPABILITY_WIDE_RUNTIME_BINDING_COVERAGE`

Why this pair:
- both are foundational follow-ups to already-merged contest work
- they deepen the product in visible ways without requiring a larger architecture reset
- they minimize cross-session conflict on the first pass

## Now / Next / Later

### Now

- `Session A`
  - `F101_TEACHER_ACTION_EXECUTION_LOOP`
- `Session B`
  - `F113_CAPABILITY_WIDE_RUNTIME_BINDING_COVERAGE`

### Next

After the first pair merges cleanly:

- `Session A`
  - `F102_INTERVENTION_ASSIGNMENT_FLOW`
  - `F103_RECOMMENDATION_ACKNOWLEDGEMENT_AND_STATUS`
  - `F108_DIAGNOSIS_FEEDBACK_CAPTURE`
- `Session B`
  - `F114_SPEC_VERSION_PINNING_PER_SESSION`
  - `F116_STUDENT_MODEL_ENRICHMENT`
  - `F119_ABSTAIN_AND_WEAK_EVIDENCE_REFINEMENT`

### Later

Use the later set once the product is moving beyond contest-demo depth:

- `Session A`
  - `F104`
  - `F105`
  - `F106`
  - `F107`
  - `F109`
  - `F110`
  - `F111`
  - `F112`
- `Session B`
  - `F115`
  - `F117`
  - `F118`
  - `F120`
  - `F121`
  - `F122`
  - `F123`
  - `F124`

## One-Session Fallback

If only one session is available:

- choose `F101_TEACHER_ACTION_EXECUTION_LOOP` first when the goal is more obvious teacher value
- choose `F113_CAPABILITY_WIDE_RUNTIME_BINDING_COVERAGE` first when the goal is stronger architecture trust and future extensibility

Do not start both a teacher-facing task and its runtime/data prerequisite in one mixed branch unless a fresh packet explicitly widens the owned-file scope.

## Conflict Rules

Stop and ask the human before editing if:

- a Session A task needs to change `deeptutor/services/runtime_policy/` or session runtime contracts
- a Session B task needs to redesign dashboard UX or teacher workflow copy
- two sessions both want to update the same dashboard payload contract
- a new task would require revising task dependencies or introducing a third active session

## Next AI Should Read

1. `AGENTS.md`
2. `ai_first/AI_OPERATING_PROMPT.md`
3. `ai_first/ACTIVE_ASSIGNMENTS.md`
4. `ai_first/TASK_REGISTRY.json`
5. this packet
6. the specific task's spec/plan/PR note once the human picks a task

## Suggested Next Action

If the human wants to open two fresh product sessions:

1. create one worktree from `origin/main` for `pod-a/teacher-action-loop`
2. create one worktree from `origin/main` for `pod-b/runtime-binding-coverage`
3. mark both assignments in `ai_first/ACTIVE_ASSIGNMENTS.md`
4. create one task packet per concrete `F` task before code edits begin
