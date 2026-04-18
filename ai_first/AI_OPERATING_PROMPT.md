# AI Operating Prompt

This is the authoritative AI-first operating file for this repository.
If there is a conflict between this file and any compatibility snapshot, this file wins.

## Mission

Build a stable VnExpress Sáng kiến Khoa học 2026 MVP:

Teacher creates Knowledge Pack -> AI generates assessment -> Student learns with Tutor Agent -> Teacher sees dashboard.

## Compatibility model

- `ai_first/AI_OPERATING_PROMPT.md` is the single entry point.
- `ai_first/AI_FIRST_ROADMAP.md` is the human-facing roadmap for the autonomous AI-first loop and future operating improvements.
- `ai_first/CURRENT_STATE.md` and `ai_first/NEXT_ACTIONS.md` are compatibility snapshots only.
- If a task packet exists, it remains the execution contract for the current feature pod.
- If no task packet exists yet, the prompt and approved plan are the bootstrap contract.

## Current snapshot

- Repository: `Creative-Science-Contest-2026/Multiagent-learning-platform`
- Base project: HKUDS/DeepTutor under Apache 2.0
- Mainline status: Milestone 0 AI-first operating layer merged into `main` on 2026-04-13.
- Goal: keep the repo self-directing enough that an AI worker can start from this prompt, read the current context, and continue without manual orchestration.
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

- Docs, task, and workflow PRs may be auto-merged when the PR is mergeable, non-draft, and has no blocking review or unresolved required discussion.
- Runtime and product PRs may be auto-merged only when relevant tests or required checks pass and there is no blocking review.
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
5. Check whether the PR is eligible for autonomous merge under the merge policy.
6. Add handoff notes with changed files, risks, merge status, and the next recommended read path.

## Next actions

1. Keep this file as the single entry point for future AI workers.
2. Use `ai_first/USAGE_GUIDE.md` as the human-friendly quick start.
3. Use `ai_first/AI_FIRST_ROADMAP.md` to understand the autonomous loop and future operating direction.
4. Keep `docs/superpowers/tasks/` populated with current Feature Pod task packets before implementation starts.
5. Mirror only the minimal status needed into `ai_first/CURRENT_STATE.md` and `ai_first/NEXT_ACTIONS.md`.
6. Use the approved docs/AI-first operating layer to drive feature pods, PRs, autonomous completion, and evidence.
