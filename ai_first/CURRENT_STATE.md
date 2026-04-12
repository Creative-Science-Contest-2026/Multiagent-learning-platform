# Current State

Last updated: 2026-04-12

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
- Two Feature Pods may work in parallel after shared operating files land.

## Active Branches and PRs

- Active branch: `docs/ai-first-project-os`
- Purpose: Milestone 0 AI-first Project OS setup.
- PR status: not opened yet from this worktree.
- Merge note: preserve parent-checkout historical files under `ai_first/2026-04-12-deeptutor-slimming/` when integrating this branch.

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

1. Milestone 0: AI-first Project OS.
2. Milestone 1: Competition demo narrative.
3. Milestone 2: Teacher Knowledge Pack MVP.
4. Milestone 3: Assessment Builder MVP.
5. Milestone 4: Student Tutor Workspace MVP.
6. Milestone 5: Teacher Dashboard MVP.
