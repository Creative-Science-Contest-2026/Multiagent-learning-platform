# Execution Queue

Last updated: 2026-04-20

This is the compact status board for humans and AI workers.  
The authoritative control plane is still `ai_first/AI_OPERATING_PROMPT.md`.

## Latest merged result

- Latest merged PR: `#44 feat: complete autopilot batch for marketplace import, API throttling, route resilience, assessment insights, and KB context badges`
- Follow-up fix PRs `#48` and `#49` were merged first, then folded into `#44`, and all required CI checks passed before merge.
- Core MVP path in `main` now includes marketplace import, assessment insights, KB context badges, route error boundaries, and API rate limiting in addition to the earlier Knowledge Pack, assessment, tutor, dashboard, and contest evidence flows.

## Active queue

- Active issue: `#50 [MVP] Teacher Knowledge Pack Sharing UI`
- Active branch: `pod-a/t012-pack-sharing-ui`
- Active task packet: `docs/superpowers/tasks/2026-04-20-T012-teacher-pack-sharing-ui.md`
- Focus set: `T012` (teacher-facing sharing controls for knowledge packs)

## Next recommended task

Implement `T012` on `pod-a/t012-pack-sharing-ui`, then open a Draft PR with a Mermaid architecture note and required validation before review.

## Status Update (2026-04-20)

**Queue Advance**:
1. `#44` merged to `main` after `Backend`, `Frontend`, `Docs`, and `Summary` checks passed
2. Next pending registry task selected in strict order: `T012 Teacher Knowledge Pack Sharing UI`
3. Issue `#50` created and task packet added for the new execution lane

## AI-owned blockers

- None currently. The scripted-reset smoke lane passed with demo-safe reset output, backend startup through the CLI server path, frontend production build, Knowledge Pack metadata, assessment session evidence, tutor session evidence, and dashboard activity.

## Human-review blockers

- None currently. Human review is still required for product direction changes, deployment or credential decisions, and any PR explicitly marked blocked.

## Read path

1. `ai_first/AI_OPERATING_PROMPT.md`
2. `ai_first/EXECUTION_QUEUE.md`
3. Task packet for the active branch
4. `ai_first/CURRENT_STATE.md` only if more context is needed

---

## Critical Path Phase 1 (Next 2 Weeks)

| Task | Status | Hours | Blocker | Start |
|------|--------|-------|---------|-------|
| T009: Marketplace Import | Completed | 4 | YES | Done |
| T010: Assessment Feedback | Completed | 6 | YES | Done |
| T011: KB Context Badges | Completed | 2 | NO | Done |
| T012: Teacher Sharing UI | In Progress | 3 | NO | Now |
| T018: Vietnamese Prompts | Not Started | 4 | YES | Parallel |
| T022: Error Boundaries | Completed | 2 | NO | Done |
| T028: Rate Limiting | Completed | 2 | YES | Done |

**Resources**: See `ai_first/TASK_REGISTRY.json` (full task list with effort estimates) and `ai_first/MVP_GAP_ANALYSIS.md` (detailed audit with risk assessment).
