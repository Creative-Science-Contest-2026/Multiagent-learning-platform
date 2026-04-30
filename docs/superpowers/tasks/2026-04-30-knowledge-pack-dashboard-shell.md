# Task Packet: Knowledge Pack Dashboard Shell

- Task ID: `UI_KNOWLEDGE_PACK_DASHBOARD_SHELL`
- Commit tag: `UI-KNOWLEDGE-SHELL`
- Date: 2026-04-30
- Branch: `fix/knowledge-pack-dashboard-shell`
- Worktree: `.worktrees/fix-knowledge-pack-dashboard-shell`
- Status: Proposed

## Objective

Refactor the `Gói kiến thức` page into a two-column business workflow where the wizard lives on the left, ingest status lives on the right, and existing-pack management sits below as a separate layer.

## User-Approved Scope

- keep the current route
- preserve the three-step wizard concept
- strengthen the stepper and form layout
- make ingest status a first-class companion panel
- move existing-pack management into a separate lower section
- normalize status/badge treatment and reduce dense text

## Owned Files

- `web/app/(utility)/knowledge/page.tsx`
- extracted Knowledge-page UI subcomponents/helpers if created during refactor
- `web/locales/vi/app.json`
- `web/locales/en/app.json`
- `web/tests/contest-vietnamese-coverage.test.ts`
- any focused knowledge-page shell test added for the new layout
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-knowledge-pack-dashboard-shell.md`
- `docs/superpowers/specs/2026-04-30-knowledge-pack-dashboard-shell-design.md`
- `docs/superpowers/plans/2026-04-30-knowledge-pack-dashboard-shell.md`
- `docs/superpowers/pr-notes/2026-04-30-knowledge-pack-dashboard-shell.md`

## Do-Not-Touch

- unrelated `/playground` and tutor runtime lanes
- teacher dashboard runtime files
- backend ingestion logic unless the UI cannot render required status data without a bounded contract adjustment
- lockfiles unless dependency changes are required

## Design before implementation

- Runtime behavior change: yes
- Approved spec:
  - `docs/superpowers/specs/2026-04-30-knowledge-pack-dashboard-shell-design.md`
- Current behavior:
  - wizard, ingest state, and pack list are mixed in one long vertical flow
- Intended behavior change:
  - two-column create flow with separate bottom management section
- Candidate approach A:
  - spacing/copy cleanup only
- Candidate approach B:
  - left wizard, right ingest panel, lower management section
- Chosen approach and reason:
  - approach B; it fixes scanning order and task clarity without a route split

## Required code reading

- Entry points/handlers to inspect:
  - `web/app/(utility)/knowledge/page.tsx`
- Primary logic/service/use-case modules to inspect:
  - any extracted FE upload/index state helpers already used by the page
- Shared contracts/schemas/types to inspect:
  - knowledge-pack metadata fields
  - pack progress/status payloads
- Adjacent or reused flows to inspect:
  - current wizard step states
  - current pack-card/table management presentation
- Existing tests to inspect:
  - `web/tests/contest-vietnamese-coverage.test.ts`
  - any existing knowledge-page shell/source tests

## Impact surface and stop conditions

- Expected affected areas:
  - page layout
  - stepper treatment
  - difficulty control
  - ingest status panel
  - existing-pack management view
- Files/modules likely to change:
  - knowledge page
  - extracted FE subcomponents/helpers
  - locale files
- Files/modules that must be reviewed even if they remain unchanged:
  - backend ingestion progress contracts
  - notebook/runtime seams already hidden from visible FE
- Minimum validation paths before the task can stop:
  - stepper reads as real progress UI
  - `Mức độ khó` reads as a clickable segmented control
  - ingest status sits beside the wizard, not buried below it
  - existing-pack list is visually separated from the create flow
- What would count as a shallow fix for this task:
  - copy-only cleanup while keeping the same long stacked page structure

## Acceptance criteria

- the create flow is visually dominant over the management list
- the page reads as `create/edit now` first, `manage existing` second
- the status panel gives immediate ingest feedback
- the existing-pack list is easier to scan and action

## Required tests

- focused FE tests for wizard shell labels and layout assumptions where practical
- targeted eslint on touched FE files
- `cd web && npm run build`

## Manual verification

- open the page on desktop and confirm the left-right hierarchy is obvious
- confirm ingest states feel like a live companion surface
- confirm the lower management section no longer interrupts the create flow

## Parallel-work notes

- This task should begin only after the business-shell lane is either merged or explicitly declared non-blocking.
- Use a separate worktree from `origin/main` and record the lane in `ai_first/ACTIVE_ASSIGNMENTS.md`.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` likely does not need an update unless the screen’s role in the documented product flow changes materially.
