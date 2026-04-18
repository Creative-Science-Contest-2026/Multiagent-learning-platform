# AI-First Usage Guide

This repository is designed so an AI worker can begin from one entry point and continue with minimal hand-holding.

## What to read first

1. `ai_first/AI_OPERATING_PROMPT.md`
2. `AGENTS.md`
3. `ai_first/CURRENT_STATE.md` if you need a compact status mirror
4. `ai_first/NEXT_ACTIONS.md` if you need the current queue

## How to start a task

1. Check `git status --short --branch`.
2. Confirm your branch name and task packet.
3. Read only the files listed in the task packet or bootstrap contract.
4. Stay inside the owned files/modules.
5. Do not touch files marked do-not-touch.

## How the repo is organized

- `ai_first/AI_OPERATING_PROMPT.md`: the control plane and single entry point.
- `ai_first/AI_FIRST_ROADMAP.md`: human-facing explanation of the autonomous AI loop and future operating direction.
- `ai_first/CURRENT_STATE.md`: compact status mirror.
- `ai_first/NEXT_ACTIONS.md`: compact queue mirror.
- `ai_first/architecture/`: Mermaid system maps and feature maps.
- `docs/superpowers/specs/`: approved designs.
- `docs/superpowers/plans/`: implementation plans.
- `docs/superpowers/tasks/`: task packets for feature pods.
- `docs/superpowers/pr-notes/`: required PR architecture notes.

## What AI should do after changes

1. Run relevant tests or explain why they were not run.
2. Update the daily log for the current date.
3. Update `ai_first/AI_OPERATING_PROMPT.md` if the operating model changed.
4. Mirror only the minimum status into `CURRENT_STATE.md` and `NEXT_ACTIONS.md` if needed.
5. Leave handoff notes in the PR and task packet.

## What AI should do after a PR is ready

1. Classify the PR as docs/task/workflow or runtime/product.
2. For docs/task/workflow PRs, auto-merge only when mergeable, non-draft, and not blocked by review.
3. For runtime/product PRs, auto-merge only when relevant tests or checks pass and no review blocks the PR.
4. Treat failing CI, merge conflicts, and blocking reviews as the next task until fixed or explicitly deferred.
5. After merge, sync from `main`, update status notes if useful, then select the next task from active PR blockers, task packets, `NEXT_ACTIONS.md`, or the long-term MVP goal.

For the readable version of this loop and its future direction, read `ai_first/AI_FIRST_ROADMAP.md`.

## What not to do

- Do not push directly to `main`.
- Do not modify files outside scope without updating the task packet.
- Do not remove Apache 2.0 license headers or upstream credit.
- Do not add extra operating files unless they solve a real problem.
