# Execution Queue

Last updated: 2026-04-23

This is the compact status board for humans and AI workers.  
The authoritative control plane is still `ai_first/AI_OPERATING_PROMPT.md`.

## Latest merged result

- Latest merged PR: `#74 [MVP] T025 Adaptive Difficulty Selection`
- `#74` added coordinator-side adaptive quiz difficulty selection from recent quiz performance context, then passed all required CI checks before merge.
- Core MVP path in `main` now includes marketplace import, preview, ratings, sorting, cached marketplace browsing, assessment insights, adaptive difficulty selection, PDF export, tutoring session replay, recommendation flow, KB context badges, student progress dashboard, teacher dashboard filtering, Vietnamese prompts, route error boundaries, API rate limiting, and teacher collaboration metadata in addition to the earlier Knowledge Pack, assessment, tutor, dashboard, and contest evidence flows.

## Active queue

- Active issue: `#75 [MVP] Mobile-First Marketplace Responsive Design`
- Active branch: `pod-a/t026-marketplace-mobile`
- Active task packet: `docs/superpowers/tasks/2026-04-23-T026-marketplace-mobile.md`
- Focus set: `T026` (Marketplace mobile responsive design)

## Next recommended task

Implement `T026` on `pod-a/t026-marketplace-mobile`, then open a Draft PR with a Mermaid architecture note and required validation before review.

## Status Update (2026-04-21)

**Queue Advance**:
1. `#74` merged to `main` after all required CI checks passed
2. Issue `#73` auto-closed with the merge
3. Next pending registry task selected in strict order: `T026 Mobile-First Marketplace Responsive Design`
4. Issue `#75` created and task packet added for the new execution lane

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
| T017: Dashboard Filtering | Completed | 2 | NO | Done |
| T018: Vietnamese Prompts | Completed | 4 | YES | Done |
| T019: Marketplace Sorting | Completed | 1.5 | NO | Done |
| T020: Assessment Export PDF | Completed | 3 | NO | Done |
| T021: Session Replay | Completed | 3 | NO | Done |
| T023: Cache Optimization | Completed | 2 | NO | Done |
| T024: Team Sharing | Completed | 6 | NO | Done |
| T025: Adaptive Difficulty | Completed | 5 | NO | Done |
| T026: Marketplace Mobile | In Progress | 1 | NO | Now |
| T022: Error Boundaries | Completed | 2 | NO | Done |
| T028: Rate Limiting | Completed | 2 | YES | Done |

**Resources**: See `ai_first/TASK_REGISTRY.json` (full task list with effort estimates) and `ai_first/MVP_GAP_ANALYSIS.md` (detailed audit with risk assessment).
