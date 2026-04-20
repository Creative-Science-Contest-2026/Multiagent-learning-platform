# AI Operating Prompt

This is the authoritative AI-first operating file for this repository.
If there is a conflict between this file and any compatibility snapshot, this file wins.

## Mission

Build a stable VnExpress Sáng kiến Khoa học 2026 MVP:

Teacher creates Knowledge Pack -> AI generates assessment -> Student learns with Tutor Agent -> Teacher sees dashboard.

## Compatibility model

- `ai_first/AI_OPERATING_PROMPT.md` is the single entry point.
- `ai_first/EXECUTION_QUEUE.md` is the compact queue/status board for humans and AI workers who need the shortest current read.
- `ai_first/AI_FIRST_ROADMAP.md` is the human-facing roadmap for the autonomous AI-first loop and future operating improvements.
- `ai_first/CURRENT_STATE.md` and `ai_first/NEXT_ACTIONS.md` are compatibility snapshots only.
- If a task packet exists, it remains the execution contract for the current feature pod.
- If no task packet exists yet, the prompt and approved plan are the bootstrap contract.

## Current snapshot

- Repository: `Creative-Science-Contest-2026/Multiagent-learning-platform`
- Base project: HKUDS/DeepTutor under Apache 2.0
- Mainline status: Milestone 0 AI-first operating layer merged into `main` on 2026-04-13.
- Goal: keep the repo self-directing enough that an AI worker can start from this prompt, read the current context, and continue without manual orchestration.
- Latest product status: Knowledge Pack, marketplace import, assessment generation and review insights, student tutoring context, KB context badges, Teacher Dashboard, route error boundaries, API rate limiting, contest evidence screenshots, and backend/frontend/docs CI are merged into `main`.
- Latest operating status: `ai_first/EXECUTION_QUEUE.md` is the shortest queue/status board, the scripted-reset smoke lane has passed against the current local demo dataset, `docs/contest/` carries the latest smoke-backed evidence refresh record, student progress dashboard is now merged into `main` through PR `#54`, and the active short task is `T015 AI-Powered Assessment Recommendations`.
- Operating model: Markdown is source of truth; GitHub Issues and PRs are execution mirrors; the prompt is the control plane.

## Required startup sequence

Before edits:

1. Read `AGENTS.md`.
2. Read this file.
3. Run `git status --short --branch`.
4. Read the relevant spec, plan, task packet, or compatibility snapshot only if the prompt points to one.
5. Confirm the assigned task scope, owned files, and do-not-touch files.

## Work rules

- Never push directly to `main`.
- Use a focused branch.
- Open every PR in review mode: create as Draft first, then move to Ready for review after self-review.
- Do not merge any PR unless all required CI checks are green.
- Respect `Owned files/modules` and `Do-not-touch files/modules`.
- For bootstrap tasks before task packets exist, use the current plan task's `Files:` section as the owned-file contract.
- Do not revert user or other-agent changes.
- Do not remove Apache 2.0 license or upstream credit.
- Do not modify lockfiles unless dependency changes require it.
- Prefer small, reviewable commits.
- Do not broaden scope just because the repo contains more files; stay inside the task packet or bootstrap contract.

## AI-first operating rules

