# Current State

Last updated: 2026-04-25

This file is a compatibility snapshot. The authoritative operating instructions live in `ai_first/AI_OPERATING_PROMPT.md`.

## Repository

- GitHub: `Creative-Science-Contest-2026/Multiagent-learning-platform`
- Base project: HKUDS/DeepTutor
- License: Apache 2.0
- Main branch policy: use PRs, do not push directly to `main`

## Product Goal

Build a stable contest MVP:

Teacher creates Knowledge Pack -> AI generates assessment -> Student learns with Tutor Agent -> Teacher sees dashboard.

## Operating Model

- Hybrid AI-first OS is approved.
- Markdown in repo is long-term source of truth.
- GitHub Issues and PRs coordinate active execution.
- The AI operating prompt is the single entry point for new workers.
- `ai_first/AI_FIRST_ROADMAP.md` explains the autonomous loop and future operating direction for humans checking progress.
- Two collaborators may work in parallel through one active task, one branch, and one PR per person, coordinated by `ai_first/ACTIVE_ASSIGNMENTS.md`.

## Active Branches and PRs

- Latest merged docs/control-plane PR: `#127 docs: sync control plane after lane rollout`
- Current branch for this sync: `docs/demo-readiness-refresh`
- Product MVP path status: Knowledge Pack, assessment, tutor, dashboard, marketplace, offline, analytics, contest evidence, submission docs, optional video runbook, two-person collaboration workflow, and the full two-lane contest MVP polish experiment are merged to `main`.
- Current purpose: keep smoke-backed evidence current after `T044` through `T051` merged and record screenshot freshness honestly.
- Historical note: preserve `ai_first/2026-04-12-deeptutor-slimming/` as background analysis, not as the operating contract.

## Active Design

- Latest completed spec: `docs/superpowers/specs/2026-04-25-two-lane-contest-mvp-polish-design.md`
- Latest completed rollout plan: `docs/superpowers/plans/2026-04-25-two-lane-contest-mvp-polish-rollout.md`

## Known Worktree Notes

Before this operating system work, the repository had existing local changes:

- `docs/package-lock.json` and `web/package-lock.json` were dirty in the parent checkout before AI-first OS execution.
- Historical analysis files exist in the parent checkout under `ai_first/2026-04-12-deeptutor-slimming/`; preserve them when merging the AI-first OS branch back.
- In the isolated worktree, bootstrap files are being created incrementally from the approved plan.

Do not revert unrelated changes.

## Near-term Milestones

1. Milestone 1: Competition demo narrative.
2. Milestone 2: Teacher Knowledge Pack MVP.
3. Milestone 3: Assessment Builder MVP.
4. Milestone 4: Student Tutor Workspace MVP.
5. Milestone 5: Teacher Dashboard MVP.

## Active Execution

- Current open task packet: `docs/superpowers/tasks/2026-04-24-T036-contest-evidence-refresh.md`
- Current open GitHub issue:
- Latest completed smoke run result: the 2026-04-25 scripted-reset smoke pass succeeded with backend online through the CLI server path, frontend build passed after `npm ci`, Knowledge Pack demo data present, assessment/tutor session evidence present, and dashboard activity available.
- Recently completed merged work: `T044`, `T045`, `T046`, `T049`, `T050`, `T051`, and the post-lane control-plane sync are all merged to `main`; the current branch is refreshing evidence freshness rather than adding new product behavior.
- Autonomous loop design: `docs/superpowers/specs/2026-04-18-autonomous-ai-loop-design.md`
- Autonomous loop roadmap: `ai_first/AI_FIRST_ROADMAP.md`

## Current Next Task

Finish the smoke/evidence refresh lane, then refresh the stale screenshot bundle or carry that gap as an explicit human follow-up.

## Autonomous Merge Policy

- Docs, task, and workflow PRs may be auto-merged when mergeable, non-draft, and not blocked by review.
- Runtime and product PRs require passing relevant tests or checks and no blocking review before auto-merge.
- CI failures, merge conflicts, and blocking reviews become the next task until fixed or explicitly deferred.

## Mirror Policy

Use this file only as a compact status mirror. Do not rely on it for the full operating contract. For a human-friendly quick start, read `ai_first/USAGE_GUIDE.md`.
