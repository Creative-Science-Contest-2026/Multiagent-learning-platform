# Execution Queue

Last updated: 2026-04-25

This is the compact status board for humans and AI workers.  
The authoritative control plane is still `ai_first/AI_OPERATING_PROMPT.md`.

## Latest merged result

- Latest merged PR: `#105 [Docs] T040 Contest product description draft`
- `#105` added the reusable contest product description draft and narrowed the remaining AI-doable submission gap to the fork-modifications note.
- Core MVP path in `main` now includes marketplace import, preview, ratings, sorting, cached marketplace browsing, mobile-first marketplace layout, metadata-driven marketplace search, batch import, offline-ready imported-pack fallback, offline quiz-result sync queue, assessment insights, adaptive difficulty selection, teacher analytics, assessment timing metrics, tutor follow-up prompts, knowledge-pack version metadata, student learning-path sequencing, PDF export, tutoring session replay, recommendation flow, KB context badges, student progress dashboard, Vietnamese prompts, route error boundaries, API rate limiting, and teacher collaboration metadata in addition to the earlier Knowledge Pack, assessment, tutor, dashboard, and contest evidence flows.

## Active queue

- Active short task: `T041 Contest Fork Modifications Note`
- Branch: `docs/t041-fork-modifications`
- Goal: document how this fork extends HKUDS/DeepTutor for the contest MVP so the final AI-doable submission checklist item is backed by a repo note.

## Next recommended task

Publish the fork-modifications lane, then confirm the remaining submission checklist items are human-owned only.

## Status Update (2026-04-25)

**Queue Advance**:
1. `#105` merged to `main` after all required CI checks passed
2. Issue `#104` auto-closed with the merge
3. `T040 Contest Product Description Draft` is now complete on `main`
4. Opened issue `#106` for `T041 Contest Fork Modifications Note`
5. The next lane documents contest-specific fork changes so only human-review submission items remain unchecked

## AI-owned blockers

- None currently. The command-backed smoke lane passed on 2026-04-24 and is already merged into `main`.

## Human-review blockers

- Human-only submission items still remain, including IP commitment review and final package sign-off. `T041` is the last clearly AI-doable checklist alignment step.

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
