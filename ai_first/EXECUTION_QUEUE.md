# Execution Queue

Last updated: 2026-04-26

This is the compact status board for humans and AI workers.  
The authoritative control plane is still `ai_first/AI_OPERATING_PROMPT.md`.

## Latest merged result

- Latest feature-risk merge: `#153 [R2] feat(evidence): strengthen diagnosis credibility framing`
- Lane 1 (`2026-04-26-lane-1-agent-spec-authoring`) merged to `main` through PR `#136`.
- Lane 2 (`2026-04-26-lane-2-spec-runtime-assembly`) merged to `main` through PR `#135`.
- Lane 3 (`2026-04-26-lane-3-observation-student-state`) merged to `main` through PR `#140`.
- Lane 4 (`2026-04-26-lane-4-diagnosis-recommendation`) merged to `main` through PR `#142`.
- Lane 5 (`2026-04-26-lane-5-teacher-insight-ui`) merged to `main` through PR `#144`.
- Lane 6 (`2026-04-26-lane-6-evaluation-evidence-readiness`) merged to `main` through PR `#145`.
- Dashboard and `/agents` evidence recapture merged to `main` through PR `#147`.
- Post-147 evidence merge sync merged to `main` through PR `#148`.
- Risk Lane 1 runtime binding proof merged to `main` through PR `#151`.
- Risk Lane 2 diagnosis credibility merged to `main` through PR `#153`.
- Latest smoke result: the 2026-04-26 scripted-reset smoke pass succeeded in lane 6 (`docs/evaluation-evidence-readiness`) against current `main` behavior.
- The two-lane contest MVP polish experiment is now fully merged to `main`:
  `#122` (`T044`), `#124` (`T045`), `#125` (`T046`), `#121` (`T049`), `#123` (`T050`), and `#126` (`T051`).
- Core MVP path in `main` now also includes the Wave 1 evidence spine: structured observations, student-state persistence, assessment diagnosis, and teacher insight payloads on top of the earlier marketplace, assessment, tutor, dashboard, offline, analytics, evidence, and submission flows.

## Active queue

- No active AI implementation task remains on `main`.
- The contest repo now also has six merged risk-hardening lane packets for judge/voter attack-surface defense.

## Next recommended task

- If the team wants to continue AI-owned product hardening, start `R3_ASSESSMENT_SAFETY` from `docs/superpowers/tasks/2026-04-26-risk-lane-3-assessment-safety.md`.
- If not, the shortest remaining non-code path is still human review of the submission package, IP commitment, and optional video decision.
- Any new AI task should start from a fresh branch/worktree off `main`, not from a merged lane branch.

If a requested task appears to span multiple packets, stop and ask the human to resolve the lane boundary before editing.

## Status Update (2026-04-25)

**Queue Advance**:
1. `T047` and `T048` succeeded: the two-lane experiment had bounded ownership and clean merge flow.
2. Lane 1 completed `T044`, `T045`, and `T046`.
3. Lane 2 completed `T049`, `T050`, and `T051`.
4. The 2026-04-25 scripted-reset smoke run passed on current `main`.
5. Screenshot evidence was refreshed and merged on 2026-04-25 through PR `#130`.

## AI-owned blockers

- None currently. The next AI-owned work is optional risk-hardening, not a blocker for the already-validated MVP path.

## Human-review blockers

- Human-only submission items remain for the contest package, including IP commitment review, optional video decision, and final package sign-off.
- Screenshot evidence is current; the remaining blockers are no longer browser-refresh tasks.

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
