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
- Latest product status: Knowledge Pack, marketplace import, batch marketplace import, offline-ready imported-pack fallback, offline quiz-result sync queue, assessment generation and review insights, student tutoring context, KB context badges, Teacher Dashboard, Vietnamese MVP prompt variants, contest-facing Vietnamese UI coverage, marketplace sorting, cached marketplace browsing, mobile-first marketplace layout, metadata-driven marketplace search, marketplace and knowledge-screen polish, dashboard/review polish, dashboard insight depth, metadata depth, session context quality, assessment adaptive difficulty, teacher analytics, assessment PDF export, tutoring session replay, route error boundaries, API rate limiting, teacher invitation metadata, assessment time tracking, tutor follow-up prompts, knowledge-pack version metadata, teacher action execution, intervention assignment flow, recommendation acknowledgement flow, diagnosis feedback capture, intervention history view, recommendation feedback capture, conservative student-model enrichment, weak-evidence abstain gating, confidence calibration refinement, misconception taxonomy expansion, contest evidence screenshots, contest submission-package sync, checklist evidence alignment, contest product-description drafting, and contest fork-modifications documentation are merged into `main`.
- Latest operating status: `ai_first/EXECUTION_QUEUE.md` is the shortest queue/status board, `ai_first/ACTIVE_ASSIGNMENTS.md` is the active coordination board, the Wave 1 evidence spine is merged through PR `#132`, the six-lane Contest MVP+ roadmap remains documented under `docs/superpowers/tasks/2026-04-26-lane-*.md`, the optional post-contest future backlog is defined in `ai_first/TASK_REGISTRY.json` plus `docs/superpowers/tasks/2026-04-26-two-session-future-backlog.md`, and no AI implementation lane is currently active on `main` after `F107`, `F108`, `F109`, `F116`, `F117`, `F118`, and `F119`.
- Operating model: Markdown is source of truth; GitHub Issues and PRs are execution mirrors; the prompt is the control plane.

## Required startup sequence

Before edits:

1. Read `AGENTS.md`.
2. Read this file.
3. Run `git status --short --branch`.
4. Check `ai_first/ACTIVE_ASSIGNMENTS.md` if any parallel lane may already be active.
5. Read the relevant spec, plan, task packet, or compatibility snapshot only if the prompt points to one.
6. Confirm the assigned task scope, owned files, and do-not-touch files.

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
- Every commit must include the active task identifier from the task packet or task registry.
- Do not broaden scope just because the repo contains more files; stay inside the task packet or bootstrap contract.

## Commit message convention

- Treat the task packet as the source of truth for commit tagging.
- Every task packet should declare both a `Task ID` and a short `Commit tag`.
- If the work maps to `ai_first/TASK_REGISTRY.json`, use that task's registry ID as the commit tag, such as `T010`.
- If the work is a lane packet or operating/docs slice outside the registry, create a stable packet-local ID and short tag, such as `L3` or `OPS-COMMIT`.
- Use this commit format: `<type>(<scope>): <summary> [<commit-tag>]`
- Allowed `type` values: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`.
- Keep `<summary>` imperative, specific, and easy to scan in `git log`.
- Prefer one dominant task per commit. Include multiple tags only when one reviewable commit truly completes more than one owned task.
- If no task packet or registry entry exposes a usable task identifier yet, stop and update the task packet first instead of inventing an ad hoc suffix.
- Examples:
  - `feat(evidence): add tutoring observation rollups [L3]`
  - `docs(ai-first): define commit tagging convention [OPS-COMMIT]`
  - `fix(dashboard): preserve recommendation confidence badge [T010]`

## AI-first operating rules

- Treat this file as the control plane for the repo-level AI-first workflow.
- Treat `ai_first/AI_FIRST_ROADMAP.md` as the readable roadmap for what the AI loop does now and where it should evolve next.
- Keep instructions short, direct, and executable.
- Do not stop to ask for permission to continue to the next strict-order task when the autonomous path is clear.
- After each merge or completed verification pass, automatically open the next issue, task packet, branch, and worktree required by the workflow.
- Do not pad handoff messages with future-intent filler such as "next I will..." when the work should continue immediately; either continue doing it or report a real blocker.
- Only ask the human to intervene when a blocker, ambiguity, or high-risk decision cannot be resolved from repo context or existing operating rules.
- Prefer one source of truth over multiple overlapping instructions.
- If a newer project status needs to be captured, update this file first and then mirror the shortest useful summary to the compatibility snapshots.
- When a feature, tool, route, data model, or workflow rule changes, update `ai_first/architecture/MAIN_SYSTEM_MAP.md`.
- Every PR must include a Markdown architecture note under `docs/superpowers/pr-notes/` with at least one Mermaid diagram.
- Every PR must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` was updated.

