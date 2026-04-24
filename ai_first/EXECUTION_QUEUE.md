# Execution Queue

Last updated: 2026-04-24

This is the compact status board for humans and AI workers.  
The authoritative control plane is still `ai_first/AI_OPERATING_PROMPT.md`.

## Latest merged result

- Latest merged PR: `#80 [MVP] T029 Marketplace Full-Text Search`
- `#80` upgraded marketplace search to match broader metadata and objective text through the list API, then passed all required CI checks before merge.
- Core MVP path in `main` now includes marketplace import, preview, ratings, sorting, cached marketplace browsing, mobile-first marketplace layout, metadata-driven marketplace search, assessment insights, adaptive difficulty selection, teacher analytics, PDF export, tutoring session replay, recommendation flow, KB context badges, student progress dashboard, Vietnamese prompts, route error boundaries, API rate limiting, and teacher collaboration metadata in addition to the earlier Knowledge Pack, assessment, tutor, dashboard, and contest evidence flows.

## Active queue

- Active issue: `#81 [MVP] T030 Assessment Time Tracking & Analytics`
- Active branch: `pod-a/t030-assessment-time`
- Active task packet: `docs/superpowers/tasks/2026-04-24-T030-assessment-time.md`
- Focus set: `T030` (Assessment time tracking)

## Next recommended task

Publish the completed `T030` implementation from `pod-a/t030-assessment-time` as a Draft PR, then monitor CI and merge before opening `T031`.

## Status Update (2026-04-24)

**Queue Advance**:
1. `#80` merged to `main` after all required CI checks passed
2. Issue `#79` auto-closed with the merge
3. Next pending registry task selected in strict order: `T030 Assessment Time Tracking & Analytics`
4. Task packet and execution lane created immediately
5. Issue `#81` now mirrors the active `T030` lane after the earlier transient GitHub CLI `503` issue cleared
6. `T030` implementation and validation are complete locally; the lane is ready for commit/push/Draft PR

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
| T026: Marketplace Mobile | Completed | 1 | NO | Done |
| T027: Analytics Dashboard | Completed | 8 | NO | Done |
| T029: Marketplace Search | Completed | 3 | NO | Done |
| T030: Assessment Time | In Progress | 2 | NO | Now |
| T022: Error Boundaries | Completed | 2 | NO | Done |
| T028: Rate Limiting | Completed | 2 | YES | Done |

**Resources**: See `ai_first/TASK_REGISTRY.json` (full task list with effort estimates) and `ai_first/MVP_GAP_ANALYSIS.md` (detailed audit with risk assessment).
