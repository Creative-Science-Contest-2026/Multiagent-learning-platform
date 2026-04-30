# Realistic Demo Seed Data Design

Date: 2026-04-30
Task packet: `docs/superpowers/tasks/2026-04-30-demo-realistic-seed-data.md`
Branch: `fix/demo-realistic-seed-data`

## Objective

Upgrade the existing local demo reset flow so one command can populate believable, varied, demo-safe data across the teacher-first contest journey without requiring live services or manual DB edits.

## Scope

In scope:

- expand the local contest reset utility
- write richer knowledge-pack metadata under `data/knowledge_bases/`
- seed SQLite session and evidence records under `data/user/chat_history.db`
- document the final reset and verification flow

Out of scope:

- frontend code changes
- API/router changes
- dependency changes
- committing generated `data/` outputs

## Current behavior

The current reset utility creates one knowledge pack and two sessions:

- one assessment demo session
- one tutor demo session

That is enough for a smoke baseline but not enough to support a polished product video. Marketplace listing, dashboard cards, grouped recommendations, intervention history, and replay variety remain too thin or empty.

## Intended behavior

The reset utility should create a cohesive classroom storyline:

- one teacher owns a classroom with multiple students
- several shareable knowledge packs exist with realistic metadata diversity
- a subset of packs is imported into the local workspace
- students have multiple assessment attempts with mixed performance
- tutor sessions reflect follow-up support after assessment findings
- dashboard evidence surfaces show both student-level and group-level intervention decisions

## Candidate approaches

### Approach 1: Extend the existing reset utility

Use the current `scripts/contest/reset_demo_data.py` entry point and factor it into bounded helpers for:

- marketplace/shareable pack metadata
- imported/local knowledge packs
- seeded assessment sessions
- seeded tutor sessions
- seeded observations and student states
- seeded teacher evidence actions and feedback

Pros:

- keeps one known-safe command
- matches the existing contest runbook
- minimizes operator confusion

Cons:

- script complexity increases and needs structure

### Approach 2: Add a parallel video-only seed command

Keep the old reset script untouched and add a new command dedicated to rich demo data.

Pros:

- avoids changing the current script behavior

Cons:

- duplicates safety and storage logic
- creates two competing demo reset paths
- higher maintenance drift risk

## Chosen approach

Choose Approach 1. The richer dataset is still the same demo reset concern, so it belongs in the existing utility rather than a separate parallel script.

## Data model and content design

### Marketplace and knowledge packs

Seed 6 to 10 demo-safe knowledge packs with varied metadata fields the marketplace already reads:

- name and short description
- subject, grade, curriculum
- learning objectives
- owner and sharing status
- updated timestamps
- review and rating summary fields when supported by metadata
- popularity/import-count style fields when supported by metadata

The set should include one flagship algebra pack plus adjacent packs so search and sorting feel real:

- quadratic equations
- factoring foundations
- linear systems review
- geometry proof starters
- statistics and charts
- STEM microscope observation writing

### Assessment sessions

Seed 8 to 12 assessment sessions across multiple students in one classroom cohort:

- varying scores
- multiple topics
- repeated misconceptions for some students
- improving trend for some students
- fresh low-score attempts for recommendation triggering

Each session should include:

- a teacher-readable title
- preferences with capability and knowledge-pack linkage
- user and assistant messages
- turn record and timestamps
- assessment payloads/events required by the current review and dashboard readers

### Tutor replay sessions

Seed 3 to 5 tutor sessions linked to the same classroom story:

- one remediation-focused session
- one confidence-building session
- one follow-up after intervention
- optional one advanced student extension session

These should contain longer, natural transcripts so replay pages look believable instead of stubbed.

### Dashboard evidence and intervention traces

Seed the evidence tables the dashboard already aggregates:

- `observations`
- `student_states`
- teacher actions
- recommendation acknowledgements
- recommendation feedback
- teacher overrides
- diagnosis feedback
- intervention assignments

The data should intentionally create:

- at least one student with repeated factoring mistakes
- at least one student with sign-error misconceptions
- at least one small group sharing the same weak topic
- at least one recommendation that has been acknowledged but not acted on
- at least one intervention assignment in progress
- at least one closed-loop history chain for the video

## Implementation structure

Refactor the reset utility into bounded helpers:

- `_seed_marketplace_packs`
- `_seed_workspace_knowledge_packs`
- `_seed_assessment_sessions`
- `_seed_tutor_sessions`
- `_seed_observations_and_student_states`
- `_seed_teacher_evidence`
- `_clear_existing_demo_records`

The exact helper names can vary, but the structure should separate metadata seeding from session/evidence seeding.

## Safety and idempotency

The command must:

- keep the existing local API base safety gate
- only touch known demo ids or clearly demo-tagged records
- delete and recreate only demo-safe rows owned by this script
- avoid touching unrelated user data
- produce the same final dataset shape on repeated runs

## Validation

Minimum validation after implementation:

- script test suite passes
- one local run of the reset command succeeds
- a second run leaves counts stable
- direct DB inspection confirms the seeded tables and ids exist
- main contest-path reads are non-empty for marketplace, dashboard, assessment review, and tutor replay

## Risks and controls

- Risk: over-seeding fields the UI does not read.
  Control: align seeded metadata with existing router/test expectations.

- Risk: polluting unrelated local sessions.
  Control: reserve a `contest-` or other explicit demo id namespace and clean only within that namespace.

- Risk: making the dataset look synthetic.
  Control: vary timestamps, student outcomes, teacher notes, and intervention status.

## Approval checkpoint

After this spec is approved, implementation can proceed in the dedicated worktree and branch with changes limited to the task packet scope.
