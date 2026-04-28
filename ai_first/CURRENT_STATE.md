# Current State

Last updated: 2026-04-28

This file is a compatibility snapshot. The authoritative operating instructions live in `ai_first/AI_OPERATING_PROMPT.md`.

## Repository

- GitHub: `Creative-Science-Contest-2026/Multiagent-learning-platform`
- Base project: HKUDS/DeepTutor
- License: Apache 2.0
- Main branch policy: use PRs, do not push directly to `main`

## Product Goal

Build a stable contest MVP:

Knowledge Pack -> Assessment -> Tutor -> Diagnosis -> Intervention.

## Operating Model

- Hybrid AI-first OS is approved.
- Markdown in repo is long-term source of truth.
- GitHub Issues and PRs coordinate active execution.
- The AI operating prompt is the single entry point for new workers.
- `ai_first/AI_FIRST_ROADMAP.md` explains the autonomous loop and future operating direction for humans checking progress.
- Two collaborators may work in parallel through one active task, one branch, and one PR per person, coordinated by `ai_first/ACTIVE_ASSIGNMENTS.md`.

## Active Branches and PRs

- Latest merged docs/control-plane PRs: `#210`, `#212`, and `#211` completed submission-close Phase 1 on 2026-04-28.
- Current branch for this lane: `docs/post-phase2-browser-recapture-run` (PR `#221`)
- Product MVP path status: the core contest flow, the Wave 1 evidence spine, the command-backed 2026-04-28 smoke refresh, and the optional Phase 2 polish train (`C212-C215`) are merged to `main` as a validated prototype; the active docs-only lane is refreshing the stale browser screenshot rows against that merged state.
- Current purpose: complete the post-Phase-2 browser recapture packet so the Knowledge, Tutor, Dashboard, and `/agents` screenshot rows can return to `Current`, then return the repo to final human review and optional video only.
- Historical note: preserve `ai_first/2026-04-12-deeptutor-slimming/` as background analysis, not as the operating contract.

## Active Design

- Latest completed spec: `docs/superpowers/specs/2026-04-28-three-session-submission-close-design.md`
- Latest completed rollout plan: `docs/superpowers/plans/2026-04-28-three-session-submission-close.md`

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

- Current open task packet: `docs/superpowers/tasks/2026-04-28-browser-recapture-after-phase2.md`
- Current open GitHub issue:
- Latest completed smoke run result: the 2026-04-28 scripted-reset smoke pass succeeded with backend online through the CLI server path, frontend build passed after `npm ci`, Knowledge Pack demo data present, assessment/tutor session evidence present, and dashboard activity available.
- Recently completed merged work: submission-close master coordination and package readiness merged through PRs `#210`, `#212`, and `#211`, followed by optional Phase 2 polish through PRs `#214`, `#215`, `#216`, and `#217`.
- Autonomous loop design: `docs/superpowers/specs/2026-04-18-autonomous-ai-loop-design.md`
- Autonomous loop roadmap: `ai_first/AI_FIRST_ROADMAP.md`

## Current Next Task

Keep docs-only PR `#221` green and merge it, then return the repo to human review of the submission package, IP commitment, optional video decision, and final sign-off.

## Autonomous Merge Policy

- Docs, task, and workflow PRs may be auto-merged when mergeable, non-draft, and not blocked by review.
- Runtime and product PRs require passing relevant tests or checks and no blocking review before auto-merge.
- CI failures, merge conflicts, and blocking reviews become the next task until fixed or explicitly deferred.

## Mirror Policy

Use this file only as a compact status mirror. Do not rely on it for the full operating contract. For a human-friendly quick start, read `ai_first/USAGE_GUIDE.md`.
## 2026-04-28

- `main` now includes submission-close Phase 1 through PRs `#210`, `#212`, and `#211` plus the optional Phase 2 polish train through PRs `#214`, `#215`, `#216`, and `#217`.
- The authoritative contest package now has command-backed validation current on 2026-04-28 and an active docs-only lane refreshing the previously stale Knowledge, Tutor, Dashboard, and `/agents` screenshot rows.
- Optional AI-owned next work after this lane should return to human review, optional video, or another newly approved packet from `main`.
