# C212 Core Loop Visibility Polish Design

Date: 2026-04-28
Status: Approved by execution assumption
Task: `C212_CORE_LOOP_VISIBILITY_POLISH`

## Goal

Make the contest loop `Knowledge Pack -> Assessment -> Tutor -> Diagnosis -> Intervention` more visible across the existing product surfaces without redesigning the app or changing submission claims.

## Assumption

Because the user explicitly asked to continue without more questions, this design assumes the safest bounded Phase 2 option:

- emphasize the loop with inline status labels on existing screens;
- do not add a new cross-app wizard, route, or persistent global shell;
- do not rewrite Session A or Session B submission docs from this lane.

## Scope

This polish is limited to four contest-facing surfaces already central to the demo path:

1. `web/app/(utility)/knowledge/page.tsx`
2. `web/app/(workspace)/dashboard/assessments/[sessionId]/page.tsx`
3. `web/app/(workspace)/agents/[botId]/chat/page.tsx`
4. `web/app/(workspace)/dashboard/page.tsx`

Plus one new shared component under `web/components/`.

## Non-goals

- no new product claims;
- no new API or backend logic;
- no route structure changes;
- no large visual redesign;
- no contest-doc wording edits from this lane;
- no screenshot or evidence refresh inside this PR.

## UX approach

Add one reusable “core loop visibility” strip that:

- lists the five contest steps in order;
- highlights the current step on the current screen;
- optionally shows which step comes next;
- uses the existing card/border/muted styling language so the polish looks native to the repo;
- wraps cleanly on mobile instead of forcing a long horizontal scroller.

## Screen mapping

### Knowledge page

- Current step: `Knowledge Pack`
- Purpose: establish the teacher-owned source of truth
- Placement: inside the top page header region, before the rest of the management UI

### Assessment review page

- Current step: `Assessment`
- Purpose: show that the teacher is reviewing the second step in the same contest loop
- Placement: directly below the page header and above the “Next Steps / Knowledge Pack / Overall Score” summary cards

### Tutor chat page

- Current step: `Tutor`
- Purpose: make the tutoring stage legible even in a minimal chat shell
- Placement: below the tutor header and above the message list

### Dashboard page

- Current step: `Diagnosis`
- Secondary callout: `Intervention` as the next teacher-facing move
- Purpose: show the dashboard as the teacher action surface around the final two loop stages
- Placement: inside the hero header card above the existing workflow summary

## Component contract

Create a shared component that accepts:

- `currentStep`
- optional `nextStep`
- optional `compact`
- optional short screen-specific helper text

The component should render:

- a small uppercase contest-loop label;
- a short helper sentence;
- five step pills with active/inactive/next styling.

## Acceptance criteria

- A teacher or judge can identify the current contest-loop step within a few seconds on each touched screen.
- The loop wording stays exactly aligned with Session A: `Knowledge Pack -> Assessment -> Tutor -> Diagnosis -> Intervention`.
- The dashboard still reads as a teacher action surface, not as an autonomous final judgment engine.
- The polish remains mobile-safe and visually consistent with the existing UI.

## Validation plan

- run targeted lint on touched frontend files;
- run a production frontend build;
- verify no TypeScript or formatting regressions are introduced.
