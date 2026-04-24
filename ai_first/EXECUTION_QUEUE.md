# Execution Queue

Last updated: 2026-04-24

This is the compact status board for humans and AI workers.  
The authoritative control plane is still `ai_first/AI_OPERATING_PROMPT.md`.

## Latest merged result

- Latest merged PR: `#99 [Docs] T037 Contest screenshot evidence refresh`
- `#99` refreshed the linked contest screenshot bundle on 2026-04-24, so screenshot evidence is `Current` again on `main`.
- Core MVP path in `main` now includes marketplace import, preview, ratings, sorting, cached marketplace browsing, mobile-first marketplace layout, metadata-driven marketplace search, batch import, offline-ready imported-pack fallback, offline quiz-result sync queue, assessment insights, adaptive difficulty selection, teacher analytics, assessment timing metrics, tutor follow-up prompts, knowledge-pack version metadata, student learning-path sequencing, PDF export, tutoring session replay, recommendation flow, KB context badges, student progress dashboard, Vietnamese prompts, route error boundaries, API rate limiting, and teacher collaboration metadata in addition to the earlier Knowledge Pack, assessment, tutor, dashboard, and contest evidence flows.

## Active queue

- Active short task: `T038 Contest Submission Package Freshness Sync`
- Branch: `docs/t038-submission-readiness-sync`
- Goal: sync the contest-facing README and submission package with the latest 2026-04-24 smoke and screenshot evidence state.

## Next recommended task

Publish the submission-readiness sync lane, then reassess whether any remaining contest evidence gaps or MVP/runtime gaps still need a new short task.

## Status Update (2026-04-24)

**Queue Advance**:
1. `#99` merged to `main` after all required CI checks passed
2. Issue `#97` auto-closed with the merge
3. `T037 Contest Screenshot Evidence Refresh` is now complete on `main`
4. Opened issue `#100` for `T038 Contest Submission Package Freshness Sync`
5. The next lane syncs contest-facing entry docs that still point at the older 2026-04-19 evidence state

## AI-owned blockers

- None currently. The command-backed smoke lane passed on 2026-04-24 and is already merged into `main`.

## Human-review blockers

- None currently. Command evidence and screenshot evidence are both current on `main`; the remaining gap is submission-facing doc freshness.

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
| T030: Assessment Time | Completed | 2 | NO | Done |
| T031: Tutor Follow-Up Questions | Completed | 3 | NO | Done |
| T032: Knowledge Pack Versioning | Completed | 4 | NO | Done |
| T033: Suggested Learning Path Sequencing | Completed | 6 | NO | Done |
| T034: Batch Import Multiple Packs | Completed | 2 | NO | Done |
| T035: Offline Mode for Downloaded Packs | Completed | 6 | NO | Done |
| T022: Error Boundaries | Completed | 2 | NO | Done |
| T028: Rate Limiting | Completed | 2 | YES | Done |

**Resources**: See `ai_first/TASK_REGISTRY.json` (full task list with effort estimates) and `ai_first/MVP_GAP_ANALYSIS.md` (detailed audit with risk assessment).
