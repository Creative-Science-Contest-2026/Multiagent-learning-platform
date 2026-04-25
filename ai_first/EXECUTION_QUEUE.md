# Execution Queue

Last updated: 2026-04-25

This is the compact status board for humans and AI workers.  
The authoritative control plane is still `ai_first/AI_OPERATING_PROMPT.md`.

## Latest merged result

- Latest merged PR: `#87 [docs] Teacher-agent platform doctrine and AI-first engineering philosophy`
- `#87` merged the long-form engineering doctrine and reinforced the repo's bias toward bounded modules, explicit contracts, and future-safe parallel work.
- Previous workflow result: `#118` synced the queue, prompt, snapshots, and assignment board after the two-person collaboration workflow had already landed in `main`.
- Previous contest result: `#113` added the optional video storyboard/runbook without changing the deferred status of the video artifact itself.
- Core MVP path in `main` now includes marketplace import, preview, ratings, sorting, cached marketplace browsing, mobile-first marketplace layout, metadata-driven marketplace search, batch import, offline-ready imported-pack fallback, offline quiz-result sync queue, assessment insights, adaptive difficulty selection, teacher analytics, assessment timing metrics, tutor follow-up prompts, knowledge-pack version metadata, student learning-path sequencing, PDF export, tutoring session replay, recommendation flow, KB context badges, student progress dashboard, Vietnamese prompts, route error boundaries, API rate limiting, and teacher collaboration metadata in addition to the earlier Knowledge Pack, assessment, tutor, dashboard, and contest evidence flows.

## Active queue

- Active docs/control-plane rollout: `T047 Contest Flow Operating Hygiene Refresh`
- Active docs/control-plane rollout: `T048 Parallel Lane Task Packet Set`
- Current purpose: prepare a two-lane contest MVP polish experiment for two accounts or machines without overlapping file ownership by default.

## Next recommended task

Finish `T047` and `T048`, then start two parallel lanes:

1. Lane 1: `T044` Vietnamese coverage, then `T045` marketplace/knowledge polish, then `T046` dashboard/review polish
2. Lane 2: choose one bounded depth slice from `T049`, `T050`, or `T051`

## Status Update (2026-04-25)

**Queue Advance**:
1. The old "wait on human review only" queue state has been replaced by a two-lane contest MVP polish experiment.
2. `T047` refreshes stale coordination state before the experiment starts.
3. `T048` creates bounded task packets for both lanes so each account has explicit owned files.
4. Contest submission docs remain ready for human review in parallel with this product-quality backlog refresh.

## AI-owned blockers

- None currently. The immediate AI work is a docs/control-plane bootstrap before two bounded implementation lanes start.

## Human-review blockers

- Human-only submission items still remain for the contest package, including IP commitment review, optional video decision, and final package sign-off.
- Those human blockers no longer prevent the repo from running a separate contest MVP polish backlog.

## Read path

1. `ai_first/AI_OPERATING_PROMPT.md`
2. `ai_first/EXECUTION_QUEUE.md`
3. `ai_first/ACTIVE_ASSIGNMENTS.md`
4. `docs/superpowers/specs/2026-04-25-two-lane-contest-mvp-polish-design.md`
5. `docs/superpowers/tasks/2026-04-25-T047-contest-operating-hygiene-refresh.md`
6. `docs/superpowers/tasks/2026-04-25-T048-parallel-lane-task-packets.md`

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
