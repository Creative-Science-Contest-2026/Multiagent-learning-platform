# Knowledge Pack Wizard Redesign

- Date: 2026-04-30
- Task ID: `UI_KNOWLEDGE_PACK_WIZARD_REDESIGN`
- Branch: `docs/knowledge-pack-wizard-redesign`

## Goal

Redesign the `Gói kiến thức` screen into a simpler Vietnamese-first wizard that removes notebook and model/provider noise, clarifies the metadata model for teachers, and surfaces OpenAI-backed indexing progress in a way that feels closer to modern RAG document-ingestion products.

## Current Behavior

- The page currently mixes multiple jobs in one surface:
  - create a knowledge pack
  - upload documents into an existing pack
  - edit pack metadata inline
  - browse knowledge packs
  - switch to a separate `Notebooks` tab
- The visible UI still mixes Vietnamese and English strings.
- The create form exposes technical implementation choices such as the RAG provider (`LlamaIndex`) even though the end user should not make that decision.
- The current `Grade` field is ambiguous and reads like a metadata label rather than a teaching-facing concept.
- Upload and indexing are functional but the page does not present the ingestion flow as a clear teacher-friendly sequence.

## User-Approved Product Decisions

- Replace the current create/upload layout with a wizard:
  - `Thông tin`
  - `Tài liệu`
  - `Hoàn tất`
- Remove `Notebooks` from the FE for this screen.
- Hide model/provider selection from end users completely.
- The backend should always use a default `OpenAI index` path.
- `Cấp độ` is redefined as `Mức độ khó`.
- `Mức độ khó` options are:
  - `Cơ bản`
  - `Trung bình`
  - `Nâng cao`
- Step `Thông tin` keeps only these required fields:
  - `Tên gói kiến thức`
  - `Chủ đề`
  - `Mức độ khó`
  - `Chương trình học`
  - `Mục tiêu học tập`
- Step `Tài liệu` supports only direct file upload for now.
- The screen should show uploaded documents and indexing progress in a style inspired by common RAG/document-ingestion products.
- Language should be almost fully Vietnamese, with technical terms preserved only where genuinely necessary for system status.

## Codebase Survey

### Entry points and handlers

- `web/app/(utility)/knowledge/page.tsx`
  - owns the current screen composition
  - currently contains both knowledge-pack and notebook branches
  - currently mixes create, upload, list, edit, and notebook detail flows in one file

### Primary service or use-case modules

- `web/lib/notebook-api.ts`
  - supports the notebook branch that is now a candidate for FE hiding on this screen
- `web/lib/session-api.ts`, `web/lib/marketplace-api.ts`
  - adjacent APIs, not directly responsible for this page today but related to broader pack usage flows

### Shared contracts, schemas, or types

- current FE state uses `Grade` metadata and provider selection patterns
- provider display strings are currently translation-backed and still expose `LlamaIndex`
- indexing progress is already surfaced at the knowledge-base level, but per-file status may need a stronger backend contract if not already available

### Adjacent or reused flows inspected

- locale coverage in:
  - `web/locales/vi/app.json`
  - `web/locales/en/app.json`
- the current header copy and tab switcher in the knowledge page
- the current card list structure for existing knowledge packs

### Closest existing tests

- `web/tests/contest-vietnamese-coverage.test.ts`
  - shows existing locale-oriented FE coverage patterns
- no focused test currently appears to cover this screen's wizard flow, notebook hiding, or provider hiding

## Candidate Approaches

### Approach A: Light cleanup on the existing page

- Keep the current page structure and only rename labels, hide the provider selector, and remove the notebook tab.
- Pros:
  - smallest diff
  - least disruption to the current code
- Cons:
  - preserves the current cognitive overload
  - still leaves create, upload, list, and edit stacked together without a clean task flow
  - does not deliver the “modern RAG upload” feel the user asked for

### Approach B: Wizard redesign inside the existing route

- Replace the top create/upload surface with a three-step wizard, keep the list of existing packs underneath, and keep the active-pack status panel visible on the right.
- Pros:
  - matches the approved UX direction
  - simplifies the teacher task without requiring route-level IA changes
  - supports OpenAI indexing status clearly
  - lets the list of existing packs remain visible and reachable
- Cons:
  - requires refactoring the current page structure
  - likely benefits from splitting the current large page component into smaller UI units

### Approach C: Split create flow into a separate dedicated route

- Move pack creation into its own full-screen flow and leave the current page mostly as a list/detail screen.
- Pros:
  - cleanest information architecture long-term
- Cons:
  - broader route and navigation scope
  - more expensive than needed for the current product goal
  - unnecessary before validating the simpler wizard concept

## Chosen Approach

Approach B.

It is the smallest redesign that still changes the user experience in a meaningful way. It keeps the current route intact, delivers a more modern wizard-based ingestion flow, removes notebook/provider confusion from the visible screen, and avoids a broader IA rewrite.

