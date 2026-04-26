# F113 Capability-Wide Runtime Binding Coverage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend bounded runtime-binding proof from the unified `chat` path to the shipped `deep_question` and `deep_solve` turn paths without broadening into teacher-facing UX or universal capability claims.

**Architecture:** Keep `agent_spec_id` as an explicit public request-contract field on covered capabilities, propagate it through `TurnRuntimeManager` via `UnifiedContext.config_overrides`, and make each covered capability compile and consume runtime policy in a capability-appropriate way. Preserve existing `chat` behavior, keep `deep_question` on the assessment-policy path, and add the smallest bounded runtime-policy injection to `deep_solve`.

**Tech Stack:** Pydantic request contracts, unified capability runtime, runtime-policy compiler/helpers, pytest

---

### Task 1: Widen Covered Capability Request Contracts

**Files:**
- Modify: `deeptutor/capabilities/request_contracts.py`
- Test: `tests/core/test_capabilities_runtime.py`

- [ ] **Step 1: Write the failing request-contract tests**

Add focused tests proving `deep_question` and `deep_solve` accept `agent_spec_id` while still rejecting unknown fields.

- [ ] **Step 2: Run the targeted tests to confirm failure**

Run: `pytest tests/core/test_capabilities_runtime.py -k "accepts_agent_spec_id or rejects_unknown_fields" -q`

Expected: FAIL because `deep_question` and `deep_solve` configs do not yet expose `agent_spec_id`.

- [ ] **Step 3: Add `agent_spec_id` to covered request models**

Update `deeptutor/capabilities/request_contracts.py` so `DeepQuestionRequestConfig` and `DeepSolveRequestConfig` both define `agent_spec_id: str = ""`.

- [ ] **Step 4: Re-run the targeted tests**

Run: `pytest tests/core/test_capabilities_runtime.py -k "accepts_agent_spec_id or rejects_unknown_fields" -q`

Expected: PASS.

- [ ] **Step 5: Commit the request-contract slice**

```bash
git add deeptutor/capabilities/request_contracts.py tests/core/test_capabilities_runtime.py
git commit -m "feat(runtime): widen covered capability request contracts [F113]"
```

### Task 2: Prove Runtime Binding For `deep_question`

**Files:**
- Modify: `tests/core/test_capabilities_runtime.py`
- Modify: `tests/api/test_unified_ws_turn_runtime.py`

- [ ] **Step 1: Write the failing capability-level `deep_question` binding test**

Prove `DeepQuestionCapability` resolves runtime policy from an Agent Spec pack and injects `Teacher Assessment Runtime Policy:` into generation input.

- [ ] **Step 2: Write the failing unified-turn `deep_question` propagation test**

Prove `TurnRuntimeManager` accepts `config.agent_spec_id` on a `deep_question` turn and the capability consumes the bound policy.

- [ ] **Step 3: Run the targeted `deep_question` tests**

Run: `pytest tests/core/test_capabilities_runtime.py -k "deep_question and runtime_policy" -q`

Run: `pytest tests/api/test_unified_ws_turn_runtime.py -k "deep_question_policy_binding" -q`

Expected: FAIL until the proof is wired and assertions match the real path.

- [ ] **Step 4: Keep production changes minimal**

If the widened request contract is sufficient, keep `deep_question` production code unchanged and only land tests. If a small bounded fix is required, keep it inside existing runtime-policy assembly.

- [ ] **Step 5: Re-run the targeted `deep_question` proof tests**

Run: `pytest tests/core/test_capabilities_runtime.py -k "deep_question and runtime_policy" -q`

Run: `pytest tests/api/test_unified_ws_turn_runtime.py -k "deep_question_policy_binding" -q`

Expected: PASS.

- [ ] **Step 6: Commit the `deep_question` proof slice**

```bash
git add tests/core/test_capabilities_runtime.py tests/api/test_unified_ws_turn_runtime.py
git commit -m "test(runtime): prove deep-question policy binding [F113]"
```

### Task 3: Add Bounded Runtime Policy Injection To `deep_solve`

**Files:**
- Modify: `deeptutor/capabilities/deep_solve.py`
- Modify: `deeptutor/services/runtime_policy/compiler.py` only if a shared formatter/helper is required
- Modify: `tests/core/test_capabilities_runtime.py`

- [ ] **Step 1: Write the failing capability-level `deep_solve` binding test**

Prove `DeepSolveCapability` compiles runtime policy and passes a bounded policy block into solver execution.

- [ ] **Step 2: Run the targeted `deep_solve` test to confirm failure**

Run: `pytest tests/core/test_capabilities_runtime.py -k "deep_solve and runtime_policy" -q`

Expected: FAIL because `deep_solve` does not yet inject runtime policy.

- [ ] **Step 3: Add the minimal policy assembly path to `deep_solve`**

Compile runtime policy, emit one runtime-policy progress event, prepend the policy block to `conversation_context`, and pass that merged context into `solver.solve(...)`.

- [ ] **Step 4: Add a shared formatter only if the existing chat formatter is the wrong fit**