- Treat this file as the control plane for the repo-level AI-first workflow.
- Treat `ai_first/AI_FIRST_ROADMAP.md` as the readable roadmap for what the AI loop does now and where it should evolve next.
- Keep instructions short, direct, and executable.
- Prefer one source of truth over multiple overlapping instructions.
- If a newer project status needs to be captured, update this file first and then mirror the shortest useful summary to the compatibility snapshots.
- When a feature, tool, route, data model, or workflow rule changes, update `ai_first/architecture/MAIN_SYSTEM_MAP.md`.
- Every PR must include a Markdown architecture note under `docs/superpowers/pr-notes/` with at least one Mermaid diagram.
- Every PR must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` was updated.

## Autonomous completion loop

After opening or updating a PR, classify it before handing off:

- Every PR must start as Draft and only move to Ready for review after local validation and checklist completion.
- No PR may be merged unless all required CI checks have passed.
- Docs, task, and workflow PRs may be auto-merged only when the PR is mergeable, non-draft, CI is green, and there is no blocking review or unresolved required discussion.
- Runtime and product PRs may be auto-merged only when relevant tests and required checks pass, CI is green, and there is no blocking review.
- If CI fails, fixing CI is the next task. Do not start a new feature until the failing PR is fixed or explicitly deferred.
- If review blocks the PR, address the review before merging or continuing.
- After a successful merge, sync from `main`, update the daily log and compact status mirrors when useful, then select the next task.
- Select next work in this order: active PR blockers, active task packets, `ai_first/NEXT_ACTIONS.md`, then the long-term MVP goal.
- If the next product change has no task packet, create or update a task packet before implementation.

## Execution contract

When starting work, do the following in order:

1. Identify the active branch and task packet.
2. Confirm owned files and do-not-touch files.
3. Check whether the change is docs-only, workflow-only, or a runtime change.
4. Read the minimum additional context needed.
5. Make the smallest useful change.
6. Run the relevant test or validation command.
7. Update this file if the repo-level operating model changed.
8. Update the daily log and handoff notes.

## Completion rules

Before handing off:

1. Run relevant tests or explain why they could not be run.
2. Record tests and failures.
3. Update `ai_first/daily/YYYY-MM-DD.md`.
4. Update this file if status, workflow, or next actions changed.
5. Confirm the PR is Ready for review (not Draft) before requesting merge.
6. Confirm all required CI checks are green before merge.
7. Check whether the PR is eligible for autonomous merge under the merge policy.
8. Add handoff notes with changed files, risks, merge status, and the next recommended read path.
## Task Tracking System

The project uses a structured task registry to track MVP gaps, priorities, and progress:

### Key Files

- `ai_first/TASK_REGISTRY.json` - Authoritative task list with metadata, priorities, and dependencies
- `ai_first/MVP_GAP_ANALYSIS.md` - Detailed audit report with issue descriptions, risk assessment, and roadmap

### Task Status Workflow

Tasks flow through states:
- **not-started**: Issue identified, not yet assigned
- **in-progress**: Active work, updated daily
- **completed**: Merged to main or stable branch

### Task Priority Levels

- **P1 Critical**: Blockers for contest submission, MVP incomplete
- **P2-P3 High**: Essential for MVP, fix next
- **P4-P10 Medium**: Important UX/features, schedule for later
- **P11-P27 Low**: Nice-to-have, polish items

### Workflow: MVP Gap Analysis to Execution

1. **Discovery**: Read `ai_first/MVP_GAP_ANALYSIS.md` for complete audit
2. **Selection**: Choose next task from Phase 1 (critical path) in JSON registry
3. **Planning**: Create or update task packet in `docs/superpowers/tasks/`
4. **Execution**: Follow Execution Contract rules above
5. **Tracking**: Update `TASK_REGISTRY.json` status field as work progresses
6. **Mirror**: Keep GitHub issues in sync with `TASK_REGISTRY.json` status

### AI Worker Quick Start

When starting a new feature or fix:
1. Check `ai_first/TASK_REGISTRY.json` for matching task ID
2. Note the priority, effort estimate, and file scope
3. Read the related section in `ai_first/MVP_GAP_ANALYSIS.md`
4. Create feature branch: `pod-a/<task-name>`, `pod-b/<task-name>`, or `fix/<task-name>`
5. Create GitHub issue using template from JSON `github_issues_template` section
6. Link PR to issue
7. Update JSON status → "in-progress" when starting
8. Update JSON status → "completed" when merged to main

### Critical P1 Tasks (Block before contest submission)

| Task ID | Title | Blocker | Phase |
|---------|-------|---------|-------|
| T009 | Marketplace Import | Fake placeholder only | 1 |
| T010 | Assessment Feedback | Minimal recommendations | 1 |
| T018 | Vietnamese Prompts | English-only LLM responses | 1 |
| T028 | Rate Limiting | API abuse risk | 1 |

### Integration with Existing Rules

- Task packets created from TASK_REGISTRY inherit `Files:` field as owned-file contract
- Every PR updates corresponding task status in JSON
- Daily logs reference task IDs for tracking progress
- Architecture changes trigger MAIN_SYSTEM_MAP.md updates per the task scope

## Next actions

1. Keep this file as the single entry point for future AI workers.
2. Use `ai_first/EXECUTION_QUEUE.md` as the shortest status board.
3. Use `ai_first/USAGE_GUIDE.md` as the human-friendly quick start.
4. Use `ai_first/AI_FIRST_ROADMAP.md` to understand the autonomous loop and future operating direction.
5. Keep `ai_first/EXECUTION_QUEUE.md` current after merges, blocker changes, and task selection.
6. Keep GitHub issue state aligned with merged PRs so the queue mirrors real work, not historical leftovers.
7. Continue from the next pending registry task in strict order after every successful merge or verification pass; current next task is `T015`.
8. Keep the demo-readiness smoke lane current after meaningful merges and treat smoke failures as the next task.
9. Use `docs/contest/DEMO_DATA_RESET.md` before smoke when local demo state may be stale, missing, or private.
10. Run the scripted reset command before the next smoke/evidence refresh so the merged utility is validated end to end.
11. Keep `docs/contest/VALIDATION_REPORT.md` as the latest smoke-backed evidence freshness record, and update `EVIDENCE_CHECKLIST.md` when screenshot or video status changes.
12. If the execution queue becomes empty, derive the next short task from the MVP goal and create or update a task packet before implementation.
13. Keep `docs/superpowers/tasks/` populated with current Feature Pod task packets before implementation starts.
14. Mirror only the minimal status needed into `ai_first/CURRENT_STATE.md` and `ai_first/NEXT_ACTIONS.md`.
15. Use the approved docs/AI-first operating layer to drive feature pods, PRs, autonomous completion, and evidence.
