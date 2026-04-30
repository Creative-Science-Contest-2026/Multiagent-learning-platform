# C218 Contest Brand And Classroom Terminology Design

## Goal

Keep upstream `DeepTutor` attribution intact while making the primary contest path read like bounded classroom software instead of a generic agent workspace.

## Current behavior

- The sidebar header still shows `DeepTutor`, which is acceptable as an attribution-facing brand surface.
- The primary contest path still mixes classroom wording with generic labels such as `Knowledge`, `TutorBot`, `Bots`, `Profiles`, and `Souls`.
- `/agents` already behaves like class-tutor setup, but several visible labels still expose implementation-facing terms rather than teacher-facing wording.

## Intended behavior

- Preserve `DeepTutor` where it functions as attribution or a technical surface.
- Normalize the primary contest-path wording so the first read is classroom-first:
  - `Knowledge` becomes `Knowledge Packs`
  - `Dashboard` becomes `Teacher dashboard`
  - `TutorBot` becomes `Class tutor` where it is a visible contest-facing label
  - `/agents` tab and helper text favor teacher/classroom language over internal terms like `Bots` and `Souls`
- Keep routes, behavior, APIs, and upstream legal/doc surfaces unchanged.

## Candidate approaches

1. Locale-only sweep
   - Pros: smallest edit set.
   - Cons: misses shell labels defined in code and can leave `/agents` wording inconsistent.

2. Bounded contest-path sweep across shell, page headers, and matching locale keys
   - Pros: fully covers the first-read surfaces without turning into a repo-wide rename.
   - Cons: touches more files and needs care to avoid changing secondary technical flows.

## Chosen approach

Use approach 2. Limit the sweep to the owned files in the packet and keep `DeepTutor` intact in the sidebar header plus attribution-facing strings.

## Required codebase survey

- Entry points and shells:
  - `web/components/sidebar/SidebarShell.tsx`
- Primary contest-path pages:
  - `web/app/(workspace)/agents/page.tsx`
  - `web/app/(workspace)/dashboard/page.tsx`
  - `web/app/(utility)/knowledge/page.tsx`
- Shared wording sources:
  - `web/locales/en/app.json`
  - `web/locales/vi/app.json`
- Closest existing tests:
  - `web/tests/sidebar-nav-groups.test.ts`
  - no current contest-copy test, so add one for the terminology keys

## Expected impact surface

- Likely change:
  - `web/components/sidebar/SidebarShell.tsx`
  - `web/app/(workspace)/agents/page.tsx`
  - `web/app/(utility)/knowledge/page.tsx`
  - `web/locales/en/app.json`
  - `web/locales/vi/app.json`
  - `web/tests/contest-terminology.test.ts`
- Reviewed but expected unchanged:
  - `web/app/(workspace)/dashboard/page.tsx` because its current header already reads teacher-first
  - `web/app/(workspace)/page.tsx`
  - `web/app/(workspace)/guide/`
  - `web/app/(workspace)/co-writer/`
  - `web/app/(utility)/marketplace/page.tsx`
  - backend and API contracts

## Validation paths

- Shell/nav labels read classroom-first while `DeepTutor` remains visible as brand attribution.
- `/agents`, `Knowledge`, and `Dashboard` use consistent contest-path terminology.
- English and Vietnamese locale files stay valid JSON.
- Build still succeeds without route or runtime regressions.
