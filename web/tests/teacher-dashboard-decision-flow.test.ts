import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import test from "node:test";

const DASHBOARD_PAGE_PATH = resolve(process.cwd(), "app/(workspace)/dashboard/page.tsx");
const TEACHER_PANEL_PATH = resolve(process.cwd(), "components/dashboard/TeacherInsightPanel.tsx");
const STUDENT_CARD_PATH = resolve(process.cwd(), "components/dashboard/StudentInsightCard.tsx");
const SMALL_GROUP_CARD_PATH = resolve(process.cwd(), "components/dashboard/SmallGroupInsightCard.tsx");

function readSource(path: string): string {
  return readFileSync(path, "utf8");
}

test("dashboard page prioritizes intervention before supporting analytics and history", () => {
  const source = readSource(DASHBOARD_PAGE_PATH);

  assert.match(source, /TeacherInsightPanel insights=\{insights\}/);
  assert.match(source, /Chủ đề cần hỗ trợ/);
  assert.match(source, /Gợi ý nhóm/);
  assert.match(source, /Hoạt động gần đây/);
  assert.match(source, /Lọc lịch sử hoạt động/);
});

test("dashboard page no longer leaks the old English fallback guidance", () => {
  const source = readSource(DASHBOARD_PAGE_PATH);

  assert.doesNotMatch(source, /Review the weakest topics first/);
  assert.doesNotMatch(source, /Open the latest session and confirm the student is ready for the next pack/);
  assert.match(source, /TeacherInsightPanel insights=\{insights\}/);
});

test("teacher insight panel explains how the teacher should read the cards", () => {
  const source = readSource(TEACHER_PANEL_PATH);

  assert.match(source, /Cần xem ngay/);
  assert.match(source, /Bước giáo viên nên làm ngay trên màn hình này/);
  assert.match(source, /Bắt đầu từ từng học sinh cần xem trước/);
});

test("student and small-group cards are framed as one evidence-to-action story", () => {
  const studentSource = readSource(STUDENT_CARD_PATH);
  const groupSource = readSource(SMALL_GROUP_CARD_PATH);

  assert.match(studentSource, /1\. Dấu hiệu hệ thống vừa thấy/);
  assert.match(studentSource, /2\. Cách hệ thống đang hiểu/);
  assert.match(studentSource, /3\. Việc giáo viên có thể làm tiếp/);
  assert.match(studentSource, /Chi tiết hệ thống/);
  assert.doesNotMatch(studentSource, /UNIFIED_/);

  assert.match(groupSource, /Nhóm học sinh có thể xử lý cùng một hướng/);
  assert.match(groupSource, /Dấu hiệu chung của nhóm/);
  assert.match(groupSource, /Việc giáo viên có thể giao cho cả nhóm/);
});
