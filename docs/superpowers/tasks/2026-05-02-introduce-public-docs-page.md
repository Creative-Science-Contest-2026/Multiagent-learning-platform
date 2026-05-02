# Task Packet: Public Introduce Docs Page

- Task ID: `UI_PUBLIC_INTRODUCE_DOCS_PAGE`
- Commit tag: `UI-INTRODUCE`
- Date: 2026-05-02
- Branch: `fix/introduce-public-docs-page`
- Status: Implemented, local validation passing

## Objective

Create a public `/introduce` route that works as a polished project-introduction and documentation surface for judges, partners, and operators, with a fixed left sidebar, right-side docs content, real product screenshots, bilingual Vietnamese/English content, and a clearer bridge into the contest submission materials.

## User-Approved Scope

- `/introduce` is a public route outside the current app shell
- target audience is judges/partners first, then educators/operators
- layout is docs-style with a fixed left sidebar and right content column
- the route should feel like docs from Stripe/Vercel/Notion, not like an internal product screen
- the top of the page should use real screenshots for credibility
- screenshot presentation uses a grid gallery with click-to-enlarge behavior
- the page is bilingual Vietnamese/English from the start
- the route should cover both:
  - non-technical user guidance
  - technical deployment and integration guidance
- visual direction should follow `notion/DESIGN.md`

## Owned Files

