# Two-Person AI-First Collaboration Design

Date: 2026-04-25
Status: Approved design baseline
Scope: Two people, two machines, one shared git repository, AI-first coordination with minimal process overhead

## Purpose

This design defines the simplest coordination model that lets two people work faster on the same AI-first repository without stepping on each other, losing context, or forcing a heavy distributed control plane into `ai_first/`.

The goal is not to solve general multi-machine orchestration. The goal is to make two collaborators productive right now.

## Core operating model

Recommended model:

- one person = one active task
- one task = one task packet
- one task = one branch
- one task = one PR

This model is intentionally narrow. It optimizes for throughput, auditability, and clean handoff while keeping the repo structure close to the current AI-first operating model.

## What this design is not

This design does not try to add:

- distributed lane leasing
- multi-worker reclaim systems
- automatic remote claiming
- coordinator services

Those are possible future directions, but they are outside the current need.

## Collaboration principles

1. Each person should work on a separate task whenever possible.
2. A task should not be started unless a task packet exists or is updated first.
3. Every active task must have explicit owned files and do-not-touch scope.
4. A collaborator should claim a task before writing code.
5. Branches and PRs are the isolation and merge boundaries.
6. `ai_first/` should hold coordination memory, not a full distributed scheduler.

## Minimal coordination layer

The recommended coordination stack is:

- `TASK_REGISTRY.json` for backlog truth
- `docs/superpowers/tasks/` for execution contracts
- `ai_first/ACTIVE_ASSIGNMENTS.md` for short-term active coordination
- branch-per-task for isolation
- PR-per-task for merge control

This keeps each artifact focused:

- backlog selection
- scope contract
- active assignment visibility
- code isolation
- merge validation

## Task assignment workflow

Recommended workflow:

1. Select a task from the active queue or task registry.
2. Confirm the task packet is present and has clear scope.
3. Add the assignment to `ai_first/ACTIVE_ASSIGNMENTS.md`.
4. Create or switch to the task branch.
5. Work only inside the owned-file scope.
6. Open a Draft PR.
7. Update assignment and packet when blocked, paused, or merged.

Hard rule:

No assignment entry means no task start.

## ACTIVE_ASSIGNMENTS.md contract

This file should stay short and human- and AI-readable.

Recommended fields per assignment:

- `Owner`
- `Machine`
- `Task`
- `Status`
- `Branch`
- `Task packet`
- `Owned files`
- `PR`
- `Last update`
- `Next action`
- `Blocker`

Recommended status values:

- `in_progress`
- `blocked`
- `in_review`
- `paused`
- `merged`

## Handoff rules

Short handoff is mandatory at these points:

- task claimed
- scope changed
- blocked
- PR opened or updated
- stopping work
- merged

The handoff surfaces have distinct purposes:

- `ACTIVE_ASSIGNMENTS.md` = current working state
- task packet = execution contract
- daily log = short dated history
- PR = technical merge and review context

Every handoff should answer:

- what is being worked on
- what is left
- which files are in scope
- what was validated
- what the next action is

## Scope safety

The design assumes the two collaborators avoid shared edits by default.

Therefore:

- do not split one feature across two people unless it has been decomposed into separate task packets
- do not use broad ownership labels like "frontend" or "backend"
- update the task packet before expanding scope
- if two tasks may collide, re-scope before coding

## Why this works

This approach is effective because it avoids coordination theater.

It gives the team:

- speed from parallel work
- low merge conflict risk
- clear read paths for AI workers
- enough shared memory to continue across machines

It avoids:

- overbuilt lane systems
- stale distributed state
- hard-to-debug ownership conflicts
- process overhead that cancels out the value of having two machines

## Recommended files and operating updates

This design should be reflected in:

- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-25.md`

## Immediate next-step ideas

### Now

- Add the minimal `ACTIVE_ASSIGNMENTS.md` template
- Add short collaboration rules to the operating prompt
- Use the pattern on the next two independent tasks

### Next

- Tighten task packet templates so owned files and do-not-touch files are always present
- Add a small checklist for "before claiming" and "before merge"

### Later

- If the team grows beyond two people, evaluate whether a richer lane registry becomes worth the added complexity