## Proposed UX

### Layout

- Top-level screen remains on the current `Gói kiến thức` route.
- The top section becomes a two-column layout:
  - left: the active wizard
  - right: a persistent status panel for the pack currently being created or indexed
- The list of existing packs remains below the wizard/status area.

### Header

- Keep a simpler page title and helper text.
- Remove the `Knowledge Packs / Notebooks` tab switcher from FE.
- Keep the teacher-first framing but shorten the visual noise around the core loop strip.

### Step 1: `Thông tin`

- Required fields only:
  - `Tên gói kiến thức`
  - `Chủ đề`
  - `Mức độ khó`
  - `Chương trình học`
  - `Mục tiêu học tập`
- `Mức độ khó` uses a segmented horizontal control with:
  - `Cơ bản`
  - `Trung bình`
  - `Nâng cao`
- Remove from this flow:
  - owner
  - sharing mode
  - team members
  - invite emails
  - provider/model selection

### Step 2: `Tài liệu`

- One upload mode only: file upload.
- UI should feel like a modern ingestion tool:
  - large drag-and-drop zone
  - clear accepted file types
  - selected files listed immediately
  - ability to remove selected files before upload/index starts
- No links in this version.
- No notebooks in this version.

### Step 3: `Hoàn tất`

- Overall status summary at the top:
  - number of uploaded files
  - number indexed
  - overall state such as:
    - `Đang tải lên`
    - `Đang xử lý`
    - `Hoàn tất`
    - `Có lỗi`
- File-level list underneath:
  - file name
  - per-file status
  - error message if present
  - optional last-updated time if the API already provides it
- Final CTAs:
  - primary: `Xem gói kiến thức`
  - secondary: `Tạo gói mới`

### Right-side status panel

- Always summarizes the active pack being created:
  - name
  - subject
  - difficulty
  - curriculum
  - file count
  - indexing progress
- During steps 2 and 3, this panel acts like a “live ingestion status” companion.

### Existing pack cards

- Each card should keep only high-value information:
  - `Tên gói`
  - `Chủ đề`
  - `Mức độ khó`
  - `Chương trình học`
  - `Số tài liệu`
  - `Trạng thái index`
- Hide `Mục tiêu học tập` from the default collapsed card surface.
- Main actions:
  - `Xem chi tiết`
  - `Chỉnh sửa`
- Secondary action:
  - `Xóa`
- `Đặt mặc định` should not remain a primary inline action on the default card if the simplified wizard/list direction is adopted.

## Language Direction

- The screen should be Vietnamese-first.
- Visible UI labels should be translated into natural Vietnamese wherever possible.
- English or technical terms should be preserved only in system-status or debugging contexts where a Vietnamese rendering would reduce clarity.
- Specific wording updates include:
  - `Grade` -> `Mức độ khó`
  - `Knowledge bases` -> `Danh sách gói kiến thức` or a similarly teacher-friendly label
  - `Upload documents` -> `Tải tài liệu`
  - `Learning objectives` -> `Mục tiêu học tập`

## Data and Backend Expectations

### FE expectations

- FE no longer exposes model/provider choice.
- FE no longer exposes notebooks on this screen.
- FE treats the ingestion process as one wizard, not two independent top cards.

### Backend expectations

- The create/update path should default to `OpenAI index` without asking the user.
- The system should expose enough indexing state for:
  - overall pack progress
  - per-file progress or per-file status where possible
- If the current API only exposes aggregate KB progress, a contract extension may be needed before the `Hoàn tất` step can fully match the target UX.

### OpenAI credential handling

- The user plans to provide an OpenAI key later if the current project credentials are not usable.
- The redesign should assume a default OpenAI indexing path but should not hardcode secret values into FE.

## Impact Surface For Implementation

### Likely to change

- `web/app/(utility)/knowledge/page.tsx`
- locale files under `web/locales/`
- supporting FE units extracted from the current page if the implementation splits the page into smaller components
- possibly backend/session or knowledge-pack progress contracts if file-level indexing status is not already exposed

### Reviewed but expected to remain unchanged unless implementation reveals a hard dependency

- unrelated tutor, dashboard, or marketplace routes
- notebook internals outside the FE hiding decision for this screen
- broad system architecture docs unless the runtime integration path changes materially

## Testing Expectations

- Add or update FE tests for:
  - notebook tab hidden on this screen
  - provider/model selector hidden
  - difficulty segmented control behavior
  - Vietnamese text coverage for the new wizard labels
  - file list and status rendering in the completion step
- Validate runtime flow for:
  - wizard progression
  - create pack
  - upload files
  - index status rendering

## Non-Goals

- no notebook redesign in this pass
- no link-ingestion flow in this pass
- no full IA split into a separate create route in this pass
- no user-facing model/provider choice in this pass