## Engineering philosophy

- Build features with bounded modules, explicit contracts, and low coupling so future AI workers can extend the system without cross-feature breakage.
- Keep policy separate from runtime, observation separate from diagnosis, recommendation separate from execution, and retrieval infrastructure separate from pedagogy.
- Do not encode product rules as scattered prompt fragments or hidden side effects.
- Prefer small, isolated modules over shared god files and broad if-else growth.
- Treat clean architecture as a scaling prerequisite, not a cleanup task for later.
- Use `ai_first/ENGINEERING_PHILOSOPHY.md` as the long-form doctrine when planning or reviewing architecture-heavy work.

## Collaboration rules

- For two-person collaboration, prefer one person, one active task, one branch, and one PR.
- Do not start code work until the task is reflected in `ai_first/ACTIVE_ASSIGNMENTS.md`.
- Keep task packets current with owned files and do-not-touch scope before parallel work begins.
- Do not split one feature across two people unless it has been decomposed into separate task packets with separate ownership.
- Treat `ai_first/ACTIVE_ASSIGNMENTS.md` as the short-term coordination memory for active work.
- For the current Contest MVP+ split, prefer `1 session = 1 lane = 1 branch = 1 PR`.
- If the human provides only this file as context, this file must still tell the AI how to choose or validate a lane before editing.

## Session triage rules

- When the human says they are splitting work into sessions, first check whether a lane-specific task packet already exists in `docs/superpowers/tasks/2026-04-26-lane-*.md`.
- If a matching lane packet exists, treat that packet as the execution contract and stay inside its owned files.
- If two candidate lane packets could both apply, stop and ask the human which session owns the task before editing.
- If another active session already owns the relevant files or worktree area, stop and ask the human to resolve the conflict.
- If the requested work spans more than one lane, do not silently proceed across boundaries; ask the human whether to narrow scope or update the task packets first.
- When uncertain, recommend the safest lane or recommend creating a new packet rather than guessing.
- Prefer concrete recommendations such as branch names, worktree paths, and likely owning lane when reporting ambiguity.

## Same-machine parallel rules

- Two AI sessions on the same machine must not edit from the same filesystem checkout.
- If two sessions are active on one machine, each session must use a different git worktree under `.worktrees/` or another explicitly assigned path.
- Record the worktree path in `ai_first/ACTIVE_ASSIGNMENTS.md` before code starts.
- When starting a new lane on the same machine, first run `git fetch origin main`, then create the lane branch and worktree from `origin/main`.
- If a lane is continuing existing work, reopen its assigned worktree instead of reusing another lane's checkout.
- Do not run two sessions against the repo root at the same time unless one of them is docs-only and not editing files.

## Sync rules

- Prefer explicit `git fetch origin main` plus `git merge origin/main` inside the active lane worktree.
- Do not rely on plain `git pull` for lane sync because it hides which upstream branch was integrated.
- After another lane merges to `main`, every still-active lane must `git fetch origin main` and merge `origin/main` into its own feature branch before the next substantial edit.
- Do not merge one feature branch into another feature branch.
- Do not rebase a shared or review-active branch unless the human explicitly asks for that cleanup.
- If merge conflicts appear after syncing `origin/main`, resolving those conflicts becomes the current task before new feature edits continue.

## Autonomous completion loop

After opening or updating a PR, classify it before handing off:

