# Feature Pod Task: Browser Recapture Refresh

Task ID: `OPS_BROWSER_RECAPTURE_REFRESH_20260430`
Commit tag: `OPS-BROWSER`
Owner: Session-specific
Branch: `docs/browser-recapture-refresh-20260430`
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Recapture the authoritative contest screenshot rows that are still marked stale after the later contest polish and differentiation merges so the judge-facing docs can move those rows back to `Current` only if fresh artifacts really exist.

## User-visible outcome

- Knowledge, Tutor, Dashboard, and `/agents` screenshot rows can honestly return to `Current`.
- The screenshot bundle reflects the current merged shell, cockpit, and classroom terminology state instead of earlier pre-follow-up UI.
- If recapture is not possible in the local environment, the blocker is documented without inventing evidence.

## Owned files/modules

- `docs/contest/screenshots/*`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `docs/contest/VALIDATION_REPORT.md`
- `docs/contest/README.md`
- `docs/contest/SUBMISSION_PACKAGE.md`
- `docs/contest/DEMO_SCRIPT.md`
- `ai_first/evidence/screenshots.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/NEXT_ACTIONS.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-browser-recapture-refresh.md`
- `docs/superpowers/pr-notes/*`

## Do-not-touch files/modules

- `deeptutor/services/`
- `deeptutor/api/routers/`
- `web/app/`
- `web/components/`
- lockfiles
- product/runtime code outside evidence capture support already present in the repo

## Evidence contract

- Reuse the current merged `main` product/runtime behavior exactly as-is.
- Refresh only the rows currently marked stale:
  - Knowledge Pack metadata form
  - Knowledge Pack after reload
  - Tutor question and response
  - Dashboard overview
  - Dashboard recent activity
  - `/agents` structured authoring
  - `/agents` export action
- Assessment screenshot rows stay unchanged unless they are discovered to be stale too.
- Move `Stale` to `Current` only after the new screenshot artifact exists, is visually checked, and is linked from the contest docs.

## Acceptance criteria

- Every currently stale browser row either has a fresh screenshot artifact and updated docs, or remains explicitly stale with a documented blocker.
- Screenshot dates, lane references, and notes align across contest docs and AI-first mirrors.
- `/agents` claims stay bounded to authoring/export proof and do not expand runtime claims.
- No product/runtime code is changed.

## Required tests

- `rg -n "Stale|Current|browser recapture|Knowledge Pack|Tutor|Dashboard|/agents|screenshots" docs/contest ai_first docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`

## Manual verification

- Open each fresh screenshot and confirm it matches the current merged UI.
- Confirm no private data or credentials appear in the captures.
- Confirm Knowledge, Tutor, Dashboard, and `/agents` screenshots reflect the current merged contest-facing shell and terminology.

## Parallel-work notes

- This lane is docs/evidence-only and should not edit runtime code.
- If browser capture is unavailable or the current environment cannot reproduce the demo-safe story, stop and document the blocker instead of fabricating screenshots.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` should remain unchanged.

## Handoff notes

- Start from `origin/main`.
- Use demo-safe `contest-demo-quadratics` data only.
- Keep command-backed proof and browser-backed proof aligned, but do not rewrite command-backed evidence dates unless the capture lane also reruns the bounded evidence helper intentionally.
