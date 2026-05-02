# Public Introduce Docs Page

- Date: 2026-05-02
- Task ID: `UI_PUBLIC_INTRODUCE_DOCS_PAGE`
- Branch: `docs/introduce-public-docs-page`

## Goal

Add one public-facing `/introduce` route that functions as a high-trust documentation and project-introduction page for judges, partners, educators, and technical operators. The page should look and read like a polished docs experience from a large product company, but it must stay honest to the current contest-proof product state and use real screenshots rather than decorative placeholder visuals.

## Current Behavior

- The repository contains rich contest documentation under `docs/contest/`, a bilingual email submission draft, screenshot evidence, validation reports, and product copy.
- The web product does not currently expose a dedicated public route that combines:
  - quick product understanding for external readers
  - screenshot-backed walkthrough proof
  - non-technical usage guidance
  - technical deployment guidance
- Existing routes are primarily product routes under either:
  - the utility shell, or
  - the workspace shell
- Those shells are not appropriate for a clean external-facing introduction page because they imply product-internal navigation and operator context rather than public documentation.

## User-Approved Product Decisions

- `/introduce` is a public, standalone route.
- The primary audience is judges/partners who need to understand the product quickly.
- The layout should follow a “big-tech docs” pattern:
  - fixed left sidebar
  - right content column
  - clean section hierarchy
- The page should be bilingual Vietnamese/English from the start.
- The route should prioritize real screenshots for trust and credibility.
- Screenshot presentation should use a compact grid gallery with click-to-enlarge behavior.
- The page should include both:
  - non-technical user documentation
  - technical/operator documentation
- Visual direction should follow `notion/DESIGN.md`.

## Codebase Survey

### Entry points and route structure

- `web/app/layout.tsx`
  - defines root fonts, theme bridge, and shell-independent app frame
- `web/app/(utility)/layout.tsx`
  - wraps utility routes with `UtilitySidebar`
- `web/app/(workspace)/layout.tsx`
  - wraps workspace routes with `WorkspaceSidebar` and `UnifiedChatProvider`

Conclusion:

- `/introduce` can live directly under `web/app/introduce/page.tsx`
- this allows a public route with no workspace or utility shell inheritance

### Existing contest-facing visual language

- `web/components/contest/TeacherCockpit.tsx`
  - shows current contest-facing copy rhythm, card density, and teacher-first messaging
- `web/components/contest/CoreLoopVisibilityStrip.tsx`
  - provides an existing visual pattern for the five-step loop that may be reused in adapted form

Conclusion:

- the public docs page can reuse product truths and some visual vocabulary from the contest path
- it should not reuse internal shell/navigation patterns

### Global design tokens and typography

- `web/app/globals.css`
  - already defines a warm neutral palette and root card/border token system
- `web/app/layout.tsx`
  - currently loads `Plus Jakarta Sans` and `Lora`
- `notion/DESIGN.md`
  - defines a Notion-like docs rhythm: fixed sidebar, structured type scale, pastel card accents, clean content hierarchy, and product-doc presentation patterns

Conclusion:

- the route should interpret `notion/DESIGN.md` through local layout/component decisions
- it should not rewrite the app's global font or token system just to mimic Notion exactly
- using the existing global fonts and base tokens is the lowest-risk way to stay coherent with the repo while still achieving the desired docs feel

### Asset inventory

The approved real screenshots already exist in `assets/`:

- `anh1_goi_kien_thuc.jpg`
- `anh2_bang_dieu_khien_giao_vien.jpg`
- `anh3_gia_su.jpg`
- `anh4_thi_truong.jpg`
- `anh5_tro_chuyen.jpg`
- `anh6_bo_nho.jpg`
- `anh7_cai_dat.jpg`

Conclusion:

- the route should consume these existing screenshots directly
- the design should not rely on synthetic mockups or illustrative filler

### Closest current documentation inputs

- `docs/contest/README.md`
- `docs/contest/SUBMISSION_PACKAGE.md`
- `docs/contest/VALIDATION_REPORT.md`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `docs/contest/VNEXPRESS_EMAIL_SUBMISSION_DRAFT.vi.md`

