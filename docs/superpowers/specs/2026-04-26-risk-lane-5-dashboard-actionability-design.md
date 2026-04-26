# Risk Lane 5 Dashboard Actionability Design

## Metadata

- Date: 2026-04-26
- Task ID: `R5_DASHBOARD_ACTIONABILITY`
- Commit tag: `R5`
- Branch: `pod-a/dashboard-actionability`
- Scope: teacher dashboard actionability hardening for contest review and classroom-legibility

## Problem

The dashboard already shows `Observed`, `Inferred`, and `Recommended Action`, but the current cards still leave room for the attack that the system "looks smart without telling a teacher what to do next." The gap is not missing analytics. The gap is that the recommendation layer needs to read like a concrete teacher move anchored to visible evidence.

## Goal

Make the teacher dashboard defendable as a decision aid, not just an insight surface, by tightening the UI and demo artifacts around concrete next steps for both individual students and small groups.

## Non-Goals

- No redesign of the dashboard layout.
- No change to diagnosis semantics, scoring, or confidence logic.
- No new runtime-policy or agent-spec behavior.
- No new backend recommendation engine unless an existing payload gap blocks the UI outright.

## Recommended Approach

Use a bounded `UI-copy + story structure` approach:

1. Keep the current dashboard layout and data hierarchy.
2. Reframe student and small-group cards around `Teacher move` and `Why this move`.
3. Mirror the same language in the student detail view so overview and drill-down tell the same story.
4. Add 2-3 concise contest story artifacts that reuse the same wording as the UI.

This is the smallest change that makes the dashboard feel classroom-actionable without opening a new product lane.

## Information Hierarchy

### Student Insight Card

Each student card keeps the evidence-first order, but the recommendation block becomes explicitly teacher-facing:

1. `Observed`
   - dominant topic
   - misses / latency / support signal
2. `Teacher move`
   - one short directive describing the next classroom action
   - examples:
     - reteach one prerequisite with one scaffolded example
     - lower the next check difficulty
     - ask the student to explain one reasoning step before another hint
3. `Why this move`
   - one short explanation grounded in the current observed and inferred payload
   - this is not a new diagnosis claim; it is a restatement of current evidence in teacher language

### Small-Group Insight Card

Each small-group card becomes a mini intervention plan:

1. `Shared signal`
   - topic
   - diagnosis type
2. `Teacher move`
   - one concrete group action
   - examples:
     - pull these students into one remediation mini-group
     - revisit the same misconception together before the next quiz
3. `Why these students belong together`
   - short explanation based on shared signal
   - visible student list kept as lightweight trace

### Student Detail View

The detail page should not introduce a different narrative. It should extend the overview:

1. `Observed`
2. `Teacher move`
3. `Why this move`

The wording should stay aligned with the overview cards so a reviewer can move between screens without re-learning the dashboard logic.

## File-Level Change Set

### UI

- `web/components/dashboard/TeacherInsightPanel.tsx`
  - tighten section intro copy so the panel promises concrete teacher moves
- `web/components/dashboard/StudentInsightCard.tsx`
  - rename action framing from generic recommendation to teacher move
  - add one short evidence-backed "why this move" line
- `web/components/dashboard/SmallGroupInsightCard.tsx`
  - add reason-for-grouping copy and more explicit group action phrasing
- `web/components/dashboard/StudentInsightDetail.tsx`
  - mirror the same teacher-move hierarchy used in overview
- `web/app/(workspace)/dashboard/page.tsx`
  - only bounded copy-level support if the overview hero or labels need to reflect the new framing
- `web/app/(workspace)/dashboard/student/page.tsx`
  - only bounded copy-level support if student detail needs matching labels

### Docs / Contest Support

- `docs/contest/`
  - add or tighten 2-3 dashboard story artifacts for reviewer/demo use
- `ai_first/competition/`
  - reuse the same wording for contest defense and presenter notes

## Data Contract Rules

- Keep the existing hierarchy:
  - `Observed`
  - `Inferred`
  - `Recommended Action`
- UI may rephrase recommendation output as a teacher move, but must not invent new diagnosis semantics.
- If a recommendation lacks enough evidence to become a concrete teacher move, the UI should stay explicit and narrow rather than fabricate specificity.

## Acceptance Criteria

1. At least 2-3 student or group stories are visible either in UI or directly supported by contest artifacts.
2. Each story names a concrete teacher move, not only an action category.
3. Each teacher move has a visible reason anchored to current evidence.
4. Small-group cards can answer both:
   - why these students are grouped
   - what the teacher should do with that group next
5. The overview and student detail surfaces use compatible wording.

## Manual Verification

Walk through at least three examples:

1. one individual student needing gentler scaffolding
2. one individual student needing stronger reasoning accountability
3. one small group sharing the same misconception

For each example, a non-technical reviewer should be able to answer:

- what happened
- what the system suggests the teacher do next
- why the system suggests that move

## Testing

- focused frontend lint for touched dashboard files
- `git diff --check`

## Risks And Boundaries

- The largest risk is over-writing the cards with generic educational prose. Keep each new line tied to current payload fields.
- The second risk is accidentally changing diagnosis meaning in the UI. The lane must stay presentation-first.
- If the existing payload cannot support one credible "why this move" sentence, stop and document the contract gap instead of inventing logic.

## Architecture Note Requirement

The PR must include a note under `docs/superpowers/pr-notes/` with a Mermaid diagram. `ai_first/architecture/MAIN_SYSTEM_MAP.md` should remain unchanged unless the dashboard workflow itself changes materially.
