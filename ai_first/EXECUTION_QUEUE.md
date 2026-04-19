# Execution Queue

Last updated: 2026-04-19

This is the compact status board for humans and AI workers.  
The authoritative control plane is still `ai_first/AI_OPERATING_PROMPT.md`.

## Latest merged result

- Latest merged PR before the current active branch: `#42`, which queued the contest submission package lane.
- Core MVP path is already in `main`: Knowledge Pack, Assessment Builder, Student Tutor context, Teacher Dashboard, contest evidence screenshots, and backend/frontend/docs CI.
- Smoke-backed evidence refresh rules, the local demo reset command, and the scripted-reset smoke result now live in `docs/contest/` on `main`.

## Active queue

- Open issue: `#41 docs: prepare contest submission package`
- Active task packet: `docs/superpowers/tasks/2026-04-19-contest-submission-package.md`
- Expected branch: `docs/contest-submission-package`

## Next recommended task

Merge the contest submission package when checks pass. After merge, the remaining near-term work is human review of IP commitment, final product description wording, and whether optional video is required.

-## Status Update (2026-04-20)
-
-**MVP Audit Complete**: Comprehensive gap analysis identified 27 actionable issues (8 completed, 19 pending).
-
-**Critical Blockers Discovered**:
-1. **T009: Marketplace Import** - Button shows success but doesn't import pack (FAKE PLACEHOLDER)
-2. **T010: Assessment Feedback** - Lacks detailed topic breakdown and learning recommendations
-3. **T018: Vietnamese Prompts** - All LLM responses still English despite UI translation
-4. **T028: Rate Limiting** - API unprotected against abuse/DoS
-
-**Next Immediate Actions**:
-1. Create GitHub issues from TASK_REGISTRY.json templates (P1 tasks)
-2. Start Feature Pod: T009 Marketplace Import Implementation (blocking contest demo)
-3. Parallel: T018 Vietnamese Prompts, T022 Error Boundaries, T028 Rate Limiting
-4. Update daily log when starting each pod
-
-**Status**: Ready for Phase 1 (Critical Path) execution. Phase 1 target: 2 weeks to complete 6 P1 tasks (~20 hours total).

## Active queue

**UPDATED**: Continuing MVP gap fixes after completion of Feature Pack 3 merge.

- Previous: Contest submission package merged
- Current: MVP gap analysis audit completed (see `ai_first/MVP_GAP_ANALYSIS.md`)
- Focus: Phase 1 critical path fixes (T009, T010, T018, T022, T028)
- Active task packet: Will be created for T009 Marketplace Import (blocking item)
- Expected branch: `pod-a/marketplace-pack-import`

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
| T009: Marketplace Import | Not Started | 4 | YES | ASAP |
| T010: Assessment Feedback | Not Started | 6 | YES | After T009 |
| T011: KB Context Badges | Not Started | 2 | NO | Parallel |
| T018: Vietnamese Prompts | Not Started | 4 | YES | Parallel |
| T022: Error Boundaries | Not Started | 2 | NO | Parallel |
| T028: Rate Limiting | Not Started | 2 | YES | Parallel |

**Resources**: See `ai_first/TASK_REGISTRY.json` (full task list with effort estimates) and `ai_first/MVP_GAP_ANALYSIS.md` (detailed audit with risk assessment).
