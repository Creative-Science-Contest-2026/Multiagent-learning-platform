# Execution Queue

Last updated: 2026-04-25

This is the compact status board for humans and AI workers.  
The authoritative control plane is still `ai_first/AI_OPERATING_PROMPT.md`.

## Latest merged result

- Latest merged PR: `#127 docs: sync control plane after lane rollout`
- Latest smoke result: the 2026-04-25 scripted-reset smoke pass succeeded against current `main`.
- The two-lane contest MVP polish experiment is now fully merged to `main`:
  `#122` (`T044`), `#124` (`T045`), `#125` (`T046`), `#121` (`T049`), `#123` (`T050`), and `#126` (`T051`).
- Core MVP path in `main` now also includes contest-facing Vietnamese UI coverage, marketplace and knowledge-screen polish, dashboard/review polish, deeper dashboard insight payloads, richer metadata contracts, and improved session context support on top of the earlier marketplace, assessment, tutor, dashboard, offline, analytics, evidence, and submission flows.

## Active queue

- Active docs/evidence lane: `T036 Contest Smoke and Evidence Refresh`
- Current purpose: keep command-backed evidence current and mark screenshot freshness honestly after the merged contest UI changes.

## Next recommended task

Refresh the screenshot bundle or complete the human evidence review step:

1. Capture a fresh screenshot bundle for the contest-facing UI updated by `T044`, `T045`, and `T046`
2. Update `docs/contest/EVIDENCE_CHECKLIST.md` from `Stale` to `Current` only after the new capture exists
3. If screenshot capture cannot happen now, keep the current command evidence and carry the screenshot freshness gap as an explicit human follow-up

## Status Update (2026-04-25)

**Queue Advance**:
1. `T047` and `T048` succeeded: the two-lane experiment had bounded ownership and clean merge flow.
2. Lane 1 completed `T044`, `T045`, and `T046`.
3. Lane 2 completed `T049`, `T050`, and `T051`.
4. The 2026-04-25 scripted-reset smoke run passed on current `main`.
5. Screenshot evidence is now explicitly `Stale` because the last capture predates the merged contest-facing UI changes.

## AI-owned blockers

- None currently for command-backed validation.
- Screenshot freshness remains a human capture follow-up unless a browser-capable worker refreshes the bundle.

## Human-review blockers

- Human-only submission items still remain for the contest package, including IP commitment review, optional video decision, and final package sign-off.
- Those human blockers no longer prevent the repo from running a separate contest MVP polish backlog.

## Read path

1. `ai_first/AI_OPERATING_PROMPT.md`
2. `ai_first/EXECUTION_QUEUE.md`
3. `ai_first/ACTIVE_ASSIGNMENTS.md`
4. `docs/contest/VALIDATION_REPORT.md`
5. `docs/contest/EVIDENCE_CHECKLIST.md`
6. `docs/contest/DEMO_DATA_RESET.md`

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