- `web/app/introduce/**`
- `web/components/introduce/**`
- `web/tests/introduce-*.test.tsx`
- `docs/superpowers/tasks/2026-05-02-introduce-public-docs-page.md`
- `docs/superpowers/specs/2026-05-02-introduce-public-docs-page-design.md`
- `docs/superpowers/plans/2026-05-02-introduce-public-docs-page.md`
- `docs/superpowers/pr-notes/2026-05-02-introduce-public-docs-page.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-05-02.md`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` if the new public docs route is treated as a material product-surface addition

## Do-Not-Touch

- active frontend coverage-gate lane files outside the new `/introduce` surface
- existing contest evidence docs unless the new route intentionally links to them
- unrelated marketplace, dashboard, knowledge, agents, or playground runtime files unless a shared helper is truly needed
- global root layout/theme behavior unless the route cannot be implemented cleanly without a narrow shared adjustment

## Runtime behavior classification

- Runtime behavior change: yes
- Public route addition: yes
- New visual surface: yes

## Design before implementation

- Brainstorming skill read before implementation: yes
- Current behavior:
  - the repo contains contest docs, screenshots, and runbooks, but no dedicated public route that introduces the product in a docs-grade format
  - current major routes live either under the utility shell or workspace shell
  - hidden or de-emphasized inherited routes mean the project lacks one clean public-facing entry for project overview plus usage/technical documentation
- Intended behavior change:
  - add one standalone public docs route at `/introduce` for project overview, evidence gallery, non-technical guidance, and technical documentation
- Candidate approach A:
  - single long marketing-style landing page with sections and no persistent docs sidebar
- Candidate approach B:
  - docs-style page with fixed sidebar, right content column, real screenshot gallery, and bilingual structured sections
- Candidate approach C:
  - reuse an internal shell route and only restyle it lightly
- Chosen approach and reason:
  - approach B; it best matches the requested “big-tech docs” reading pattern while keeping the page credible, scannable, and distinct from the internal shell
- Concrete files/modules expected to change:
  - new route under `web/app/introduce/`
  - new introduce-specific UI components under `web/components/introduce/`
  - focused tests for route rendering and gallery/modal behavior
  - architecture/docs mirrors only if the route is considered a meaningful product-surface addition
- Tests to add or update:
  - route render test
  - sidebar anchor rendering test
  - gallery/lightbox interaction test
  - targeted frontend build/lint/test commands for the new route surface

## Required code reading

- Entry points/handlers to inspect:
  - `web/app/layout.tsx`
  - current route-group layouts under `web/app/(utility)/layout.tsx` and `web/app/(workspace)/layout.tsx`
- Primary logic/service/use-case modules to inspect:
  - contest-facing surfaces such as `web/components/contest/TeacherCockpit.tsx`
  - any existing shared card, typography, or shell patterns worth reusing without importing internal navigation
- Shared contracts/schemas/types to inspect:
  - static image import patterns
  - any existing simple content-presenter conventions used by current contest routes
- Adjacent or reused flows to inspect:
  - `notion/DESIGN.md`
  - `docs/contest/**`
  - screenshot assets under `assets/anh*.jpg`
- Existing tests to inspect:
  - current frontend route/component tests under `web/tests/`
- Notes from codebase survey:
  - the new route can live directly under `web/app/introduce/page.tsx` without using the existing utility/workspace shells
  - the current global theme already defines warm neutral tokens; the route should adapt `notion/DESIGN.md` patterns locally instead of rewriting global theme/font rules

## Impact surface and stop conditions

- Expected affected areas:
  - new public route
  - introduce-specific components
  - optional route-level metadata
- Files/modules likely to change:
  - `web/app/introduce/page.tsx`
  - `web/components/introduce/*`
- Files/modules that must be reviewed even if they may remain unchanged:
  - `web/app/layout.tsx`
  - `web/app/globals.css`
  - `web/components/contest/TeacherCockpit.tsx`
  - `notion/DESIGN.md`
- Minimum validation paths before the task can stop:
  - open `/introduce` directly and confirm it renders outside the internal shell
  - confirm the left sidebar anchors map to the expected sections
  - confirm the screenshot gallery opens and closes correctly
  - confirm bilingual content is present in the intended sections
  - confirm desktop layout works first and mobile/tablet degrade cleanly
- What would count as a shallow fix for this task:
  - adding a plain text page with headings but no docs sidebar, no screenshot gallery, and no differentiated non-technical vs technical sections
- Conditions that must be checked before marking done:
  - the route reads as a public docs page, not an internal admin view
  - real screenshots are integrated and usable
  - the route does not accidentally inherit workspace or utility shell navigation

## Acceptance criteria

- `/introduce` exists as a public route outside the internal shell
- the page includes a fixed left sidebar and right-side docs content on desktop
- the top of the page explains the product quickly for judges/partners
- the page shows the real screenshot gallery using the seven provided images
- gallery items support click-to-enlarge behavior
- the page includes both non-technical and technical documentation sections
- content is bilingual Vietnamese/English
- the route follows `notion/DESIGN.md` direction while staying coherent with the repo's current theme

## Required tests

- focused route/component tests for the new `/introduce` surface
- targeted frontend lint/build/test commands on touched files
- manual browser pass on desktop plus a smaller viewport check

## Manual verification

- visit `/introduce` in desktop mode
- verify sticky/fixed sidebar behavior
- verify hero screenshot and gallery order
- click multiple gallery images and close the modal/lightbox
- verify section anchors scroll correctly
- confirm non-technical and technical sections are both visible and readable

## Parallel-work notes

- Before implementation, record the runtime lane in `ai_first/ACTIVE_ASSIGNMENTS.md`.
- Implementation must use a dedicated worktree, not the current docs checkout.
- The current root checkout is already serving docs/spec work and must not become the runtime editing surface for `web/**`.

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.

## Handoff notes

- The screenshot inventory approved during design is:
  - `assets/anh1_goi_kien_thuc.jpg`
  - `assets/anh2_bang_dieu_khien_giao_vien.jpg`
  - `assets/anh3_gia_su.jpg`
  - `assets/anh4_thi_truong.jpg`
  - `assets/anh5_tro_chuyen.jpg`
  - `assets/anh6_bo_nho.jpg`
  - `assets/anh7_cai_dat.jpg`
- The route should prefer local route-specific components over shared shell abstractions unless reuse is clearly low-risk.
