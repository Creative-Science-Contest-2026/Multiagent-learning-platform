import { StudentInsightCard } from "@/components/dashboard/StudentInsightCard";
import type { DashboardInsights } from "@/lib/dashboard-api";
import { useTranslation } from "react-i18next";

export function TeacherInsightPanel({
  insights,
}: {
  insights: DashboardInsights | null;
}) {
  const { t } = useTranslation();

  if (!insights || (insights.students.length === 0 && insights.small_groups.length === 0)) {
    return (
      <section className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-5 shadow-sm">
        <p className="text-[12px] font-semibold uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
          {t("Cần xem ngay")}
        </p>
        <h2 className="mt-1 text-[20px] font-semibold text-[var(--foreground)]">
          {t("Học sinh cần giáo viên xem trước")}
        </h2>
        <p className="mt-2 text-[13px] leading-6 text-[var(--muted-foreground)]">
          {t("Chưa có dữ liệu đủ rõ để giáo viên rà soát. Hãy hoàn thành ít nhất một bài đánh giá hoặc một phiên học để nhận gợi ý cụ thể hơn.")}
        </p>
      </section>
    );
  }

  return (
    <section className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-5 shadow-sm">
      <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
        <div>
          <p className="text-[12px] font-semibold uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
            {t("Cần xem ngay")}
          </p>
          <h2 className="mt-1 text-[20px] font-semibold text-[var(--foreground)]">{t("Học sinh cần giáo viên xem trước")}</h2>
          <p className="mt-1 text-[13px] text-[var(--muted-foreground)]">
            {t("Đọc từ trái sang phải: dấu hiệu, cách hiểu hiện tại, rồi mới quyết định việc cần làm.")}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <span className="rounded-full bg-[var(--muted)] px-3 py-1 text-[12px] text-[var(--muted-foreground)]">
            {t("{{count}} học sinh cần xem", { count: insights.students.length })}
          </span>
          <span className="rounded-full bg-[var(--muted)] px-3 py-1 text-[12px] text-[var(--muted-foreground)]">
            {t("{{count}} gợi ý cho nhóm nhỏ", { count: insights.small_groups.length })}
          </span>
        </div>
      </div>

      <div className="mt-4 rounded-2xl border border-[var(--border)] bg-[var(--background)]/70 p-4">
        <div className="text-[12px] font-semibold uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
          {t("Bước giáo viên nên làm ngay trên màn hình này")}
        </div>
        <p className="mt-2 text-[13px] leading-6 text-[var(--muted-foreground)]">
          {t("Bắt đầu từ từng học sinh cần xem trước, sau đó mới nhìn sang nhóm nhỏ có cùng điểm vướng để chọn một hướng xử lý tiết kiệm thời gian trên lớp.")}
        </p>
      </div>

      <div className="mt-4 grid gap-4 xl:grid-cols-[1.8fr_1fr]">
        <div className="space-y-4 xl:col-span-2">
          {insights.students.map((student) => (
            <StudentInsightCard key={student.student_id} student={student} t={t} />
          ))}
        </div>
      </div>
    </section>
  );
}
