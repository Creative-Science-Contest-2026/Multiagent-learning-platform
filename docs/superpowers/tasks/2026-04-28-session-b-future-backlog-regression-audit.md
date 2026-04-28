# Task Packet: OPS_SESSION_B_FUTURE_BACKLOG_AUDIT

- Task ID: `OPS_SESSION_B_FUTURE_BACKLOG_AUDIT`
- Commit tag: `OPS-B-AUDIT`
- Owner: `Codex`
- Status: `completed`

## Objective

Audit the merged Session B future-backlog work (`F113-F124`) to confirm the shipped code still matches each task's bounded contract, the key validations still pass on current `main`, and no obvious regression or requirement drift remains hidden after the merge sequence.

## Owned Files

- `docs/superpowers/tasks/2026-04-28-session-b-future-backlog-regression-audit.md`
- `docs/superpowers/specs/2026-04-28-session-b-future-backlog-regression-audit-design.md`
- `docs/superpowers/plans/2026-04-28-session-b-future-backlog-regression-audit.md`
- `docs/superpowers/pr-notes/2026-04-28-session-b-future-backlog-regression-audit.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-28.md`
- bounded Session B implementation files only if the audit finds a concrete defect in:
  - `deeptutor/services/runtime_policy/`
  - `deeptutor/services/session/`
  - `deeptutor/services/evidence/`
  - `deeptutor/api/routers/{agent_specs,dashboard,system}.py`
  - `scripts/contest/`
  - `ai_first/evidence/`
  - matching bounded tests under `tests/`

## Do-Not-Touch

- teacher-facing dashboard frontend UX
- Session A task areas and their historical packets
- unrelated legacy worktrees or stale branches
- screenshot or video assets unless an audit finding proves one is structurally wrong

## Audit Scope

Review the merged Session B backlog slices:

- `F113_CAPABILITY_WIDE_RUNTIME_BINDING_COVERAGE`
- `F114_SPEC_VERSION_PINNING_PER_SESSION`
- `F115_RUNTIME_POLICY_AUDIT_TRACE`
- `F116_STUDENT_MODEL_ENRICHMENT`
- `F117_CONFIDENCE_CALIBRATION_REFINEMENT`
- `F118_MISCONCEPTION_TAXONOMY_EXPANSION`
- `F119_ABSTAIN_AND_WEAK_EVIDENCE_REFINEMENT`
- `F120_INTERVENTION_EFFECTIVENESS_TRACKING`
- `F121_CLASS_ROSTER_AND_GROUP_FOUNDATION`
- `F122_PILOT_FEEDBACK_INGESTION_PATH`
- `F123_CASEPACK_AND_EVALUATION_DATASET_EXPANSION`
- `F124_EVIDENCE_AUTOMATION_REFRESH`

## Acceptance Criteria

1. Each audited Session B task is checked against its packet/spec intent and current merged code.
2. A bounded validation bundle is rerun across the highest-risk Session B areas.
3. Any concrete defect or requirement drift found by the audit is fixed inside this lane with matching tests.
4. If no defect is found, the audit leaves a written proof artifact instead of silent reassurance.
5. AI-first tracking reflects the audit lane and the final review outcome.

## Validation

- task-specific pytest runs grouped by audited area
- `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null` if tracking files change
- `git diff --check`