- Every PR must start as Draft and only move to Ready for review after local validation and checklist completion.
- No PR may be merged unless all required CI checks have passed.
- Docs, task, and workflow PRs may be auto-merged only when the PR is mergeable, non-draft, CI is green, and there is no blocking review or unresolved required discussion.
- Runtime and product PRs may be auto-merged only when relevant tests and required checks pass, CI is green, and there is no blocking review.
- If CI fails, fixing CI is the next task. Do not start a new feature until the failing PR is fixed or explicitly deferred.
- If review blocks the PR, address the review before merging or continuing.
- After a successful merge, sync from `main`, update the daily log and compact status mirrors when useful, then select the next task.
- Task selection and lane creation should happen immediately after that sync unless a live blocker takes priority.
- Select next work in this order: active PR blockers, active task packets, `ai_first/NEXT_ACTIONS.md`, then the long-term MVP goal.
- If the next product change has no task packet, create or update a task packet before implementation.

## Execution contract

When starting work, do the following in order:

1. Identify the active branch and task packet.
2. Confirm the task ID and commit tag.
3. Confirm owned files and do-not-touch files.
4. Check whether the change is docs-only, workflow-only, or a runtime change.
5. Read the minimum additional context needed.
6. Make the smallest useful change.
7. Run the relevant test or validation command.
8. Update this file if the repo-level operating model changed.
9. Update the daily log and handoff notes.

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
- **P11-P43 Low**: Nice-to-have, polish items

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
9. Use the task packet or registry commit tag in every commit for that task

### Critical P1 Tasks (Block before contest submission)

| Task ID | Title | Blocker | Phase |
|---------|-------|---------|-------|
| T009 | Marketplace Import | Fake placeholder only | 1 |
| T010 | Assessment Feedback | Minimal recommendations | 1 |
| T018 | Vietnamese Prompts | English-only LLM responses | 1 |
| T028 | Rate Limiting | API abuse risk | 1 |

### Integration with Existing Rules

- Task packets created from TASK_REGISTRY inherit `Files:` field as owned-file contract
- Task packets should expose a `Task ID` and `Commit tag` so the AI can commit without guessing
- Every PR updates corresponding task status in JSON
- Daily logs reference task IDs for tracking progress
- Architecture changes trigger MAIN_SYSTEM_MAP.md updates per the task scope
- Post-MVP and upgrade work should be tracked in AI-readable `Now / Next / Later` buckets with product-pipeline context so future workers can continue without rebuilding intent from scratch.

## Next actions

1. Keep this file as the single entry point for future AI workers.
2. Use `ai_first/EXECUTION_QUEUE.md` as the shortest status board.
3. Use `ai_first/USAGE_GUIDE.md` as the human-friendly quick start.
4. Use `ai_first/AI_FIRST_ROADMAP.md` to understand the autonomous loop and future operating direction.
5. Keep `ai_first/EXECUTION_QUEUE.md` current after merges, blocker changes, and task selection.
6. Keep GitHub issue state aligned with merged PRs so the queue mirrors real work, not historical leftovers.
7. Continue from the next pending registry task in strict order after every successful merge or verification pass. The two-lane contest MVP polish experiment (`T044` through `T051`) is complete, the 2026-04-25 smoke refresh passed, and the refreshed screenshot bundle is now merged, so the next operational step is the remaining human review or optional video decision.
8. Keep the demo-readiness smoke lane current after meaningful merges and treat smoke failures as the next task.
9. Use `docs/contest/DEMO_DATA_RESET.md` before smoke when local demo state may be stale, missing, or private.
10. Run the scripted reset command before the next smoke/evidence refresh so the merged utility is validated end to end.
11. Keep `docs/contest/VALIDATION_REPORT.md` as the latest smoke-backed evidence freshness record, and update `EVIDENCE_CHECKLIST.md` when screenshot or video status changes.
12. If the execution queue becomes empty, derive the next short task from the MVP goal and create or update a task packet before implementation.
13. Keep `docs/superpowers/tasks/` populated with current Feature Pod task packets before implementation starts.
14. Mirror only the minimal status needed into `ai_first/CURRENT_STATE.md` and `ai_first/NEXT_ACTIONS.md`.
15. Use the approved docs/AI-first operating layer to drive feature pods, PRs, autonomous completion, and evidence.
16. When the repo is in multi-session mode, route AI workers through the lane-specific task packets first and ask the human to resolve any detected session overlap or contract ambiguity.
