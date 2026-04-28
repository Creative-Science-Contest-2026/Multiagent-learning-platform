# Feature Pod Task: Browser Recapture After Phase 2 Polish

Task ID: `OPS_BROWSER_RECAPTURE_AFTER_PHASE2`
Commit tag: `OPS-BROWSER`
Owner: Session-specific
Branch: `docs/post-phase2-browser-recapture`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Recapture the browser screenshot evidence that is now stale after the merged Phase 2 polish train (`#214`, `#215`, `#216`, `#217`) so the contest package can move the affected rows from `Stale` back to `Current`.

## User-visible outcome

- Contest docs can truthfully mark the current Knowledge, Tutor, Dashboard, and `/agents` screenshot rows as `Current`.
- Reviewers see the latest teacher-controlled adaptive wording and loop framing rather than pre-polish browser captures.
- The contest package keeps command-backed proof and browser-backed proof aligned without widening claims.

## Owned files/modules

- `docs/contest/screenshots/*`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `docs/contest/VALIDATION_REPORT.md`
- `docs/contest/README.md`
- `docs/contest/SUBMISSION_PACKAGE.md`
- `docs/contest/DEMO_SCRIPT.md`
- `ai_first/evidence/screenshots.md`
- `ai_first/evidence/demo-script.md`
- `docs/superpowers/tasks/2026-04-28-browser-recapture-after-phase2.md`
- `docs/superpowers/pr-notes/*`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/NEXT_ACTIONS.md`
- `ai_first/CURRENT_STATE.md`
- `ai_first/daily/2026-04-28.md`

## Do-not-touch files/modules

- `deeptutor/services/`
- `deeptutor/api/routers/`
- `web/app/`
- `web/components/`
- `ai_first/AI_OPERATING_PROMPT.md` unless the browser-recapture workflow itself changes operating rules

## Evidence contract

- Reuse the latest command-backed smoke baseline from 2026-04-28 unless the local app must be restarted for capture confidence.
- Recapture only the rows that are currently stale:
  - Knowledge Pack metadata form
  - Knowledge Pack after reload
  - Tutor question and response
  - Dashboard overview
  - Dashboard recent activity
  - `/agents` structured authoring
  - `/agents` export action
- Assessment screenshot rows already remain `Current`; do not recapture them unless the UI changed again before capture.
- Only move `Stale` -> `Current` after new screenshots are produced, linked, and visually checked.

## Acceptance criteria

- Every stale screenshot row has a fresh artifact in `docs/contest/screenshots/`.
- Contest evidence docs reference the new capture date and capture lane.
- Hybrid `/agents` claims remain bounded to authoring/export proof plus the already-documented runtime-binding guardrail.
- This lane does not change product/runtime code.

## Required tests

- `rg -n "Stale|Current|browser recapture|Knowledge Pack|Tutor Agent|Dashboard|/agents|screenshots" docs/contest ai_first docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`

## Manual verification

- Open each new screenshot and confirm it matches the current merged UI.
- Confirm no private data or credentials appear in the captures.
- Confirm Knowledge and Tutor screenshots reflect the new loop framing from `#214` and `#215`.
- Confirm Dashboard screenshots reflect the new teacher-reviewed signals framing from `#214` and `#215`.
- Confirm `/agents` screenshots reflect the updated adaptive tutor wording from `#215`.

## Parallel-work notes

- This lane is docs/evidence-only and browser-heavy.
- If browser capture is unavailable, leave rows `Stale` and document the blocker explicitly instead of inventing artifacts.
- Do not “fix” UI or backend issues from this lane; capture the current merged behavior only.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` should remain unchanged.

## Handoff notes

- `#217` intentionally split command-backed freshness from browser-backed freshness; this lane is the follow-up that can restore the browser rows to `Current`.
- Start from `origin/main`, use demo-safe data, and only update screenshot dates after the fresh artifacts exist.
- 2026-04-28 execution note: local backend and frontend were started from `.worktrees/submission-close-c`, demo data was reset, a demo-safe `fraction-coach` spec pack was seeded for `/agents`, and the seven stale screenshot rows were freshly recaptured before doc statuses were moved back to `Current`.
