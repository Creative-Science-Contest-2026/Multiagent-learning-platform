# F114 Spec Version Pinning Per Session Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Persist and reuse an exact Agent Spec version pin per session so runtime policy remains reproducible across turns after teachers edit the current pack.

**Architecture:** Introduce a bounded Agent Spec version-fetch API, store a session-level `agent_spec_pin`, and teach runtime policy/session runtime to create or reuse that pin without changing teacher-facing UX. The first turn using `agent_spec_id` writes the pin; later turns resolve the pinned snapshot instead of the latest pack.

**Tech Stack:** AgentSpec service, SQLite session preferences JSON, runtime-policy compiler, unified-turn runtime, pytest

---

### Task 1: Add The F114 Task Contract

**Files:**
- Create: `docs/superpowers/tasks/2026-04-27-f114-spec-version-pinning-per-session.md`
- Create: `docs/superpowers/specs/2026-04-27-f114-spec-version-pinning-per-session-design.md`
- Create: `docs/superpowers/plans/2026-04-27-f114-spec-version-pinning-per-session.md`

- [ ] **Step 1: Write the task packet**

Create the packet with owned files under `deeptutor/services/agent_spec/`, `deeptutor/services/session/`, and `deeptutor/services/runtime_policy/`, plus an explicit do-not-touch boundary for teacher-facing dashboard files.

- [ ] **Step 2: Write the design doc**

Record the session pin model, first-turn pinning rule, version-fetch service API, and runtime metadata expectations.

- [ ] **Step 3: Write the implementation plan**

Save this plan file before any production edits.

- [ ] **Step 4: Commit the planning artifacts**

```bash
git add docs/superpowers/tasks/2026-04-27-f114-spec-version-pinning-per-session.md docs/superpowers/specs/2026-04-27-f114-spec-version-pinning-per-session-design.md docs/superpowers/plans/2026-04-27-f114-spec-version-pinning-per-session.md
git commit -m "docs(runtime): define F114 session pinning plan [F114]"
```

### Task 2: Add Version Snapshot Fetching To Agent Spec Service

**Files:**
- Modify: `deeptutor/services/agent_spec/service.py`
- Modify: `tests/services/agent_spec/test_service.py`

- [ ] **Step 1: Write the failing service test**

Add a test proving a saved version snapshot can be loaded after the current pack has advanced:

```python
def test_get_pack_version_reads_historical_snapshot(tmp_path) -> None:
    service = AgentSpecService(tmp_path / "agent_specs")
    service.create_pack(agent_id="fraction-coach", display_name="Fraction Coach")
    service.save_pack(
        agent_id="fraction-coach",
        display_name="Fraction Coach",
        files={"WORKFLOW.md": "# Workflow\n\nVersion two"},
    )

    version_one = service.get_pack_version("fraction-coach", 1)
    version_two = service.get_pack_version("fraction-coach", 2)

    assert "Version two" not in version_one["files"]["WORKFLOW.md"]
    assert "Version two" in version_two["files"]["WORKFLOW.md"]
```

- [ ] **Step 2: Run the targeted test to confirm failure**

Run: `pytest tests/services/agent_spec/test_service.py -k historical_snapshot -q`

Expected: FAIL because the version-fetch API does not exist yet.

- [ ] **Step 3: Add the version-fetch helper**

Implement a dedicated helper in `service.py` that reads `versions/vNNNN/metadata.json` and versioned markdown files.

- [ ] **Step 4: Re-run the targeted service test**

Run: `pytest tests/services/agent_spec/test_service.py -k historical_snapshot -q`

Expected: PASS.

### Task 3: Persist Session-Level Agent Spec Pins

**Files:**
- Modify: `deeptutor/services/session/sqlite_store.py`
- Modify: `tests/services/session/test_sqlite_store.py`

- [ ] **Step 1: Write the failing session-store test**

Add a test proving session preferences can store and later return an `agent_spec_pin`.

- [ ] **Step 2: Run the targeted session-store test**

Run: `pytest tests/services/session/test_sqlite_store.py -k agent_spec_pin -q`

