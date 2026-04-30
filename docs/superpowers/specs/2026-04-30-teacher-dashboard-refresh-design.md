# Teacher Dashboard Refresh Design

## Goal

Make the teacher dashboard easier for non-technical Vietnamese teachers to scan and act on without changing backend contracts or introducing new routes.

## Current behavior

- The dashboard mixes high-priority teacher decisions with secondary analytics and history.
- Primary dashboard copy still contains English phrases and technical wording.
- Student insight cards use three equal columns, so observed evidence, diagnosis, and teacher action do not read as one connected story.

## Intended behavior

- The top of the page should immediately answer:
  - điều gì cần giáo viên xem trước;
  - chủ đề nào cần hỗ trợ;
  - lớp đang làm tốt ở đâu.
- The teacher insight section should become the dominant middle layer of the page.
- Each student card should show a compact narrative from observed evidence to suggested classroom move.
- Supporting metrics, filters, and history should remain visible but move into a calmer lower layer.

## Approaches considered

### 1. Copy-only pass

- Smallest scope.
- Rejected because it would leave the page structure confusing.

### 2. Bounded presentation refresh on existing surfaces

- Reuses the current data and actions.
- Lets the page become clearer without widening into backend changes.
- Chosen approach.

### 3. Multi-tab dashboard

- Could reduce density.
- Rejected because it adds navigation and widens the runtime surface.

## Chosen approach

Refresh the existing dashboard in three layers:

1. **Priority summary**
   - Replace the current mixed hero with a simpler Vietnamese headline and three short summary blocks.
   - Emphasize one teacher-first priority statement above generic dashboard metrics.

2. **Teacher insight narrative**
   - Reframe the section title and supporting text in classroom language.
   - Redesign each student card so the suggested teacher action is the clearest object on the card, with observed evidence and system interpretation directly supporting it.
   - Convert raw technical strings from backend payloads into bounded, teacher-friendly Vietnamese labels in the presentation layer.

3. **Supporting follow-up**
   - Collapse redundant metric density by turning the current KPI spread into fewer summary cards.
   - Keep filters, recent activity, and Knowledge Pack activity below the teaching decision layer.

## Files and responsibilities

- `web/app/(workspace)/dashboard/page.tsx`
  - Reorders the page into priority summary, teacher insights, compact follow-up metrics, filters, and history.
- `web/components/dashboard/TeacherInsightPanel.tsx`
  - Renames and reframes the main teacher-review section.
- `web/components/dashboard/StudentInsightCard.tsx`
  - Changes the card layout and text hierarchy.
- `web/components/dashboard/dashboard-presenters.ts`
  - Centralizes teacher-facing wording for statuses, confidence labels, support levels, and recommendation labels.
- `web/locales/en/app.json`
  - Adds the bounded English fallback keys for the new dashboard text.
- `web/locales/vi/app.json`
  - Adds the bounded Vietnamese dashboard wording.
- `web/tests/teacher-dashboard-copy.test.ts`
  - Locks the new presenter mappings and priority-summary wording.

## Tests to add or update

- Add a focused node test for dashboard presenter helpers so the teacher-facing labels are verified before the UI is changed.
- Keep locale coverage aligned by extending the existing terminology test only where new bounded dashboard strings need protection.
- Run eslint on the changed dashboard files and a full `web` build.

## Impact surface review

- Reviewed and intentionally left unchanged:
  - `web/lib/dashboard-api.ts` data contracts
  - dashboard child routes
  - composer submit components
  - backend service logic
- Changed:
  - main dashboard presentation and teacher-facing display terms only