Prefer reusing `format_chat_system_context(policy)` unless tests show it is semantically unsuitable.

- [ ] **Step 5: Re-run the targeted `deep_solve` tests**

Run: `pytest tests/core/test_capabilities_runtime.py -k "deep_solve and runtime_policy" -q`

Run: `pytest tests/services/runtime_policy/test_compiler.py -q`

Expected: PASS.

- [ ] **Step 6: Commit the `deep_solve` runtime-policy slice**

```bash
git add deeptutor/capabilities/deep_solve.py deeptutor/services/runtime_policy/compiler.py tests/core/test_capabilities_runtime.py
git commit -m "feat(runtime): bind deep-solve to teacher policy [F113]"
```

### Task 4: Prove Unified Turn Propagation For `deep_solve`

**Files:**
- Modify: `tests/api/test_unified_ws_turn_runtime.py`
- Modify: `deeptutor/services/session/turn_runtime.py` only if bounded propagation fixes are required

- [ ] **Step 1: Write the failing unified-turn `deep_solve` propagation test**

Prove a `deep_solve` turn with `config.agent_spec_id` reaches capability execution and carries runtime policy into solver context.

- [ ] **Step 2: Run the targeted unified-turn test**

Run: `pytest tests/api/test_unified_ws_turn_runtime.py -k "deep_solve_policy_binding" -q`

Expected: FAIL until the capability path is wired.

- [ ] **Step 3: Make only bounded propagation fixes if the test exposes a real gap**

Keep any runtime fix local to `deeptutor/services/session/turn_runtime.py` and avoid adding a second metadata-only path for `agent_spec_id`.

- [ ] **Step 4: Re-run the targeted `deep_solve` propagation test**

Run: `pytest tests/api/test_unified_ws_turn_runtime.py -k "deep_solve_policy_binding" -q`

Expected: PASS.

- [ ] **Step 5: Commit the unified-turn proof slice**

```bash
git add deeptutor/services/session/turn_runtime.py tests/api/test_unified_ws_turn_runtime.py
git commit -m "test(runtime): prove deep-solve turn binding [F113]"
```

### Task 5: Run The Full Bounded Validation Matrix

**Files:**
- Modify: `tests/core/test_capabilities_runtime.py` only if cleanup or deduplication is still needed
- Modify: `tests/api/test_unified_ws_turn_runtime.py` only if cleanup or deduplication is still needed

- [ ] **Step 1: Clean up duplicate or confusing runtime tests**

Collapse any duplicate test definitions so each behavior has one authoritative test.

- [ ] **Step 2: Run the bounded runtime-policy suite**

Run: `pytest tests/core/test_capabilities_runtime.py tests/api/test_unified_ws_turn_runtime.py tests/services/runtime_policy/test_compiler.py -q`

Expected: PASS.

- [ ] **Step 3: Run diff hygiene**

Run: `git diff --check`

Expected: exit `0`.

- [ ] **Step 4: Commit any final test cleanup**

```bash
git add tests/core/test_capabilities_runtime.py tests/api/test_unified_ws_turn_runtime.py
git commit -m "test(runtime): stabilize capability binding coverage [F113]"
```

### Task 6: Record Scope-Bounded Docs And AI-First State

**Files:**
- Create: `docs/superpowers/pr-notes/2026-04-26-f113-capability-wide-runtime-binding-coverage.md`
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/TASK_REGISTRY.json`
- Modify: `ai_first/daily/2026-04-26.md`
- Modify: `docs/contest/README.md` or `docs/contest/VALIDATION_REPORT.md` only if the proof scope actually widens

- [ ] **Step 1: Create the runtime-binding PR note with an exact coverage diagram**

Include one Mermaid diagram showing `TurnRuntimeManager -> config_overrides -> chat/deep_question/deep_solve -> runtime policy compiled`.

- [ ] **Step 2: Record the active assignment and task status**

Mark `F113_CAPABILITY_WIDE_RUNTIME_BINDING_COVERAGE` as `in-progress` when work begins and move the assignment to review-ready state when validation is done.

- [ ] **Step 3: Append a daily log entry with test evidence**

Capture branch/worktree, covered capabilities, validation commands, and whether contest-facing claim wording changed.

- [ ] **Step 4: Update contest-facing docs only if the proof scope actually widened**

If claim wording changes, keep it exact: `chat`, `deep_question`, and `deep_solve` only.

- [ ] **Step 5: Run the final scoped validation commands**

Run: `pytest tests/core/test_capabilities_runtime.py tests/api/test_unified_ws_turn_runtime.py tests/services/runtime_policy/test_compiler.py -q`

Run: `git diff --check`

Expected: both pass.

- [ ] **Step 6: Commit the docs/state slice**

```bash
git add docs/superpowers/pr-notes/2026-04-26-f113-capability-wide-runtime-binding-coverage.md ai_first/ACTIVE_ASSIGNMENTS.md ai_first/TASK_REGISTRY.json ai_first/daily/2026-04-26.md docs/contest/README.md docs/contest/VALIDATION_REPORT.md
git commit -m "docs(runtime): record bounded binding coverage [F113]"
```