Expected: FAIL until the helper path is explicit in tests or implementation.

- [ ] **Step 3: Add bounded helpers if needed**

Prefer using the existing session preferences JSON update path. Add a tiny helper only if it makes pin read/write clearer and testable.

- [ ] **Step 4: Re-run the targeted session-store test**

Run: `pytest tests/services/session/test_sqlite_store.py -k agent_spec_pin -q`

Expected: PASS.

### Task 4: Reuse Pinned Versions In Runtime Policy

**Files:**
- Modify: `deeptutor/services/runtime_policy/compiler.py`
- Modify: `tests/services/runtime_policy/test_compiler.py`

- [ ] **Step 1: Write the failing runtime-policy test**

Prove that a session pin forces runtime policy to use a historical snapshot even when the current pack has changed.

- [ ] **Step 2: Run the targeted runtime-policy test**

Run: `pytest tests/services/runtime_policy/test_compiler.py -k pinned_version -q`

Expected: FAIL because runtime policy still resolves the latest pack only.

- [ ] **Step 3: Teach runtime policy to prefer the session pin**

Read `agent_spec_pin` from session-scoped metadata/preferences, resolve the pinned version via the Agent Spec service helper, and expose the pinned version in runtime debug metadata.

- [ ] **Step 4: Re-run the targeted runtime-policy test**

Run: `pytest tests/services/runtime_policy/test_compiler.py -k pinned_version -q`

Expected: PASS.

### Task 5: Create And Reuse Pins In Unified Turn Runtime

**Files:**
- Modify: `deeptutor/services/session/turn_runtime.py`
- Modify: `tests/api/test_unified_ws_turn_runtime.py`

- [ ] **Step 1: Write the failing unified-turn tests**

Add one test for first-turn pin creation and one for later-turn reuse after the current pack changes.

- [ ] **Step 2: Run the targeted unified-turn tests**

Run: `pytest tests/api/test_unified_ws_turn_runtime.py -k \"agent_spec_pin or pinned_version\" -q`

Expected: FAIL because the turn runtime does not yet persist or reload the pin.

- [ ] **Step 3: Add bounded pin create/reuse logic**

Persist the pin when a turn first resolves `agent_spec_id`, then inject it into later turns through the existing session/runtime context path.

- [ ] **Step 4: Re-run the targeted unified-turn tests**

Run: `pytest tests/api/test_unified_ws_turn_runtime.py -k \"agent_spec_pin or pinned_version\" -q`

Expected: PASS.

### Task 6: Final Validation And PR Note

**Files:**
- Create: `docs/superpowers/pr-notes/2026-04-27-f114-spec-version-pinning-per-session.md`
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/TASK_REGISTRY.json`
- Modify: `ai_first/daily/2026-04-27.md` or `2026-04-26.md` depending on execution date

- [ ] **Step 1: Write the PR note**

Include one Mermaid diagram showing `agent_spec_id -> first turn pin -> later turn reuse`.

- [ ] **Step 2: Run the bounded suite**

Run: `pytest tests/services/agent_spec/test_service.py tests/services/session/test_sqlite_store.py tests/services/runtime_policy/test_compiler.py tests/api/test_unified_ws_turn_runtime.py -q`

Expected: PASS.

- [ ] **Step 3: Run diff hygiene**

Run: `git diff --check`

Expected: exit `0`.

- [ ] **Step 4: Commit the implementation**

```bash
git add deeptutor/services/agent_spec/service.py deeptutor/services/session/sqlite_store.py deeptutor/services/runtime_policy/compiler.py deeptutor/services/session/turn_runtime.py tests/services/agent_spec/test_service.py tests/services/session/test_sqlite_store.py tests/services/runtime_policy/test_compiler.py tests/api/test_unified_ws_turn_runtime.py docs/superpowers/pr-notes/2026-04-27-f114-spec-version-pinning-per-session.md ai_first/ACTIVE_ASSIGNMENTS.md ai_first/TASK_REGISTRY.json ai_first/daily/2026-04-27.md
git commit -m "feat(runtime): pin spec versions per session [F114]"
```
