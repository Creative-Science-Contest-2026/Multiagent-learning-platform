# Realistic Demo Seed Data Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the local demo reset utility so one command seeds realistic, diverse, demo-safe data across marketplace, imported packs, assessment review, tutor replay, and dashboard evidence.

**Architecture:** Keep the existing `scripts.contest.reset_demo_data` entry point and extend it with bounded helpers that seed only local demo-safe knowledge-pack metadata plus SQLite-backed session/evidence rows. Use script-level TDD first, then implement the minimum helper structure needed to satisfy the richer dataset and idempotency guarantees.

**Tech Stack:** Python, SQLite, pytest, local JSON metadata under `data/knowledge_bases/`, existing evidence helper modules

---

### Task 1: Lock the richer reset contract with failing tests

**Files:**
- Modify: `tests/scripts/test_reset_demo_data.py`
- Reference: `scripts/contest/reset_demo_data.py`

- [ ] **Step 1: Write the failing test expectations for the richer dataset**

Add assertions for:
- multiple public/team marketplace packs in `kb_config.json`
- at least one imported workspace pack ending with `__imported`
- multiple assessment/tutor sessions
- non-empty `observations` and `student_states`
- non-empty teacher evidence tables

- [ ] **Step 2: Run the script tests to verify RED**

Run: `rtk pytest tests/scripts/test_reset_demo_data.py -v`
Expected: FAIL because the current reset script only creates one pack, two sessions, and no richer evidence rows.

- [ ] **Step 3: Refine the test to avoid false positives**

Keep the expectations bounded to exact demo-safe ids and minimum counts so the test proves realistic breadth without over-coupling to incidental implementation details.

- [ ] **Step 4: Re-run the script tests**

Run: `rtk pytest tests/scripts/test_reset_demo_data.py -v`
Expected: FAIL for the same missing richer-seed reasons, but with the final intended assertions.

### Task 2: Implement richer knowledge-pack and session seeding

**Files:**
- Modify: `scripts/contest/reset_demo_data.py`
- Reference: `deeptutor/services/session/sqlite_store.py`
- Reference: `deeptutor/api/routers/marketplace.py`
- Reference: `deeptutor/services/session/assessment_review.py`

- [ ] **Step 1: Add bounded demo dataset constants and cleanup helpers**

Create explicit demo namespaces and helper lists for:
- shareable marketplace packs
- imported workspace packs
- assessment sessions
- tutor sessions
- student ids and cohort metadata

Also add cleanup helpers that delete only demo-owned records from the SQLite tables and knowledge-base config entries.

- [ ] **Step 2: Seed richer marketplace and workspace pack metadata**

Extend the script so it writes:
- 6 to 10 public/team demo packs with varied metadata and marketplace review summaries
- 2 to 3 imported/private workspace packs linked back to shareable sources
- raw document placeholders for preview/document counts where needed

- [ ] **Step 3: Seed assessment and tutor sessions using the current session contract**

Seed:
- 8 to 12 assessment sessions with `[Quiz Performance]` messages and linked knowledge bases
- 3 to 5 tutor sessions with natural-looking user/assistant transcript messages
- session preferences including `student_id`, `cohort`, `knowledge_bases`, `capability`, and `demo`

- [ ] **Step 4: Run script tests after the first implementation pass**

Run: `rtk pytest tests/scripts/test_reset_demo_data.py -v`
Expected: some failures may remain around evidence-table coverage or idempotency details, but the counts for packs/sessions should move toward the target.

### Task 3: Seed dashboard evidence and close idempotency gaps

**Files:**
- Modify: `scripts/contest/reset_demo_data.py`
- Reference: `deeptutor/services/evidence/teacher_actions.py`
- Reference: `deeptutor/services/evidence/recommendation_acks.py`
- Reference: `deeptutor/services/evidence/recommendation_feedback.py`
- Reference: `deeptutor/services/evidence/teacher_overrides.py`
- Reference: `deeptutor/services/evidence/diagnosis_feedback.py`
- Reference: `deeptutor/services/evidence/intervention_assignments.py`

- [ ] **Step 1: Seed observations and student-state rollups for the classroom story**

Populate observation rows with varied timestamps, topics, correctness, hint counts, retries, and dominant errors. Then write student-state rollups so dashboard reasoning surfaces have realistic support and misconception signals.

- [ ] **Step 2: Seed teacher evidence tables with believable workflow traces**

Create:
- recommendation acknowledgements
- recommendation feedback
- teacher overrides
- teacher actions
- intervention assignments
- diagnosis feedback

Cover both student-level and at least one small-group storyline.

- [ ] **Step 3: Run the script tests to verify GREEN**

Run: `rtk pytest tests/scripts/test_reset_demo_data.py -v`
Expected: PASS.

- [ ] **Step 4: Run the reset command twice against the worktree repo root**

Run: `rtk .venv/bin/python -m scripts.contest.reset_demo_data --project-root . --api-base http://localhost:8001`
Run again: `rtk .venv/bin/python -m scripts.contest.reset_demo_data --project-root . --api-base http://localhost:8001`
Expected: both runs succeed and report stable demo ids/paths without duplicate growth.

### Task 4: Update contest docs and record the lane

**Files:**
- Modify: `docs/contest/DEMO_DATA_RESET.md`
- Modify: `docs/contest/SMOKE_RUNBOOK.md`
- Modify: `ai_first/daily/2026-04-30.md`
- Create: `docs/superpowers/pr-notes/2026-04-30-demo-realistic-seed-data.md`

- [ ] **Step 1: Update the reset runbook**

Document the richer seeded dataset shape, including that the reset now prepares marketplace, multiple assessment/tutor sessions, and dashboard evidence for video capture.

- [ ] **Step 2: Update the smoke runbook only where the richer dataset matters**

Clarify that the reset primes a fuller teacher-first dataset before smoke and video capture, without changing the smoke sequence itself.

- [ ] **Step 3: Add the PR architecture note with Mermaid**

Create a short note describing the local-only data flow from reset script to knowledge-base metadata and SQLite evidence tables. State that `ai_first/architecture/MAIN_SYSTEM_MAP.md` was not changed because this is a local demo helper lane.

- [ ] **Step 4: Update the daily log**

Record the new richer reset utility scope, tests run, and any residual environment limitations.

### Task 5: Verify, commit, open PR, and merge if eligible

**Files:**
- Modify: tracked files from Tasks 1-4 only

- [ ] **Step 1: Run the required verification commands**

Run:
- `rtk pytest tests/scripts/test_reset_demo_data.py -v`
- `rtk rg -n "demo data|reset|seed|smoke|Knowledge Pack|contest|Mermaid" scripts tests docs/contest docs/superpowers/tasks docs/superpowers/pr-notes ai_first`
- `rtk python3 -m compileall scripts`
- `rtk git diff --check`

Expected: all commands succeed.

- [ ] **Step 2: Review the diff and commit with the required tag**

Commit format:
`feat(contest-demo): expand realistic local seed dataset [DEMO-SEED]`

- [ ] **Step 3: Push the lane branch and open a draft PR**

Push `fix/demo-realistic-seed-data`, create a draft PR, and include the PR note path plus validation summary in the description.

- [ ] **Step 4: Move PR to Ready and merge only if eligible**

Only merge if:
- local verification is complete
- PR is no longer draft
- required CI is green
- no blocking review exists

