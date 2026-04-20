# Execution Queue

Last updated: 2026-04-21

This is the compact status board for humans and AI workers.  
The authoritative control plane is still `ai_first/AI_OPERATING_PROMPT.md`.

## Latest merged result

- Latest merged PR: `#58 [MVP] Add Pack Ratings & Reviews System`
- `#58` added lightweight marketplace ratings and review submission, then passed all required CI checks before merge.
- Core MVP path in `main` now includes marketplace import, preview, and ratings, assessment insights, recommendation flow, KB context badges, student progress dashboard, route error boundaries, and API rate limiting in addition to the earlier Knowledge Pack, assessment, tutor, dashboard, and contest evidence flows.

## Active queue

- Active issue: `#59 [MVP] Assessment History Filtering & Search`
- Active branch: `pod-a/t017-dashboard-filtering`
- Active PR: `#60 [MVP] Assessment History Filtering & Search` (Draft)
- Active task packet: `docs/superpowers/tasks/2026-04-21-T017-dashboard-filtering.md`
- Focus set: `T017` (dashboard filtering)

## Next recommended task

Monitor CI for `#60`, fix any failing checks on `pod-a/t017-dashboard-filtering`, then merge to `main` once all required checks are green.

## Status Update (2026-04-21)

**Queue Advance**:
1. `#58` merged to `main` after all required CI checks passed
2. Issue `#57` auto-closed with the merge
3. Next pending registry task selected in strict order: `T017 Assessment History Filtering & Search`
4. Issue `#59` created and task packet added for the new execution lane
5. Draft PR `#60` opened with validation complete and architecture note attached

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
| T012: Teacher Sharing UI | Completed | 3 | NO | Verified |
| T013: Marketplace Preview | Completed | 3 | NO | Done |
| T014: Student Progress Dashboard | Completed | 5 | NO | Done |
| T015: Assessment Recommendations | Completed | 6 | NO | Done |
| T016: Marketplace Ratings | Completed | 4 | NO | Done |
| T017: Dashboard Filtering | In Progress | 2 | NO | Now |
| T018: Vietnamese Prompts | Not Started | 4 | YES | Parallel |
| T022: Error Boundaries | Completed | 2 | NO | Done |
| T028: Rate Limiting | Completed | 2 | YES | Done |

**Resources**: See `ai_first/TASK_REGISTRY.json` (full task list with effort estimates) and `ai_first/MVP_GAP_ANALYSIS.md` (detailed audit with risk assessment).
