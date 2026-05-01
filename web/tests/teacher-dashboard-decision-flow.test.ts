import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const DASHBOARD_PAGE_PATH = resolve(process.cwd(), "app/(workspace)/dashboard/page.tsx");
const TEACHER_PANEL_PATH = resolve(process.cwd(), "components/dashboard/TeacherInsightPanel.tsx");
const STUDENT_CARD_PATH = resolve(process.cwd(), "components/dashboard/StudentInsightCard.tsx");
const SMALL_GROUP_CARD_PATH = resolve(process.cwd(), "components/dashboard/SmallGroupInsightCard.tsx");

function readSource(path: string): string {
  return readFileSync(path, "utf8");
}

describe("teacher dashboard decision flow", () => {
  it("prioritizes intervention before supporting analytics and history", () => {
    const source = readSource(DASHBOARD_PAGE_PATH);

    expect(source).toMatch(/TeacherInsightPanel insights=\{insights\}/);
    expect(source).toMatch(/Chủ đề cần hỗ trợ/);
    expect(source).toMatch(/Gợi ý nhóm/);
    expect(source).toMatch(/Hoạt động gần đây/);
    expect(source).toMatch(/Lọc lịch sử hoạt động/);
  });

  it("no longer leaks the old English fallback guidance", () => {
    const source = readSource(DASHBOARD_PAGE_PATH);

    expect(source).not.toMatch(/Review the weakest topics first/);
    expect(source).not.toMatch(
      /Open the latest session and confirm the student is ready for the next pack/,
    );
    expect(source).toMatch(/TeacherInsightPanel insights=\{insights\}/);
  });

  it("explains how the teacher should read the cards", () => {
    const source = readSource(TEACHER_PANEL_PATH);

    expect(source).toMatch(/Cần xem ngay/);
    expect(source).toMatch(/Bước giáo viên nên làm ngay trên màn hình này/);
    expect(source).toMatch(/Bắt đầu từ từng học sinh cần xem trước/);
  });

  it("frames student and small-group cards as one evidence-to-action story", () => {
    const studentSource = readSource(STUDENT_CARD_PATH);
    const groupSource = readSource(SMALL_GROUP_CARD_PATH);

    expect(studentSource).toMatch(/1\. Dấu hiệu hệ thống vừa thấy/);
    expect(studentSource).toMatch(/2\. Cách hệ thống đang hiểu/);
    expect(studentSource).toMatch(/3\. Việc giáo viên có thể làm tiếp/);
    expect(studentSource).toMatch(/Chi tiết hệ thống/);
    expect(studentSource).not.toMatch(/UNIFIED_/);

    expect(groupSource).toMatch(/Nhóm học sinh có thể xử lý cùng một hướng/);
    expect(groupSource).toMatch(/Dấu hiệu chung của nhóm/);
    expect(groupSource).toMatch(/Việc giáo viên có thể giao cho cả nhóm/);
  });
});
