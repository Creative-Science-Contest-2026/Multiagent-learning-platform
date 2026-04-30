export interface DashboardPrioritySummary {
  priorityTitle: string;
  priorityBody: string;
  focusTitle: string;
  focusBody: string;
  strengthTitle: string;
  strengthBody: string;
}

function humanizeToken(value: string): string {
  return value
    .split(/[_-]+/g)
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export function formatTeacherFacingLabel(value?: string | null): string {
  return value ? humanizeToken(value) : "Chưa rõ";
}

export function buildDashboardPrioritySummary({
  nextActionRationale,
  focusTopic,
  masteredTopic,
}: {
  nextActionRationale?: string | null;
  focusTopic?: string | null;
  masteredTopic?: string | null;
}): DashboardPrioritySummary {
  return {
    priorityTitle: "Việc giáo viên nên xem trước",
    priorityBody:
      nextActionRationale?.trim() ||
      "Chưa có cảnh báo nổi bật. Hãy mở phiên học hoặc bài đánh giá gần nhất để rà soát.",
    focusTitle: "Chủ đề cần hỗ trợ",
    focusBody: focusTopic?.trim() || "Chưa có chủ đề cần chú ý",
    strengthTitle: "Điểm lớp đang làm tốt",
    strengthBody: masteredTopic?.trim() || "Chưa có điểm mạnh nổi bật",
  };
}

export function formatConfidenceLabel(value?: string | null): string {
  switch ((value || "").toLowerCase()) {
    case "low":
    case "low confidence":
      return "Cần giáo viên kiểm tra thêm";
    case "medium":
    case "medium confidence":
      return "Tạm đủ cơ sở";
    case "high":
    case "high confidence":
      return "Khá chắc chắn";
    default:
      return "Chưa rõ";
  }
}

export function formatSupportLevelLabel(value?: string | null): string {
  switch ((value || "").toLowerCase()) {
    case "guided":
      return "Có hướng dẫn";
    case "independent":
      return "Tự làm";
    case "intensive":
      return "Cần kèm sát";
    default:
      return value ? humanizeToken(value) : "Chưa rõ";
  }
}

export function formatActivityTypeLabel(value?: string | null): string {
  switch ((value || "").toLowerCase()) {
    case "assessment":
      return "Bài đánh giá";
    case "tutoring":
      return "Phiên học với gia sư";
    default:
      return value ? humanizeToken(value) : "Hoạt động";
  }
}

export function formatActivityStatusLabel(value?: string | null): string {
  switch ((value || "").toLowerCase()) {
    case "completed":
      return "Đã hoàn thành";
    case "running":
      return "Đang diễn ra";
    case "failed":
      return "Gặp lỗi";
    case "pending":
      return "Đang chờ";
    case "assigned":
      return "Đã giao";
    case "acknowledged":
      return "Đã ghi nhận";
    default:
      return formatTeacherFacingLabel(value);
  }
}

export function formatDiagnosisLabel(value?: string | null): string {
  switch ((value || "").toLowerCase()) {
    case "careless_error":
      return "Dễ sai do bất cẩn";
    case "knowledge_gap":
      return "Hổng kiến thức nền";
    case "misconception":
      return "Hiểu sai khái niệm";
    default:
      return value ? humanizeToken(value) : "Chưa có nhận định";
  }
}

export function formatTeacherMoveLabel(value?: string | null): string {
  switch ((value || "").toLowerCase()) {
    case "retry_easier":
      return "Luyện lại với mức dễ hơn";
    case "reteach_concept":
      return "Ôn lại khái niệm";
    case "small_group_reteach":
      return "Dạy lại theo nhóm nhỏ";
    default:
      return value ? humanizeToken(value) : "Chưa có gợi ý";
  }
}
