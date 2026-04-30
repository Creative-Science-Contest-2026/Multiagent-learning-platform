# 2026-04-30 Teacher Dashboard Refresh

- Task ID: `UI_TEACHER_DASHBOARD_REFRESH`
- Commit tag: `UI-TDASH`
- Branch: `fix/teacher-dashboard-refresh`
- Worktree: `.worktrees/fix-teacher-dashboard-refresh`
- Status: `in_progress`

## Goal

Make the teacher dashboard read clearly for non-technical Vietnamese teachers by rewriting the copy in simpler classroom language and reorganizing the screen into a tighter, more obvious review flow.

## User-visible outcome

- The dashboard headline and summary area explain what the teacher should look at first.
- Student insight cards read as one connected story instead of three unrelated technical columns.
- English leakage and machine-style labels on the main dashboard are replaced with simpler Vietnamese wording.
- Secondary analytics remain available, but they no longer compete with the core teacher decision flow.

## Owned files

- `web/app/(workspace)/dashboard/page.tsx`
- `web/components/dashboard/TeacherInsightPanel.tsx`
- `web/components/dashboard/StudentInsightCard.tsx`
- `web/components/dashboard/SmallGroupInsightCard.tsx`
- `web/components/dashboard/dashboard-presenters.ts`
- `web/tests/teacher-dashboard-copy.test.ts`
- `web/tests/contest-terminology.test.ts`
- `web/locales/en/app.json`
- `web/locales/vi/app.json`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-teacher-dashboard-refresh.md`
- `docs/superpowers/specs/2026-04-30-teacher-dashboard-refresh-design.md`
- `docs/superpowers/plans/2026-04-30-teacher-dashboard-refresh.md`
- `docs/superpowers/pr-notes/2026-04-30-teacher-dashboard-refresh.md`

## Do-not-touch

- `deeptutor/`
- dashboard child routes under `web/app/(workspace)/dashboard/**` other than the main `page.tsx`
- `web/components/dashboard/*Composer.tsx`
- `web/lib/dashboard-api.ts` unless a pure frontend type helper is strictly required
- lockfiles and generated files

## Required code reading

- `web/app/(workspace)/dashboard/page.tsx`
- `web/components/dashboard/TeacherInsightPanel.tsx`
- `web/components/dashboard/StudentInsightCard.tsx`
- `web/components/dashboard/SmallGroupInsightCard.tsx`
- `web/lib/dashboard-api.ts`
- `web/locales/vi/app.json`

## Design before implementation

### Current behavior

- The dashboard has the right data, but the reading order is unclear.
- The first screen mixes summary cards, teacher insights, filters, metrics, and recent activity with similar visual weight.
- Several labels are still English or technical enough that non-technical teachers have to decode what the product means.
- The student insight card spreads one story across three equal panels, making the recommendation feel disconnected from the observed evidence.

### Intended behavior change

- The screen should tell the teacher what to review first, why it matters, and what action is suggested.
- The top area should answer three questions quickly:
  - what needs attention now;
  - which topic needs support;
  - what the class is already doing well.
- The student insight card should read like a guided narrative:
  - what the system saw;
  - what it thinks that means;
  - what the teacher may want to do next.
- Lower-priority analytics and history should stay available but move below the main decision-making surfaces.

### Candidate approaches

1. **Copy-only cleanup**
   - Pros: fastest, lowest risk.
   - Cons: does not solve the unclear reading order or disconnected card structure.

2. **Bounded copy + layout refresh on the existing dashboard surfaces**
   - Pros: fixes the main usability problems without touching API contracts or child routes.
   - Cons: requires coordinated edits across the dashboard page, insight panel, and student card.

3. **Split the dashboard into multiple tabs**
   - Pros: could reduce density.
   - Cons: adds navigation overhead and widens scope beyond a bounded refresh.

### Chosen approach

- Use **Approach 2**.
- Keep all backend contracts intact and improve only the frontend presentation layer, term mapping, and reading order.

### Expected impact surface

- Likely change:
  - `web/app/(workspace)/dashboard/page.tsx`
  - `web/components/dashboard/TeacherInsightPanel.tsx`
  - `web/components/dashboard/StudentInsightCard.tsx`
  - locale entries used by the refreshed dashboard
  - a small pure helper for teacher-facing label formatting
- Reviewed but expected unchanged:
  - dashboard API fetchers and backend payloads
  - child dashboard pages
  - composer form components and their submit behavior

### Validation paths

- Main dashboard first viewport clearly communicates teacher priority and next review step.
- Core teacher insight card content is mostly Vietnamese and non-technical.
- Recent activity, filters, and supporting metrics still work and remain readable.
- No dashboard child route or API contract changes are required.

## Acceptance criteria

- The first screen no longer feels like a stack of disconnected cards.
- The main dashboard uses simpler Vietnamese classroom language for its primary labels.
- Student insight cards visually connect evidence, interpretation, and suggested action.
- Supporting analytics are still present but visually secondary.

## Validation

- `cd web && node --test tests/contest-terminology.test.ts tests/teacher-dashboard-copy.test.ts`
- `cd web && npx eslint "app/(workspace)/dashboard/page.tsx" "components/dashboard/TeacherInsightPanel.tsx" "components/dashboard/StudentInsightCard.tsx" "components/dashboard/dashboard-presenters.ts"`
- `cd web && npm run build`
- `git diff --check`

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` is expected to remain unchanged because this lane refines a bounded presentation layer, not the system architecture or route graph.