Conclusion:

- `/introduce` should act as a web presentation layer over these truths, not invent a second product story

## Candidate Approaches

### Approach A: Landing page with long scrolling sections

- One public page with hero, several stacked sections, and no persistent docs navigation.
- Pros:
  - easiest initial implementation
  - highly flexible for visual storytelling
- Cons:
  - less “official docs” feel
  - weaker scanability for judges or operators returning to a specific section
  - less aligned with the approved Stripe/Vercel/Notion-style pattern

### Approach B: Docs-style public route with sidebar, gallery, and structured sections

- One public docs page with:
  - fixed/sticky left sidebar
  - hero and evidence summary
  - screenshot gallery
  - non-technical guide
  - technical guide
  - resources section
- Pros:
  - best fit for the requested docs reading mode
  - easy for judges and operators to scan
  - supports both storytelling and reference use
  - works well with bilingual structured content
- Cons:
  - requires careful hierarchy so it does not feel too dense
  - gallery and modal interactions add some implementation complexity

### Approach C: Reuse an internal shell route and restyle it

- Add a new route but keep it inside an existing shell and navigation frame.
- Pros:
  - minimal route/layout work
- Cons:
  - wrong mental model for external readers
  - public introduction would inherit internal product affordances
  - weaker trust and weaker separation between product UI and public docs

## Chosen Approach

Approach B.

This is the only approach that cleanly satisfies all approved decisions: public route, docs-grade navigation, screenshot evidence, bilingual structure, and a sharp separation from internal app shells.

## Proposed Information Architecture

### Top-level route

- `web/app/introduce/page.tsx`
- no utility sidebar
- no workspace sidebar
- no chat/session provider dependency unless a component unexpectedly requires it

### Sidebar sections

The left sidebar should expose a compact section list:

1. `Overview / Tổng quan`
2. `Core Loop / Luồng sản phẩm`
3. `Evidence Gallery / Hình ảnh thực tế`
4. `For Educators / Dành cho người dùng không chuyên kỹ thuật`
5. `Technical Documentation / Tài liệu kỹ thuật`
6. `FAQ / Câu hỏi thường gặp`
7. `Resources / Tài nguyên`

### Main content sections

#### 1. Overview / Tổng quan

Purpose:

- help a judge/partner understand the product in under one minute

Content:

- product name
- one clear thesis sentence
- who it is for
- what problem it solves
- one hero screenshot
- compact evidence or status facts such as:
  - current stage: prototype/demo
  - field: education
  - teacher-controlled workflow

#### 2. Core Loop / Luồng sản phẩm

Purpose:

- make the core product logic obvious before readers descend into screenshots or instructions

Content:

- `Knowledge Pack -> Assessment -> Tutor -> Diagnosis -> Intervention`
- short bilingual explanation of each step
- possible reuse/adaptation of the existing loop-strip pattern

#### 3. Evidence Gallery / Hình ảnh thực tế

Purpose:

- provide immediate visual trust through real product surfaces

Content:

- grid gallery of the seven approved screenshots
- each image should include:
  - title
  - short caption
  - optional tag such as `Teacher setup`, `Evidence`, `Technical`, `Workflow`
- click-to-enlarge behavior:
  - modal or lightbox overlay
  - keyboard and click-away close behavior if reasonable

#### 4. For Educators / Dành cho người dùng không chuyên kỹ thuật

Purpose:

- translate the product into concrete steps for teachers and operators

Content blocks:

- how to create a Knowledge Pack from existing materials
- how to generate an assessment
- how students use the AI tutor
- how to read diagnosis and dashboard signals
- how to identify students needing intervention

Presentation:

- short step cards or numbered subsections
- screenshot references where helpful
- keep language operational, not technical

#### 5. Technical Documentation / Tài liệu kỹ thuật

Purpose:

- support IT staff, developers, and integration-oriented reviewers

Content blocks:

- local/server installation overview
- runtime environment requirements
- environment variable and AI API configuration overview
- Docker / Docker Compose guidance
- API and schema overview at a high level
- integration and cloud deployment notes

