# F116 Student Model Enrichment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enrich the student-state contract with additive mastery, support, and misconception signals while keeping the existing evidence-first behavior stable.

**Architecture:** Extend the student-state contract and rollup derivation in session/evidence layers, then prove the new signals through focused storage and diagnosis tests.

**Tech Stack:** SQLite session store, evidence contracts/diagnosis helpers, pytest

---

### Task 1: Add The F116 Task Contract

**Files:**
- Create: `docs/superpowers/tasks/2026-04-27-f116-student-model-enrichment.md`
- Create: `docs/superpowers/specs/2026-04-27-f116-student-model-enrichment-design.md`
- Create: `docs/superpowers/plans/2026-04-27-f116-student-model-enrichment.md`

- [ ] **Step 1: Write the task packet**
- [ ] **Step 2: Write the design doc**
- [ ] **Step 3: Write the implementation plan**
- [ ] **Step 4: Commit the planning artifacts**

### Task 2: Enrich The Student-State Contract

**Files:**
- Modify: `deeptutor/services/evidence/contracts.py`
- Modify: `tests/services/session/test_sqlite_store.py`

- [ ] **Step 1: Write failing storage/contract tests**

Add tests proving enriched student-state fields survive persistence and rollup generation.

- [ ] **Step 2: Run the targeted tests**

Run: `pytest tests/services/session/test_sqlite_store.py -k "student_state or rollup" -q`

Expected: FAIL until the richer shape is produced or persisted.

- [ ] **Step 3: Implement additive contract/storage support**

Keep existing top-level fields stable and add nested signal groups.

- [ ] **Step 4: Re-run the targeted storage tests**

Expected: PASS.

### Task 3: Derive Richer Signals From Observations

**Files:**
- Modify: `deeptutor/services/session/sqlite_store.py`
- Modify: `tests/services/session/test_sqlite_store.py`

- [ ] **Step 1: Write failing rollup-detail tests**

Prove the store can derive topic-level mastery/support/misconception signals from mixed recent observations.

- [ ] **Step 2: Run the targeted rollup tests**

- [ ] **Step 3: Implement bounded derivation logic**

Use explainable topic buckets and recent-support summaries rather than opaque scoring.

- [ ] **Step 4: Re-run the targeted rollup tests**

Expected: PASS.

### Task 4: Keep Diagnosis Compatible With The Enriched Model

**Files:**
- Modify: `deeptutor/services/evidence/diagnosis.py`
- Modify: `tests/services/evidence/test_diagnosis.py`

- [ ] **Step 1: Write failing diagnosis tests**

Add tests showing diagnosis payloads preserve or consume the enriched student-state shape without changing the observation-first policy.

- [ ] **Step 2: Run the targeted diagnosis tests**

Run: `pytest tests/services/evidence/test_diagnosis.py -q`

Expected: FAIL until the enriched model is handled cleanly.

- [ ] **Step 3: Implement bounded diagnosis compatibility**

Keep diagnosis scoring centered on observations and treat enriched state as context only.

- [ ] **Step 4: Re-run the targeted diagnosis tests**

Expected: PASS.

### Task 5: Final Validation And PR Note

**Files:**
- Create: `docs/superpowers/pr-notes/2026-04-27-f116-student-model-enrichment.md`
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/TASK_REGISTRY.json`
- Modify: `ai_first/daily/2026-04-27.md`
- Modify: `ai_first/architecture/MAIN_SYSTEM_MAP.md` if shared contract framing changes

- [ ] **Step 1: Write the PR note**

Include one Mermaid diagram showing observations -> student-state rollup -> diagnosis context.

- [ ] **Step 2: Run the bounded suite**

Run the focused session/evidence tests touched by the task.

- [ ] **Step 3: Run diff hygiene**

Run: `git diff --check`

- [ ] **Step 4: Commit the implementation**

Use commit messages tagged with `[F116]`.
