import test from "node:test";
import assert from "node:assert/strict";
import {
  buildDashboardPrioritySummary,
  formatActivityStatusLabel,
  formatActivityTypeLabel,
  formatConfidenceLabel,
  formatSupportLevelLabel,
} from "../components/dashboard/dashboard-presenters.ts";

test("dashboard priority summary prefers the first recommendation rationale", () => {
  const summary = buildDashboardPrioritySummary({
    nextActionRationale: "Ưu tiên ôn lại phép biến đổi cơ bản trước khi giao bài mới.",
    focusTopic: "Phương trình bậc hai",
    masteredTopic: "Biểu đồ hàm số",
  });

  assert.equal(summary.priorityTitle, "Việc giáo viên nên xem trước");
  assert.equal(summary.priorityBody, "Ưu tiên ôn lại phép biến đổi cơ bản trước khi giao bài mới.");
  assert.equal(summary.focusTitle, "Chủ đề cần hỗ trợ");
  assert.equal(summary.focusBody, "Phương trình bậc hai");
  assert.equal(summary.strengthTitle, "Điểm lớp đang làm tốt");
  assert.equal(summary.strengthBody, "Biểu đồ hàm số");
});

test("dashboard priority summary falls back to calm empty-state wording", () => {
  const summary = buildDashboardPrioritySummary({});

  assert.equal(summary.priorityBody, "Chưa có cảnh báo nổi bật. Hãy mở phiên học hoặc bài đánh giá gần nhất để rà soát.");
  assert.equal(summary.focusBody, "Chưa có chủ đề cần chú ý");
  assert.equal(summary.strengthBody, "Chưa có điểm mạnh nổi bật");
});

test("confidence labels are rewritten for teachers", () => {
  assert.equal(formatConfidenceLabel("low"), "Cần giáo viên kiểm tra thêm");
  assert.equal(formatConfidenceLabel("medium"), "Tạm đủ cơ sở");
  assert.equal(formatConfidenceLabel("high"), "Khá chắc chắn");
  assert.equal(formatConfidenceLabel(undefined), "Chưa rõ");
});

test("activity and support labels avoid raw system terms", () => {
  assert.equal(formatActivityTypeLabel("assessment"), "Bài đánh giá");
  assert.equal(formatActivityTypeLabel("tutoring"), "Phiên học với gia sư");
  assert.equal(formatActivityStatusLabel("completed"), "Đã hoàn thành");
  assert.equal(formatActivityStatusLabel("running"), "Đang diễn ra");
  assert.equal(formatSupportLevelLabel("guided"), "Có hướng dẫn");
  assert.equal(formatSupportLevelLabel("independent"), "Tự làm");
});
