# Task Packet: Teacher Dashboard Decision Flow

- Task ID: `UI_TEACHER_DASHBOARD_DECISION_FLOW`
- Commit tag: `UI-TEACHER-DASH`
- Date: 2026-04-30
- Branch: `fix/teacher-dashboard-decision-flow`
- Worktree: `.worktrees/fix-teacher-dashboard-decision-flow`
- Status: Proposed

## Objective

Refactor the `Bảng điều khiển giáo viên` screen into a decision-first dashboard with a strong intervention layer, compact KPI row, supporting topic cards, and a calmer lower activity/history section.

## User-Approved Scope

- top KPI summary row
- left intervention column for students needing attention now
- right supporting column for topics and group recommendations
- lower trend/filter/activity layer
- remove raw/debug/unfinished English technical strings from the default teacher-facing UI

## Owned Files

- `web/app/(workspace)/dashboard/page.tsx`
- `web/components/dashboard/TeacherInsightPanel.tsx`
- `web/components/dashboard/StudentInsightCard.tsx`
- `web/components/dashboard/SmallGroupInsightCard.tsx`
- `web/components/dashboard/dashboard-presenters.ts`
- `web/locales/vi/app.json`
- `web/locales/en/app.json`
- `web/tests/teacher-dashboard-copy.test.ts`
- `web/tests/teacher-dashboard-decision-flow.test.ts`
- any focused dashboard shell/decision-flow tests added during implementation
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-teacher-dashboard-decision-flow.md`
- `docs/superpowers/specs/2026-04-30-teacher-dashboard-decision-flow-design.md`
- `docs/superpowers/plans/2026-04-30-teacher-dashboard-decision-flow.md`
- `docs/superpowers/pr-notes/2026-04-30-teacher-dashboard-decision-flow.md`

## Do-Not-Touch

- backend dashboard/recommendation services unless a bounded presenter-contract fix is absolutely required
- knowledge-pack page runtime files
- tutor chat routes
- lockfiles unless dependency changes are required

## Design before implementation

- Runtime behavior change: yes
- Approved spec:
  - `docs/superpowers/specs/2026-04-30-teacher-dashboard-decision-flow-design.md`
- Current behavior:
  - the dashboard mixes urgent intervention, metrics, filters, history, and debug-style strings in the same reading layer
- Intended behavior change:
  - intervention-first teacher dashboard with strict display rules for non-technical users
- Candidate approach A:
  - copy simplification only
- Candidate approach B:
  - four-zone decision dashboard with presenter-based teacher-friendly mapping
- Chosen approach and reason:
  - approach B; it changes the scan order and hides technical clutter without requiring new routes

## Required code reading

- Entry points/handlers to inspect:
  - `web/app/(workspace)/dashboard/page.tsx`
- Primary logic/service/use-case modules to inspect:
  - `web/components/dashboard/TeacherInsightPanel.tsx`
  - `web/components/dashboard/StudentInsightCard.tsx`
  - `web/components/dashboard/SmallGroupInsightCard.tsx`
  - any existing dashboard presenter/helper layer
- Shared contracts/schemas/types to inspect:
  - dashboard API response fields that currently feed names, topics, confidence, and recommendation text
- Adjacent or reused flows to inspect:
  - recent activity/history presentation
  - any current KPI metric surfaces
- Existing tests to inspect:
  - `web/tests/teacher-dashboard-copy.test.ts`
  - `web/tests/contest-terminology.test.ts` if new Vietnamese terminology needs protection

## Impact surface and stop conditions

- Expected affected areas:
  - KPI row
  - intervention card layout
  - topic/group summary column
  - history/filter presentation
  - presenter mapping for teacher-friendly language
- Files/modules likely to change:
  - dashboard page
  - teacher insight panel
  - student card
  - small-group card
  - dashboard presenters
  - locale and copy tests
- Files/modules that must be reviewed even if they remain unchanged:
  - backend dashboard API contracts
  - group recommendation surfaces
  - any existing detail/disclosure path for system/debug content
- Minimum validation paths before the task can stop:
  - first screenful clearly prioritizes intervention
  - student cards are scannable and action-oriented
  - raw/debug/unfinished English strings are gone from default UI
  - history and filters are still accessible but visually secondary
- What would count as a shallow fix for this task:
  - translating strings without restructuring the information hierarchy or hiding debug/raw content

## Acceptance criteria

- teachers can see urgent decisions first
- student cards emphasize next action instead of technical detail
- topic and group summaries support the main intervention layer without overwhelming it
- debug/raw variables are not shown by default

## Required tests

- focused dashboard presenter/copy tests
- targeted eslint on touched dashboard files
- `cd web && npm run build`

## Manual verification

- open the dashboard and confirm the first scan surface is `what do I need to do now?`
- confirm card actions feel primary and grouped
- confirm system detail is hidden or demoted behind optional disclosure

## Parallel-work notes

- This task should begin only after the business-shell lane is either merged or explicitly declared non-blocking.
- Use a dedicated worktree from `origin/main` and record the lane in `ai_first/ACTIVE_ASSIGNMENTS.md`.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` likely does not need an update unless the dashboard’s role in the documented teacher workflow changes materially.
