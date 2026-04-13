# AI Operating Prompt

This is the authoritative AI-first operating file for this repository.
If there is a conflict between this file and any compatibility snapshot, this file wins.

## Mission

Build a stable VnExpress Sáng kiến Khoa học 2026 MVP:

Teacher creates Knowledge Pack -> AI generates assessment -> Student learns with Tutor Agent -> Teacher sees dashboard.

## Compatibility model

- `ai_first/AI_OPERATING_PROMPT.md` is the single entry point.
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
- Keep instructions short, direct, and executable.
- Prefer one source of truth over multiple overlapping instructions.
- If a newer project status needs to be captured, update this file first and then mirror the shortest useful summary to the compatibility snapshots.
- When a feature, tool, route, data model, or workflow rule changes, update `ai_first/architecture/MAIN_SYSTEM_MAP.md`.
- Every PR must include a Markdown architecture note under `docs/superpowers/pr-notes/` with at least one Mermaid diagram.
- Every PR must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` was updated.

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
5. Add handoff notes with changed files, risks, and the next recommended read path.

## Next actions

1. Keep this file as the single entry point for future AI workers.
2. Use `ai_first/USAGE_GUIDE.md` as the human-friendly quick start.
3. Keep `docs/superpowers/tasks/` populated with current Feature Pod task packets before implementation starts.
4. Mirror only the minimal status needed into `ai_first/CURRENT_STATE.md` and `ai_first/NEXT_ACTIONS.md`.
5. Use the approved docs/AI-first operating layer to drive feature pods, PRs, and evidence.
