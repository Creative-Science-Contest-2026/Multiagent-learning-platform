# 2026-04-30 C220 Contest Layout Breakage Sweep

- Task ID: `C220_CONTEST_LAYOUT_BREAKAGE_SWEEP`
- Commit tag: `C220`
- Branch: `fix/contest-layout-breakage-sweep`
- Worktree: `.worktrees/contest-layout-breakage-sweep`
- Status: `in_progress`

## Goal

Fix the remaining broken responsive layouts on the teacher-first contest path so the product can survive judge-facing desktop and laptop widths without overlapping controls, clipped text, or collapsed columns.

## User-visible outcome

- `/agents` no longer shows overlapping action buttons, crushed center content, or unreadable right-rail summaries.
- The teacher cockpit, Knowledge, Marketplace, and Dashboard continue to read cleanly after the same responsive hardening pass.
- Longer Vietnamese strings fit inside the audited layouts instead of making the current breakage worse.

## Owned files

- `web/components/agents/SpecPackAuthoringTab.tsx`
- `web/app/(workspace)/agents/page.tsx`
- `web/components/contest/TeacherCockpit.tsx`
- `web/components/contest/CoreLoopVisibilityStrip.tsx`
- `web/app/(workspace)/dashboard/page.tsx`
- `web/app/(utility)/knowledge/page.tsx`
- `web/app/(utility)/marketplace/page.tsx` only if the same contest-path layout issue is confirmed there during the audit
- any tightly related shared frontend layout helper that is required to remove the breakage without widening scope
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-c220-contest-layout-breakage-sweep.md`
- `docs/superpowers/pr-notes/2026-04-30-c220-contest-layout-breakage-sweep.md`

## Do-not-touch

- `web/locales/en/app.json`
- `web/locales/vi/app.json`
- `deeptutor/`
- backend API routers and data contracts
- contest docs under `docs/contest/`
- repo-level attribution and license files
- lockfiles and generated files

## Required code reading

- `web/components/agents/SpecPackAuthoringTab.tsx`
- `web/app/(workspace)/agents/page.tsx`
- `web/components/contest/TeacherCockpit.tsx`
- `web/components/contest/CoreLoopVisibilityStrip.tsx`
- `web/app/(workspace)/dashboard/page.tsx`
- `web/app/(utility)/knowledge/page.tsx`
- `web/app/(utility)/marketplace/page.tsx` if the screen is part of the same responsive failure family
- the closest existing tests that cover these screens or related contest-path layout behavior

## Design before implementation

### Current behavior

- `/agents` currently uses a three-column authoring layout that collapses under real copy length and causes visible overlap between the center authoring controls and the right summary rail.
- The teacher cockpit and other contest-path pages still rely on desktop-biased grid assumptions that were acceptable with shorter English copy but become fragile once the UI is actually used in Vietnamese.
- The breakage is visible enough to undermine the teacher-first contest story even though the underlying features work.

### Intended behavior change

- The audited contest-path screens should stack or wrap gracefully at realistic laptop widths.
- Action rows should wrap instead of colliding.
- Long labels and summaries should clamp, shrink, or move below the primary content instead of pushing other panels off-screen.

### Candidate approaches

1. **Apply isolated CSS band-aids only where the screenshot is broken**
   - Pros: fastest path to the worst regression.
   - Cons: high risk of leaving the same structural problem on adjacent contest screens.

2. **Do one bounded contest-path responsive hardening sweep**
   - Pros: fixes the root layout assumptions across `/agents`, then verifies the same patterns on `/`, `Knowledge`, `Marketplace`, and `Dashboard`.
   - Cons: slightly larger frontend sweep.

### Chosen approach

- Prefer **Approach 2**.
- Keep it bounded to the contest path and solve the layout structurally with `min-w-0`, breakpoint restacking, rail wrapping, and overflow guards rather than page-specific hacks.

### Expected impact surface

- Likely change:
  - `web/components/agents/SpecPackAuthoringTab.tsx`
  - `web/app/(workspace)/agents/page.tsx`
  - `web/components/contest/TeacherCockpit.tsx`
  - possibly one or more of `web/app/(workspace)/dashboard/page.tsx`, `web/app/(utility)/knowledge/page.tsx`, and `web/app/(utility)/marketplace/page.tsx` if the same responsive pattern appears there
- Reviewed but expected unchanged:
  - route wiring and navigation targets
  - backend APIs
  - locale files and wording

### Validation paths

- `/agents`
- `/`
- `/knowledge`
- `/marketplace`
- `/dashboard`

## Execution notes

- This is a runtime-facing frontend task. Read the brainstorming skill before implementation, then keep the sweep inside the owned files above.
- Do not mix wording or localization work into this packet unless a tiny emergency label trim is required to stop a layout collision; broader Vietnamese cleanup belongs to `C221`.
- Do not add new APIs, routes, or data requirements.
- If a broken layout is found outside the contest path, stop and open a separate packet instead of widening this one.

## Acceptance criteria

- `/agents` no longer shows visible overlap, clipping, or unreadable collapsed columns on the main authoring flow.
- The teacher cockpit, Knowledge, Marketplace, and Dashboard pass the same responsive sanity check at the target viewport widths.
- No backend or route-contract changes are required.

## Validation

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `git diff --check`
- `cd web && npx eslint "components/agents/SpecPackAuthoringTab.tsx" "app/(workspace)/agents/page.tsx" "components/contest/TeacherCockpit.tsx" "components/contest/CoreLoopVisibilityStrip.tsx" "app/(workspace)/dashboard/page.tsx" "app/(utility)/knowledge/page.tsx" "app/(utility)/marketplace/page.tsx"`
- `cd web && npm run build`

## Manual verification

- Open `/agents` at the viewport widths that currently show breakage and confirm the three-column authoring flow remains readable.
- Open `/`, `/knowledge`, `/marketplace`, and `/dashboard` and confirm no new overlap or horizontal spill appears after the responsive hardening.

## Parallel-work notes

- Run this packet before `C221` because the Vietnamese pass will lengthen content and should not land on broken containers.
- Keep the lane strictly on layout and responsive behavior; wording changes belong to `C221`.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` is not expected to change because this lane adjusts presentation and responsive layout only.
