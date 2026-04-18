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

- Current branch for this docs update: `docs/execution-queue-status-board`
- Milestone 0 status: merged into `main` via PR #1 on 2026-04-13
- PR `#4 docs: add first feature pod task packets` merged into `main` on 2026-04-18.
- Product MVP path status: Knowledge Pack, Assessment Builder, Student Tutor context, Teacher Dashboard, contest evidence screenshots, and runtime/backend/frontend/docs CI are merged.
- Current purpose: use a compact execution queue/status board under `ai_first/` so humans and AI workers can inspect latest merges, active queue, and next work from one short document.
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

- Current open task packet: `docs/superpowers/tasks/2026-04-19-execution-queue-status-board.md`
- Current open GitHub issue: `#19`
- Recently completed merged work: Knowledge Pack (`#6`), Assessment + Student Tutor (`#8`), Teacher Dashboard (`#11`), contest evidence (`#13`, `#14`, `#15`), and CI (`#17`, `#18`)
- Autonomous loop design: `docs/superpowers/specs/2026-04-18-autonomous-ai-loop-design.md`
- Autonomous loop roadmap: `ai_first/AI_FIRST_ROADMAP.md`

## Current Next Task

Use `ai_first/EXECUTION_QUEUE.md` as the shortest read path before choosing the next feature or workflow packet. If the active queue becomes empty after issue `#19` is closed, create or update the next task packet before implementation starts.

## Autonomous Merge Policy

- Docs, task, and workflow PRs may be auto-merged when mergeable, non-draft, and not blocked by review.
- Runtime and product PRs require passing relevant tests or checks and no blocking review before auto-merge.
- CI failures, merge conflicts, and blocking reviews become the next task until fixed or explicitly deferred.

## Mirror Policy

Use this file only as a compact status mirror. Do not rely on it for the full operating contract. For a human-friendly quick start, read `ai_first/USAGE_GUIDE.md`.