Important scope rule:

- this section should summarize and link to existing deeper sources where possible
- it should not overclaim support that the repo does not actually prove

#### 6. FAQ / Câu hỏi thường gặp

Purpose:

- reduce friction for both non-technical and technical readers

Content:

- short operational questions
- expected environment/setup questions
- contest-proof/product-scope clarity questions if helpful

#### 7. Resources / Tài nguyên

Purpose:

- connect the route to the rest of the submission and technical documentation

Content:

- links to repo
- links to contest docs
- future PDF/video links
- future technical runbook or external documents if added later

## Visual Design Direction

### High-level style

The page should feel like:

- a polished product-doc page
- serious enough for judges and partners
- lighter and clearer than the internal product routes

It should not feel like:

- a generic marketing landing page
- a copied Notion homepage
- an internal admin dashboard

### How to use `notion/DESIGN.md`

Use it as a structural and stylistic reference for:

- page hierarchy
- sidebar behavior
- spacing rhythm
- doc-section density
- card composition
- accent usage

Do **not** apply it literally by:

- replacing the app's global font stack
- rewriting root CSS variables for the whole site
- forcing a foreign brand palette across the entire app

### Local adaptation strategy

- keep the repo's current warm neutral base tokens from `globals.css`
- introduce route-level composition patterns inspired by `notion/DESIGN.md`
- allow a few route-local accent surfaces if needed for cards, labels, or gallery states
- use the current `font-sans` stack for consistency

### Desktop layout

- left sidebar stays visible and anchored
- right column becomes the main reading surface
- hero and gallery prioritize width and whitespace
- sections should breathe like docs, not stack like form panels

### Mobile behavior

- sidebar collapses into a top section index or inline navigation rail
- gallery becomes 1-column or 2-column depending on width
- the docs hierarchy should remain readable even if sticky behavior is reduced

## Content Strategy

### Bilingual presentation

The safest first version is:

- Vietnamese heading/paragraph first
- English translation immediately below or paired in the same block

This keeps both audiences readable without requiring a separate locale-routing system for the first slice.

### Judge-first framing

The first screenful should answer:

- what is this product
- who is it for
- why is it useful
- what evidence shows it is real

Only after that should the route move into deeper user guidance and technical material.

### Proof discipline

The route should preserve the repo's current claim discipline:

- teacher-controlled adaptive tutoring
- contest-safe validated prototype/demo
- no classroom-outcome overclaim
- no autonomous-final-judgment framing

## Implementation Boundaries

### Likely files to change

- `web/app/introduce/page.tsx`
- `web/components/introduce/IntroduceSidebar.tsx`
- `web/components/introduce/IntroduceSection.tsx`
- `web/components/introduce/IntroduceGallery.tsx`
- `web/components/introduce/IntroduceLightbox.tsx`
- `web/components/introduce/introduce-content.ts`
- focused tests under `web/tests/`

### Files reviewed but likely unchanged

- `web/app/layout.tsx`
- `web/app/globals.css`
- existing shell layouts
- contest docs source files

### Why not use locale JSON first

For this first slice, route-local structured bilingual content is cleaner than pushing a large amount of long-form docs copy into `web/locales/*.json`. That keeps the change bounded and avoids noisy locale-diff churn during early iteration.

## Testing Expectations

### Automated

- route renders without internal shell components
- sidebar sections render in the expected order
- gallery renders all approved screenshots
- image click opens and closes the lightbox

### Manual

- desktop viewport confirms the desired docs reading mode
- mobile/tablet viewport does not collapse into unusable density
- the route feels public and polished
- the first screenful is persuasive without being overclaiming

## Open Implementation Decisions Already Resolved

- public route: resolved
- primary audience: judges/partners first
- layout family: docs page with left sidebar
- language: bilingual from the start
- top-of-page visual proof: real screenshots
- screenshot treatment: grid gallery with click-to-enlarge

## Next Step

After user review of this spec, write a task-by-task implementation plan and then implement the route in a dedicated worktree/runtime lane.
