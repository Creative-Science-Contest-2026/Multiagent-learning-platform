# Knowledge Pack Dashboard Shell Design

- Date: 2026-04-30
- Task ID: `UI_KNOWLEDGE_PACK_DASHBOARD_SHELL`
- Branch: `docs/business-ui-specs`

## Goal

Redesign the `Gói kiến thức` screen into a focused two-column business workflow where creating a pack, tracking ingest status, and managing existing packs feel like one coherent dashboard instead of one long stacked page.

## Current Behavior

- The page mixes too many layers in one vertical flow:
  - page intro
  - loop/context copy
  - wizard
  - ingest state
  - existing knowledge packs
- The wizard structure is conceptually right, but visually weak:
  - steps read like text more than process UI
  - the form fields feel densely stacked
  - the CTA bar does not strongly anchor the step action
- Ingest status is important to the flow but currently lacks a strong companion panel or KPI-style status treatment.
- Existing-pack management appears too close to the create flow, so it competes with the primary task.

## Intended Behavior

- Desktop layout should read as:
  - left: create/edit wizard
  - right: ingest status for the active pack
  - bottom: existing-pack management
- The current stepper should become visually stronger and easier to scan.
- `Mức độ khó` should become a clear segmented choice.
- Existing packs should move into a more compact management surface such as a table or consistent card grid.

## Relationship To Earlier Spec

- This spec supersedes the earlier wizard-only framing by adding a clearer dashboard-shell treatment on top of the already approved three-step Knowledge Pack flow.
- The core wizard direction stays the same:
  - `Thông tin`
  - `Tài liệu`
  - `Hoàn tất`

## Candidate Approaches

### Approach A: Keep the existing wizard and only polish spacing/copy

- Pros:
  - low implementation risk
  - preserves current structure
- Cons:
  - still leaves the page too linear
  - does not fix the weak relationship between form and ingest status

### Approach B: Two-column create flow plus bottom management zone

- Left column owns the active wizard.
- Right column owns ingest status and file-processing feedback.
- Existing packs move below as a separate management section.
- Pros:
  - strongest alignment with the user’s requested mental model
  - keeps the main task obvious
  - makes ingest feel like immediate system feedback instead of an afterthought
- Cons:
  - requires a more opinionated page layout refactor

### Approach C: Split create and manage into separate routes

- Pros:
  - clean information architecture
- Cons:
  - broader routing change than needed
  - unnecessary before validating the stronger two-column layout

## Chosen Approach

Approach B.

This is the smallest redesign that changes the user’s scanning experience in the right way without widening into route-level IA work.

## Proposed Layout

### 1. Header

- H1: `Gói kiến thức`
- one-sentence helper text only
- optional secondary CTA on the right:
  - `Nhập từ file`
  - or `Tạo nhanh`
- keep the top area compact so the wizard starts earlier on the page

### 2. Main Two-Column Zone

#### Left: Wizard

- show the three-step flow as connected step cards:
  - `1. Thông tin`
  - `2. Tài liệu`
  - `3. Hoàn tất`
- current step uses a stronger accent state
- completed steps show a clear success/check treatment

#### Form Structure

- row 1:
  - `Tên gói`
  - `Chủ đề`
- row 2:
  - `Chương trình học`
  - `Mức độ khó`
- `Mức độ khó` uses a segmented control:
  - `Cơ bản`
  - `Trung bình`
  - `Nâng cao`
- `Mục tiêu học tập` becomes a labeled textarea with helper text under the field, not placeholder-heavy pseudo content
- the footer action bar should feel anchored and important:
  - `Lưu nháp`
  - primary `Tiếp tục sang Tài liệu`

#### Right: Ingest Status Panel

- use a dedicated status card
- support three primary states:
  - no documents yet
  - processing/indexing
  - completed
- panel content should include:
  - progress bar
  - number of files
  - latest update time
  - most recent error if present
- if no active pack exists yet, show a proper empty state with icon and short guidance

### 3. Existing Packs Section

- place existing-pack management below the create/ingest zone
- use either:
  - a table on desktop
  - or compact consistent cards if the table becomes too dense
- preferred table columns:
  - `Tên gói`
  - `Chủ đề`
  - `Chương trình`
  - `Tài liệu`
  - `Trạng thái`
  - `Cập nhật`
  - `Hành động`

### 4. Status and Metadata Treatment

- `Mặc định` becomes a small badge
- ingest/index state becomes a normalized status pill
- remove inconsistent raw display values that make difficulty or other metadata look unnormalized
- if a data field is semantically different from `Mức độ khó`, do not display it in the same visual slot

## Files Expected To Change During Implementation

- `web/app/(utility)/knowledge/page.tsx`
- any extracted Knowledge-page UI subcomponents if the page is split for clarity
- `web/locales/vi/app.json`
- `web/locales/en/app.json`
- focused knowledge-page tests covering wizard shell and Vietnamese-first labels

## Files Reviewed But Expected To Remain Mostly Unchanged

- backend ingestion runtime
- notebook backend internals if the page no longer exposes them
- marketplace routes
- teacher dashboard routes

## Validation Expectations

- the create flow is visually dominant over the pack-management list
- ingest status reads as a companion panel, not buried text below the form
- the stepper feels like progress UI, not plain labels
- difficulty selection is clearly clickable and mutually exclusive
- existing knowledge packs are easier to scan and manage as a separate lower layer
