# Agents Tutor Setup Cleanup Design

- Date: 2026-04-30
- Task ID: `UI_AGENTS_TUTOR_SETUP_CLEANUP`
- Branch: `fix/agents-tutor-setup-cleanup`

## Goal

Clean up only the `Gia sư lớp học / Tutor setup` tab on `/agents` so it reads like a production teacher-facing setup flow instead of exposing internal tooling, file-system language, and confusing form behavior.

## Scope

- only the `Gia sư lớp học / Tutor setup` tab
- resolve reviewed issues `1-10`
- do not implement:
  - sticky section tabs
  - status-pill polish for the version row
- do not redesign the other `/agents` tabs

## Current Behavior

- The tutor-setup tab still shows a runtime/debug panel that is not intended for teachers.
- Section headers use internal file names like `IDENTITY.md`, `SOUL.md`, and `RULES.md`.
- Curriculum content can render escaped HTML entities like `&lt;br&gt;` literally in the textarea.
- The rule `Không giải hộ trực tiếp` is represented as a free-text input with values like `yes`.
- `/agents` still shows the shared chat-history sidebar even though this route is a configuration workflow.
- The linked Knowledge Pack area is duplicated:
  - one summary block at the top
  - one teacher-facing summary block at the side
- The empty state and main actions are not explicit enough for first-time teachers.

## Intended Behavior

- The tutor-setup tab should be teacher-facing and production-safe by default.
- Internal/debug surfaces should be hidden from the default production UI.
- Form semantics should be clear:
  - correct control types
  - fixed labels
  - clearer action names
- The page should keep one clear source of truth for the linked Knowledge Pack summary.
- The route sidebar should not compete with the setup task by showing unrelated conversation history.

## Candidate Approaches

### Approach A: Only patch the visibly broken pieces

- hide the debug panel
- rename a few labels
- swap one or two controls
- Pros:
  - smallest diff
- Cons:
  - still leaves the tab feeling inconsistent and half-internal
  - duplicate summary, empty state, and action problems remain

### Approach B: Complete production cleanup for the tutor-setup tab only

- resolve issues `1-10`
- keep data and route architecture largely intact
- avoid redesigning the other tabs
- Pros:
  - best balance of quality and scope
  - fixes the full teacher-facing flow for this tab
- Cons:
  - broader than a hotfix
  - still leaves sticky tabs and status-pill polish for later

### Approach C: Redesign the whole `/agents` route

- unify all tabs into one product-level UX sweep
- Pros:
  - cleanest long-term result
- Cons:
  - too wide for this lane
  - would mix a tab-local cleanup with unrelated product redesign

## Chosen Approach

Approach B.

This is the right scope boundary: fix the tab that teachers actually see, remove production blockers, and keep the lane out of the rest of `/agents`.

## Planned Changes By Issue

### 1. Hide runtime/debug tooling

- Hide the `KIỂM TRA CHÍNH SÁCH RUNTIME / Kiểm tra runtime kỹ thuật` panel from the production teacher-facing surface.
- Hide the `Open Next.js Dev Tools` affordance from production as well.
- If runtime audit remains useful for local development, gate it behind development-only rendering.

### 2. Replace file-name section titles

- Rename internal file headings to teacher-facing Vietnamese labels:
  - `IDENTITY.md` -> `Thông tin gia sư`
  - `SOUL.md` -> `Phong cách giảng dạy`
  - `RULES.md` -> `Quy tắc và giới hạn`
  - markdown/manual sections should also surface teacher-facing labels instead of raw file names wherever possible

### 3. Fix escaped curriculum content

- Decode curriculum and related markdown textarea values before hydrating the field if the current client path is double-escaping.
- Also inspect the save/load path so the fix is not only cosmetic.

### 4. Change `Không giải hộ trực tiếp` to a boolean control

- Replace the text input with a clear toggle/switch.
- Preserve the existing serialized value shape if the API still stores `yes` / `no`.

### 5. Remove chat history from the `/agents` shell

- Keep route navigation.
- Do not show the dominant conversation list on this route.
- This should align `/agents` with the same calmer business-shell direction already applied to other business routes.

### 6. Replace native pack select with searchable combobox

- The linked-pack selector should support search/filter.
- It should remain scoped to this tab only.

### 7. Stop relying on placeholder-as-label

- Use fixed labels above each field.
- Do not use floating-label treatment for this lane because the form is already long and dense; fixed labels are calmer and clearer.

### 8. Remove duplicate linked-pack summary block

- Remove the top linked-pack summary block from the main form.
- Keep the teacher-facing summary panel as the single preview surface for linked-pack context.

### 9. Redesign the empty state

- Add:
  - illustration/icon
  - heading
  - short helper text
  - strong CTA such as `Tạo gia sư đầu tiên`

### 10. Clarify action buttons

- Rename and explain the main actions:
  - `Xuất cấu hình`
  - `Lưu & tạo gia sư` or `Lưu thay đổi`
- Add icon support and sensible disabled states, especially when no Knowledge Pack is selected.

## Files Expected To Change During Implementation

- `web/components/agents/SpecPackAuthoringTab.tsx`
- `web/components/agents/class-tutor-pack-presenters.ts`
- `web/components/sidebar/WorkspaceSidebar.tsx`
- `web/components/sidebar/SidebarShell.tsx`
- `web/app/(workspace)/agents/page.tsx` only if route-level shell wiring or tab framing needs a bounded adjustment
- locale files and focused tests

## Files Reviewed But Expected To Remain Mostly Unchanged

- `BotsTab`
- `ProfilesTab`
- `SoulsTab`
- backend agent-spec endpoints unless the escaped curriculum issue is proven to originate there

## Validation Expectations

- `/agents` no longer shows the conversation-history block in the sidebar
- tutor setup no longer exposes runtime/debug panels on the production surface
- section titles are teacher-facing and no longer use raw file names
- the boolean rule control is understandable
- the linked-pack summary appears only once
- actions and empty state are clearer for a first-time teacher
