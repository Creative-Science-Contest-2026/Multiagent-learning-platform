# Current State

Last updated: 2026-04-19

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
- Two Feature Pods may work in parallel after shared operating files land.

## Active Branches and PRs

- Current branch for this docs update: `docs/post-pr4-next-actions`
- Milestone 0 status: merged into `main` via PR #1 on 2026-04-13
- PR `#4 docs: add first feature pod task packets` merged into `main` on 2026-04-18.
- Current purpose: update the queue after PR `#4`, then continue with Pod A before Pod B.
- Historical note: preserve `ai_first/2026-04-12-deeptutor-slimming/` as background analysis, not as the operating contract.

## Active Design

- Spec: `docs/superpowers/specs/2026-04-12-ai-first-project-os-design.md`
- Plan: `docs/superpowers/plans/2026-04-12-ai-first-project-os.md`

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

- Pod A task packet: `docs/superpowers/tasks/2026-04-13-teacher-knowledge-pack-pod-a.md`
- Pod B task packet: `docs/superpowers/tasks/2026-04-13-assessment-student-workspace-pod-b.md`
- Pod A GitHub issue: `#2`
- Pod B GitHub issue: `#3`
- Autonomous loop design: `docs/superpowers/specs/2026-04-18-autonomous-ai-loop-design.md`
- Autonomous loop roadmap: `ai_first/AI_FIRST_ROADMAP.md`

## Current Next Task

Audit the existing `pod-a/teacher-knowledge-pack-mvp` worktree before continuing implementation. It contains uncommitted changes in both Pod A-owned files and Pod B-owned/do-not-touch files, so the next AI worker must separate scope before committing or editing.

## Autonomous Merge Policy

- Docs, task, and workflow PRs may be auto-merged when mergeable, non-draft, and not blocked by review.
- Runtime and product PRs require passing relevant tests or checks and no blocking review before auto-merge.
- CI failures, merge conflicts, and blocking reviews become the next task until fixed or explicitly deferred.

## Mirror Policy

Use this file only as a compact status mirror. Do not rely on it for the full operating contract. For a human-friendly quick start, read `ai_first/USAGE_GUIDE.md`.
