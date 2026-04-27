# F115 Runtime Policy Audit Trace Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expose a bounded, inspectable runtime-policy audit trace for current or historical Agent Spec snapshots without changing teacher-facing UX.

**Architecture:** Add a runtime-policy audit assembly helper, expose a small read endpoint near Agent Specs, and prove both latest-pack and historical-version audit behavior with focused tests.

**Tech Stack:** FastAPI, runtime-policy compiler/service helpers, Agent Spec service, pytest

---

### Task 1: Add The F115 Task Contract

**Files:**
- Create: `docs/superpowers/tasks/2026-04-27-f115-runtime-policy-audit-trace.md`
- Create: `docs/superpowers/specs/2026-04-27-f115-runtime-policy-audit-trace-design.md`
- Create: `docs/superpowers/plans/2026-04-27-f115-runtime-policy-audit-trace.md`

- [ ] **Step 1: Write the task packet**
- [ ] **Step 2: Write the design doc**
- [ ] **Step 3: Write the implementation plan**
- [ ] **Step 4: Commit the planning artifacts**

### Task 2: Add A Bounded Audit Assembly Helper

**Files:**
- Modify: `deeptutor/services/runtime_policy/compiler.py`
- Modify: `tests/services/runtime_policy/test_compiler.py`

- [ ] **Step 1: Write the failing runtime-policy audit tests**

Add tests proving:
- an audit helper can return the existing runtime-policy payload for a chosen `agent_spec_id`
- a requested historical version returns the pinned snapshot instead of the latest pack

- [ ] **Step 2: Run the targeted runtime-policy tests**

Run: `pytest tests/services/runtime_policy/test_compiler.py -k "audit or pinned_version" -q`

Expected: FAIL until the audit helper exists.

- [ ] **Step 3: Implement the audit helper**

Prefer a helper that builds a minimal `UnifiedContext` from explicit inputs and returns `RuntimePolicy.to_dict()` plus top-level metadata needed by the API route.

- [ ] **Step 4: Re-run the targeted runtime-policy tests**

Run: `pytest tests/services/runtime_policy/test_compiler.py -k "audit or pinned_version" -q`

Expected: PASS.

### Task 3: Expose The Audit Route

**Files:**
- Modify: `deeptutor/api/routers/agent_specs.py`
- Add or modify: relevant API tests

- [ ] **Step 1: Write the failing API tests**

Add tests for:
- latest runtime-policy audit by `agent_id`
- historical runtime-policy audit by `agent_id` + `version`
- 404 when the Agent Spec or version is missing

- [ ] **Step 2: Run the targeted API tests**

Run: `pytest tests/api -k "runtime_policy_audit or agent_spec_audit" -q`

Expected: FAIL until the route exists.

- [ ] **Step 3: Implement the bounded route**

Add a small GET endpoint that delegates to the runtime-policy audit helper and returns a stable JSON envelope.

- [ ] **Step 4: Re-run the targeted API tests**

Run: `pytest tests/api -k "runtime_policy_audit or agent_spec_audit" -q`

Expected: PASS.

### Task 4: Final Validation And PR Note

**Files:**
- Create: `docs/superpowers/pr-notes/2026-04-27-f115-runtime-policy-audit-trace.md`
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/TASK_REGISTRY.json`
- Modify: `ai_first/daily/2026-04-27.md` or `2026-04-26.md` depending on execution date

- [ ] **Step 1: Write the PR note**

Include one Mermaid diagram showing `Agent Spec -> audit helper -> API audit route`.

- [ ] **Step 2: Run the bounded suite**

Run the exact focused tests added for compiler and API behavior.

- [ ] **Step 3: Run diff hygiene**

Run: `git diff --check`

- [ ] **Step 4: Commit the implementation**

Use commit messages tagged with `[F115]`.
