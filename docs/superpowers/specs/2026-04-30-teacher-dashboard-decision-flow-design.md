# Teacher Dashboard Decision Flow Design

- Date: 2026-04-30
- Task ID: `UI_TEACHER_DASHBOARD_DECISION_FLOW`
- Branch: `docs/business-ui-specs`

## Goal

Restructure the `Bảng điều khiển giáo viên` screen into a decision-first dashboard where urgent student interventions come first, supporting topics and metrics come second, and technical/debug details are removed from the default teacher view.

## Current Behavior

- The page has the right raw ingredients, but too many of them compete in the same reading layer:
  - hero summary
  - loop copy
  - teacher insights
  - KPI summaries
  - filters
  - activity/history
- Student-insight cards are especially overloaded:
  - observed evidence
  - inferred diagnosis
  - raw variables
  - rationale
  - multiple actions
  - debug-style strings
- Several user-facing strings still read as technical or unfinished English.
- IDs and raw classifier/debug outputs leak into the primary teacher-facing view.

## Intended Behavior

- The page should answer this order of questions:
  1. điều gì cần xem ngay;
  2. lớp đang vướng ở chủ đề nào;
  3. lớp đang làm tốt ở đâu;
  4. gần đây đã diễn ra những gì.
- High-priority intervention should dominate the page.
- Metrics and history should still exist, but in calmer supporting layers.
- Technical details should be hidden behind optional disclosure, not shown by default.

## Relationship To Earlier Spec

- This spec extends the earlier teacher-dashboard refresh direction with a stronger dashboard layout and stricter display rules for non-technical end users.
- The earlier narrative cleanup remains valid, but this spec makes the page structure more explicitly decision-first.

## Candidate Approaches

### Approach A: Keep the existing layout and only simplify copy

- Pros:
  - minimal implementation cost
- Cons:
  - leaves scanning difficulty unresolved
  - keeps overloaded insight cards

### Approach B: Four-zone decision dashboard

- top KPI row
- left priority intervention column
- right supporting topic/action column
- lower recent-activity zone
- Pros:
  - matches teacher decision-making
  - gives every layer a clear job
  - easiest path to removing default technical clutter
- Cons:
  - requires a meaningful page-layout refactor

### Approach C: Split the dashboard into multiple tabs

- Pros:
  - reduces single-page density
- Cons:
  - adds navigation friction
  - weakens the “what do I do now?” dashboard purpose

## Chosen Approach

Approach B.

The dashboard should help a teacher decide quickly, not browse through multiple tabs or parse one long narrative surface.

## Proposed Layout

### 1. Top KPI Row

- four compact KPI cards:
  - `Học sinh cần hỗ trợ`
  - `Nhóm cần can thiệp`
  - `Điểm trung bình gần đây`
  - `Phiên học đang mở`
- each card should emphasize:
  - the number
  - a short label
  - optional small delta/trend if available

### 2. Main Intervention Layer

#### Left Column: `Cần xem ngay`

- this becomes the dominant section
- each student card should answer only:
  - who needs attention
  - what topic they are struggling with
  - how urgent it is
  - what the next teacher move should be

#### Student Card Structure

- row 1:
  - student display name
  - priority badge
  - optional state badge
- row 2:
  - `Đang vướng: <chủ đề>`
- row 3:
  - two short evidence chips such as:
    - `1 câu cần xem lại`
    - `Hỗ trợ hiện tại: có hướng dẫn`
- row 4:
  - `Gợi ý tiếp theo: <can thiệp ngắn gọn>`
- row 5:
  - primary action:
    - `Xem hồ sơ học sinh`
  - secondary action:
    - `Đánh dấu đã xem`

### 3. Right Supporting Column

- stack smaller cards:
  - `Chủ đề cần hỗ trợ`
  - `Chủ đề lớp đang làm tốt`
  - `Gợi ý nhóm`
- each item should be short and count-based
- use badges to show how many students are affected

### 4. Lower Follow-Up Layer

- compact trend panel for recent score movement if available
- filter toolbar in one clear row
- recent activity list/table with denser rows and less preview text

## Strict Display Rules

The default teacher-facing view must not show:

- raw student IDs such as `UNIFIED_...`
- debug variables such as:
  - `miss_count=1`
  - `support_level=guided`
  - `contradiction_ratio=0.0`
- unfinished English technical copy such as:
  - `Primary support for...`
  - `careless_error pattern`

These may be moved into an optional collapsed section such as `Chi tiết hệ thống` if the product still needs operator access.

## Presenter / Mapping Direction

- Map raw diagnosis terms into teacher-friendly Vietnamese summaries.
- Map raw confidence/debug states into bounded status pills.
- Prefer short phrases such as:
  - `Hệ thống nghi ngờ lỗi bất cẩn`
  - `Nên cho làm lại câu dễ hơn`
  - `Cần giáo viên xem trước khi tiếp tục`

## Files Expected To Change During Implementation

- `web/app/(workspace)/dashboard/page.tsx`
- `web/components/dashboard/TeacherInsightPanel.tsx`
- `web/components/dashboard/StudentInsightCard.tsx`
- `web/components/dashboard/dashboard-presenters.ts`
- `web/locales/vi/app.json`
- `web/locales/en/app.json`
- focused dashboard copy/presenter tests

## Files Reviewed But Expected To Remain Mostly Unchanged

- backend dashboard APIs
- recommendation-generation services
- activity/session storage
- knowledge-pack management screens

## Validation Expectations

- the first screenful clearly shows urgent teacher action before deeper analytics
- student cards are scannable in under a few seconds each
- raw/debug/English technical strings are removed from the default UI
- supporting topics and recent activity remain accessible but visually secondary
