# 2026-04-30 C221 Contest Vietnamese Coverage Completion

- Task ID: `C221_CONTEST_VIETNAMESE_COVERAGE_COMPLETION`
- Commit tag: `C221`
- Branch: `fix/contest-vietnamese-coverage-completion`
- Worktree: `.worktrees/contest-vietnamese-coverage-completion`
- Status: `in_progress`

## Goal

Complete the remaining Vietnamese coverage on the primary contest path so the teacher-first demo no longer leaks English fallback copy on `/`, `/agents`, `Knowledge`, `Marketplace`, and `Dashboard`.

## User-visible outcome

- The teacher cockpit reads fully Vietnamese on the main flow instead of mixing English action descriptions into Vietnamese UI chrome.
- `/agents` no longer exposes English seed content, empty-state copy, or fallback summary labels in the spec-pack authoring flow.
- Knowledge, Marketplace, and Dashboard remain internally consistent in Vietnamese after the final localization pass.

## Owned files

- `web/components/contest/teacher-cockpit-content.ts`
- `web/components/contest/TeacherCockpit.tsx` only if localized key usage needs bounded cleanup
- `web/components/agents/SpecPackAuthoringTab.tsx`
- `web/app/(workspace)/agents/page.tsx`
- `web/app/(workspace)/dashboard/page.tsx`
- `web/app/(utility)/knowledge/page.tsx`
- `web/app/(utility)/marketplace/page.tsx` if the screen still shows contest-path English leakage during the audit
- `web/locales/en/app.json`
- `web/locales/vi/app.json`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-c221-contest-vietnamese-coverage-completion.md`
- `docs/superpowers/pr-notes/2026-04-30-c221-contest-vietnamese-coverage-completion.md`

## Do-not-touch

- `deeptutor/`
- backend API routers and data contracts
- route structure and navigation ownership from `C216` and `C217`
- contest docs under `docs/contest/`
- repo-level attribution and license files
- lockfiles and generated files

## Required code reading

- `web/components/contest/teacher-cockpit-content.ts`
- `web/components/contest/TeacherCockpit.tsx`
- `web/components/agents/SpecPackAuthoringTab.tsx`
- `web/app/(workspace)/agents/page.tsx`
- `web/app/(workspace)/dashboard/page.tsx`
- `web/app/(utility)/knowledge/page.tsx`
- `web/app/(utility)/marketplace/page.tsx` if the screen still shows contest-path English leakage
- `web/locales/en/app.json`
- `web/locales/vi/app.json`
- the closest existing contest terminology or localization tests

## Design before implementation

### Current behavior

- The teacher cockpit still depends on hard-coded English action strings that only partially map to existing locale keys.
- `/agents` spec-pack authoring seeds English markdown content and English fallback summaries directly in the component, so Vietnamese mode still leaks English even when surrounding labels are translated.
- The primary contest path therefore reads as half-localized rather than classroom-ready for a Vietnamese judge or teacher.

### Intended behavior change

- Vietnamese mode should render the primary contest-path copy fully in Vietnamese wherever the string is a teacher-facing label, helper, empty state, or seeded classroom guidance.
- Technical filenames, upstream product attribution, and repo/legal identifiers should remain unchanged where translating them would alter contracts or provenance.

### Candidate approaches

1. **Patch only the missing locale keys**
   - Pros: smaller diff.
   - Cons: leaves hard-coded English seed content and brittle exact-string fallbacks inside components.

2. **Do a bounded contest-path localization completion sweep**
   - Pros: closes both missing locale keys and hard-coded component fallbacks in one pass.
   - Cons: broader than a pure locale-file edit.

### Chosen approach

- Prefer **Approach 2**.
- Keep the sweep bounded to the contest path and teacher-facing copy only, while leaving technical filenames and legal attribution intact.

### Expected impact surface

- Likely change:
  - `web/components/contest/teacher-cockpit-content.ts`
  - `web/components/agents/SpecPackAuthoringTab.tsx`
  - `web/locales/en/app.json`
  - `web/locales/vi/app.json`
  - small bounded contest-path page usage sites if they still rely on unmatched exact-string keys
- Reviewed but expected unchanged:
  - route structure
  - backend APIs
  - non-contest technical/admin surfaces

### Validation paths

- `/`
- `/agents`
- `/knowledge`
- `/marketplace`
- `/dashboard`

## Execution notes

- This is a runtime-facing frontend task. Read the brainstorming skill before implementation, then stay inside the contest-path localization sweep.
- Run `C220` first unless the worker proves the current layout is already stable, because Vietnamese strings are generally longer and should not be added onto broken layouts.
- Preserve DeepTutor and Apache 2.0 attribution and do not translate raw markdown filenames or other contract-carrying identifiers unless a separate display label is introduced.
- If the sweep reveals broader repo-wide localization debt outside the contest path, stop and open a separate packet instead of widening this one.

## Acceptance criteria

- The teacher-first contest path no longer shows obvious English fallback copy in Vietnamese mode.
- `/agents` spec-pack authoring no longer leaks English seed text or English empty-state summaries where a teacher-facing Vietnamese string is expected.
- DeepTutor attribution, legal surfaces, and contract-carrying identifiers remain intact.

## Validation

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `python3 -m json.tool web/locales/en/app.json >/dev/null`
- `python3 -m json.tool web/locales/vi/app.json >/dev/null`
- `git diff --check`
- `cd web && npx eslint "components/contest/teacher-cockpit-content.ts" "components/contest/TeacherCockpit.tsx" "components/agents/SpecPackAuthoringTab.tsx" "app/(workspace)/agents/page.tsx" "app/(workspace)/dashboard/page.tsx" "app/(utility)/knowledge/page.tsx" "app/(utility)/marketplace/page.tsx"`
- `cd web && npm run build`

## Manual verification

- Open the main teacher cockpit in Vietnamese and confirm the action cards and core-loop helper copy are fully localized.
- Open `/agents` in Vietnamese and confirm the authoring flow, summaries, and empty states no longer mix English fallback text into the page.
- Spot-check Knowledge, Marketplace, and Dashboard in Vietnamese for any remaining obvious English contest-path copy.

## Parallel-work notes

- This packet should follow `C220` because the Vietnamese pass makes text longer and depends on a stable responsive layout.
- Keep the lane strictly on contest-path localization. Do not widen into a repo-wide language migration.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` is not expected to change because this lane changes teacher-facing copy only, not the system architecture or route contracts.
