# 2026-04-30 C217 Teacher Cockpit Default Entry

- Task ID: `C217_TEACHER_COCKPIT_DEFAULT_ENTRY`
- Commit tag: `C217`
- Branch: `fix/teacher-cockpit-default-entry`
- Worktree: `.worktrees/teacher-cockpit-default-entry`
- Status: `pending`

## Goal

Replace the generic chat-first workspace landing with a teacher-first cockpit that foregrounds classroom setup, assessment, tutoring context, and students needing attention before broad multi-tool exploration.

## User-visible outcome

- Opening the main workspace no longer feels like entering a generic AI chat app.
- Teachers land on a contest-first cockpit that points them toward Knowledge Pack setup, tutor setup, assessment, and dashboard follow-up.
- Free-form chat and inherited tool modes remain available only as secondary paths, not the default contest story.

## Owned files

- `web/app/(workspace)/page.tsx`
- `web/app/(workspace)/dashboard/page.tsx`
- `web/components/sidebar/SidebarShell.tsx` only if the landing or highlighted primary route must stay aligned with the new entry
- `web/components/contest/`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-c217-teacher-cockpit-default-entry.md`
- `docs/superpowers/pr-notes/2026-04-30-c217-teacher-cockpit-default-entry.md`

## Do-not-touch

- `web/locales/`
- `deeptutor/`
- `web/app/(workspace)/agents/page.tsx`
- `web/app/(workspace)/agents/[botId]/chat/page.tsx`
- `web/app/(utility)/knowledge/page.tsx`
- `web/app/(utility)/marketplace/page.tsx`
- `web/app/(workspace)/guide/`
- `web/app/(workspace)/co-writer/`
- contest submission docs under `docs/contest/`
- lockfiles and generated files

## Required code reading

- `web/app/(workspace)/page.tsx`
- `web/app/(workspace)/dashboard/page.tsx`
- `web/components/sidebar/SidebarShell.tsx`
- `web/components/contest/CoreLoopVisibilityStrip.tsx`

## Design before implementation

### Current behavior

- `/` opens the broad DeepTutor multi-capability workspace with chat, capability pickers, tool toggles, research modes, visualization modes, notebook hooks, and session history.
- The current page is powerful, but its first impression is a generic AI workspace rather than a teacher-facing classroom product.
- Dashboard already carries the strongest teacher-first framing, but it is not the default landing experience.

### Intended behavior change

- The default workspace entry should present a teacher cockpit or teacher-first redirect that centers the contest loop:
  - prepare classroom context;
  - configure the class tutor;
  - draft or review assessment activity;
  - inspect diagnosis and next intervention.
- The landing should reduce cognitive load and communicate one product story before exposing the broader tool surface.

### Candidate approaches

1. **Hard redirect from `/` to `/dashboard`**
   - Pros: smallest change, minimal new UI.
   - Cons: loses the chance to create a dedicated teacher-cockpit summary and may overload the dashboard with two jobs.

2. **Convert `/` into a bounded teacher cockpit that links into existing Knowledge, `/agents`, assessment flow, and Dashboard**
   - Pros: strongest first impression, preserves the contest narrative, avoids overloading one existing page with every concern.
   - Cons: larger bounded frontend change than a redirect.

### Chosen approach

- Prefer **Approach 2** if it can stay inside the owned files and existing data contracts.
- Fall back to **Approach 1** only if the cockpit would require new APIs, localization expansion, or broader page-family edits.

### Expected impact surface

- Likely change:
  - `web/app/(workspace)/page.tsx`
  - one or more bounded shared components under `web/components/contest/`
  - possibly `web/app/(workspace)/dashboard/page.tsx` if the new cockpit reuses or extracts an existing teacher-summary block
- Reviewed but expected unchanged:
  - `web/app/(workspace)/agents/page.tsx`
  - `web/app/(utility)/knowledge/page.tsx`
  - route implementations for co-writer, guide, memory, and marketplace
  - backend data providers and API clients

### Validation paths

- Main workspace opens into the teacher-first entry.
- Knowledge, `/agents`, dashboard, and any retained chat path are still reachable.
- No existing route breaks from the changed landing.
- Contest loop framing remains visible on the landing or immediate next step.

## Execution notes

- This is a runtime-facing frontend task. Read the brainstorming skill before implementation, then stay within the design above or refine it in-place without widening scope.
- Do not turn this task into a product rename or localization sweep; that belongs to `C218`.
- Do not rebuild backend contracts or add new endpoints for the cockpit.
- Prefer extracting one small shared contest component over duplicating large dashboard or chat sections.
- If the cleanest cockpit needs new localized copy keys, stop and convert that requirement into `C218` rather than widening here.

## Acceptance criteria

- `/` no longer defaults to the generic multi-capability chat workspace for the contest path.
- The new default entry clearly points to teacher setup, assessment, tutor, and dashboard follow-up.
- Existing core contest routes remain reachable without regression.
- No backend or API contract changes are required.

## Validation

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `git diff --check`
- `cd web && npx eslint "app/(workspace)/page.tsx" "app/(workspace)/dashboard/page.tsx" "components/sidebar/SidebarShell.tsx" components/contest/*.tsx`
- `cd web && npm run build`

## Manual verification

- Open `/` and confirm the first read is teacher-first, not tool-first.
- From the landing, navigate to Knowledge, `/agents`, and Dashboard without dead ends.
- Confirm any retained path to the old broad chat workspace is secondary, intentional, and still functional.

## Parallel-work notes

- This packet assumes `C216` has already clarified the shell hierarchy or that the worker will adapt to any shell changes already merged.
- Do not widen into the full brand rename or Vietnamese terminology pass from `C218`.
- If the cockpit needs contest metrics, stories, or demo-proof callouts beyond existing surfaces, split that into `C219` instead of widening this runtime task.

## PR architecture note

- Must include Mermaid diagram.
- Update `ai_first/architecture/MAIN_SYSTEM_MAP.md` only if the default user entry flow materially changes beyond a bounded UI redirect/cockpit layer.

## Handoff

- The next expected follow-up after this packet is `C218_CONTEST_BRAND_AND_CLASSROOM_TERMINOLOGY`, unless the worker discovers the cockpit still needs only docs-side narrative support from `C219`.
