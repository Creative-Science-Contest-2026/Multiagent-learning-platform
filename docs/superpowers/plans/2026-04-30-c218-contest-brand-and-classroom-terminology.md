# C218 Contest Brand And Classroom Terminology Plan

## Scope

Bounded contest-path terminology pass only. No routing, behavior, API, or repo-wide brand changes.

## Task 1

Add lane tracking and focused copy-validation coverage.

- Keep `ai_first/ACTIVE_ASSIGNMENTS.md`, `ai_first/TASK_REGISTRY.json`, and `ai_first/daily/2026-04-30.md` aligned with the live lane.
- Add a focused terminology regression test for the contest-path copy keys used in the sidebar and `/agents`.

## Task 2

Implement the contest-path wording sweep.

- Update `SidebarShell.tsx` so the visible nav labels read `Knowledge Packs`, `Teacher dashboard`, and `Class tutor` while keeping `DeepTutor` intact in the header.
- Update `/agents` visible tabs, helper text, and empty states to classroom-first wording.
- Update `Knowledge` header copy so the page title and helper text match the contest-path language.
- Update the matching `en` and `vi` locale keys without widening into a repo-wide rename.

## Task 3

Validate and prepare the PR.

- Run the packet validation commands plus the new terminology test.
- Record the lane in the daily log.
- Write the PR architecture note with Mermaid before commit and PR creation.
