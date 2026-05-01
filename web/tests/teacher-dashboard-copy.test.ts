import { describe, expect, it } from "vitest";
import {
  buildDashboardPrioritySummary,
  formatActivityStatusLabel,
  formatActivityTypeLabel,
  formatConfidenceLabel,
  formatDiagnosisLabel,
  formatStudentDisplayName,
  formatSupportLevelLabel,
  formatTeacherFacingLabel,
  formatTeacherMoveLabel,
} from "../components/dashboard/dashboard-presenters";

describe("dashboard presenters", () => {
  it("prefers the first recommendation rationale in the priority summary", () => {
    const summary = buildDashboardPrioritySummary({
      nextActionRationale: "Ưu tiên ôn lại phép biến đổi cơ bản trước khi giao bài mới.",
      focusTopic: "Phương trình bậc hai",
      masteredTopic: "Biểu đồ hàm số",
    });

    expect(summary.priorityTitle).toBe("Việc giáo viên nên xem trước");
    expect(summary.priorityBody).toBe(
      "Ưu tiên ôn lại phép biến đổi cơ bản trước khi giao bài mới.",
    );
    expect(summary.focusTitle).toBe("Chủ đề cần hỗ trợ");
    expect(summary.focusBody).toBe("Phương trình bậc hai");
    expect(summary.strengthTitle).toBe("Điểm lớp đang làm tốt");
    expect(summary.strengthBody).toBe("Biểu đồ hàm số");
  });

  it("falls back to calm empty-state wording", () => {
    const summary = buildDashboardPrioritySummary({});

    expect(summary.priorityBody).toBe(
      "Chưa có cảnh báo nổi bật. Hãy mở phiên học hoặc bài đánh giá gần nhất để rà soát.",
    );
    expect(summary.focusBody).toBe("Chưa có chủ đề cần chú ý");
    expect(summary.strengthBody).toBe("Chưa có điểm mạnh nổi bật");
  });

  it("rewrites confidence labels for teachers", () => {
    expect(formatConfidenceLabel("low")).toBe("Cần giáo viên kiểm tra thêm");
    expect(formatConfidenceLabel("medium")).toBe("Tạm đủ cơ sở");
    expect(formatConfidenceLabel("high")).toBe("Khá chắc chắn");
    expect(formatConfidenceLabel(undefined)).toBe("Chưa rõ");
  });

  it("avoids raw system terms in activity and support labels", () => {
    expect(formatActivityTypeLabel("assessment")).toBe("Bài đánh giá");
    expect(formatActivityTypeLabel("tutoring")).toBe("Phiên học với gia sư");
    expect(formatActivityStatusLabel("completed")).toBe("Đã hoàn thành");
    expect(formatActivityStatusLabel("running")).toBe("Đang diễn ra");
    expect(formatSupportLevelLabel("guided")).toBe("Có hướng dẫn");
    expect(formatSupportLevelLabel("independent")).toBe("Tự làm");
  });

  it("hides raw classifier tokens in diagnosis and teacher move labels", () => {
    expect(formatDiagnosisLabel("careless_error")).toBe("Dễ sai do bất cẩn");
    expect(formatDiagnosisLabel("knowledge_gap")).toBe("Hổng kiến thức nền");
    expect(formatTeacherMoveLabel("retry_easier")).toBe("Luyện lại với mức dễ hơn");
    expect(formatTeacherMoveLabel("small_group_reteach")).toBe(
      "Dạy lại theo nhóm nhỏ",
    );
  });

  it("keeps generic teacher-facing labels bounded and readable", () => {
    expect(formatTeacherFacingLabel("acknowledged")).toBe("Đã ghi nhận");
    expect(formatTeacherFacingLabel("teacher_review_required")).toBe(
      "Cần giáo viên xác nhận",
    );
    expect(formatTeacherFacingLabel(undefined)).toBe("Chưa rõ");
  });

  it("hides raw unified identifiers in student display names", () => {
    expect(formatStudentDisplayName("UNIFIED_1776618085500_8C117467")).toBe(
      "Học sinh 8C117467",
    );
    expect(formatStudentDisplayName("student-demo")).toBe("student-demo");
    expect(formatStudentDisplayName(undefined)).toBe("Học sinh");
  });
});
