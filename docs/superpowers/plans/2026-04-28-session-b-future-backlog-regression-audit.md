# Session B Future Backlog Regression Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Audit merged Session B backlog slices `F113-F124`, rerun their highest-risk validation bundles, and fix only concrete regressions or requirement drift uncovered by that audit.

**Architecture:** This lane is an audit-and-repair slice, not a feature lane. It starts by mapping each merged Session B task back to its packet/spec, then reruns grouped validations across runtime policy, evidence/diagnosis, and validation-ops areas, and only then applies minimal corrective patches if any review finding is proven.

**Tech Stack:** Markdown task artifacts, Python services, FastAPI routers, pytest, JSON validation, GitHub PR review flow

---

### Task 1: Establish the audit lane control plane

**Files:**
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/daily/2026-04-28.md`
- Create: `docs/superpowers/tasks/2026-04-28-session-b-future-backlog-regression-audit.md`
- Create: `docs/superpowers/specs/2026-04-28-session-b-future-backlog-regression-audit-design.md`
- Create: `docs/superpowers/plans/2026-04-28-session-b-future-backlog-regression-audit.md`

- [ ] Record the audit assignment, owned files, and branch/worktree in `ai_first/ACTIVE_ASSIGNMENTS.md`.
- [ ] Add a daily-log entry stating that this lane is a bounded Session B audit and not a new product backlog item.
- [ ] Create the packet/spec/plan trio so the audit has an explicit contract before code review or verification begins.

### Task 2: Review Session B runtime-policy slices against their packets

**Files:**
- Read: `docs/superpowers/tasks/2026-04-26-two-session-future-backlog.md`
- Read: `docs/superpowers/tasks/2026-04-26-f113-capability-wide-runtime-binding-coverage-design.md`
- Read: `docs/superpowers/tasks/2026-04-27-f114-spec-version-pinning-per-session.md`
- Read: `docs/superpowers/tasks/2026-04-27-f115-runtime-policy-audit-trace.md`
- Read/Inspect: `deeptutor/services/runtime_policy/`
- Read/Inspect: `deeptutor/services/agent_spec/`
- Read/Inspect: `deeptutor/services/session/turn_runtime.py`
- Read/Inspect: `deeptutor/api/routers/agent_specs.py`
- Test: `tests/services/runtime_policy/`
- Test: `tests/services/agent_spec/`
- Test: `tests/api/test_unified_ws_turn_runtime.py`
- Test: `tests/api/test_agent_specs_router.py`

- [ ] Map `F113-F115` packet claims to the current merged files and note any missing contract or overclaim.
- [ ] Rerun the grouped runtime-policy validations and confirm they still cover the promised bounded behavior.
- [ ] If the audit reveals a defect, write a failing regression test first, run it red, then patch the minimal implementation and rerun green.

### Task 3: Review evidence and student-model slices against their packets

**Files:**
- Read: `docs/superpowers/tasks/2026-04-27-f116-student-model-enrichment.md`
- Read: `docs/superpowers/tasks/2026-04-27-f117-confidence-calibration-refinement.md`
- Read: `docs/superpowers/tasks/2026-04-27-f118-misconception-taxonomy-expansion.md`
- Read: `docs/superpowers/tasks/2026-04-27-f119-abstain-and-weak-evidence-refinement.md`
- Read: `docs/superpowers/tasks/2026-04-28-f120-intervention-effectiveness-tracking.md`
- Read/Inspect: `deeptutor/services/evidence/`
- Test: `tests/services/evidence/`
- Test: `tests/api/test_dashboard_router.py`
- Test: `tests/api/test_assessment_router.py`

- [ ] Map `F116-F120` packet claims to the current merged diagnosis, confidence, abstain, taxonomy, and effectiveness code.
- [ ] Rerun the grouped evidence-layer validations and inspect whether later merges weakened earlier guarantees.
- [ ] If a defect appears, add the smallest failing regression proof first, then patch only the bounded evidence code and matching tests.

### Task 4: Review validation-ops and roster slices against their packets

**Files:**
- Read: `docs/superpowers/tasks/2026-04-28-f121-class-roster-and-group-foundation.md`
- Read: `docs/superpowers/tasks/2026-04-28-f122-pilot-feedback-ingestion-path.md`
- Read: `docs/superpowers/tasks/2026-04-28-f123-casepack-and-evaluation-dataset-expansion.md`
- Read: `docs/superpowers/tasks/2026-04-28-f124-evidence-automation-refresh.md`
- Read/Inspect: `deeptutor/services/session/sqlite_store.py`
- Read/Inspect: `deeptutor/api/routers/{dashboard,system}.py`
- Read/Inspect: `scripts/contest/`
- Read/Inspect: `ai_first/evidence/`
- Read/Inspect: `docs/contest/`
- Test: `tests/services/session/test_sqlite_store.py`
- Test: `tests/services/evidence/test_pilot_feedback.py`
- Test: `tests/services/evidence/test_validation_casepack.py`
- Test: `tests/scripts/test_refresh_evidence_status.py`
- Test: `tests/api/test_system_router.py`
- Test: `tests/api/test_dashboard_router.py`

- [ ] Map `F121-F124` packet claims to the current merged roster, pilot feedback, casepack, and evidence-refresh code/docs.
- [ ] Rerun the grouped validation-ops tests and inspect docs/artifacts for stale or contradictory claims.
- [ ] If an issue is real, fix the bounded backend/data/docs slice only after a failing proof exists where possible.

### Task 5: Publish the audit outcome

**Files:**
- Create: `docs/superpowers/pr-notes/2026-04-28-session-b-future-backlog-regression-audit.md`
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/daily/2026-04-28.md`

- [ ] Write a PR note summarizing reviewed units, commands run, concrete findings, and residual risks, with at least one Mermaid diagram.
- [ ] If no defects were found, state that explicitly and list any remaining watchouts instead of padding with generic reassurance.
- [ ] If defects were fixed, record the exact bounded files changed and the validation evidence.
- [ ] Update `ACTIVE_ASSIGNMENTS.md` and the daily log with the final audit state before opening the Draft PR.
