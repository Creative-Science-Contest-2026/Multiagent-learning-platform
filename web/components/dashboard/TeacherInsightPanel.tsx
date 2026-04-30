import { SmallGroupInsightCard } from "@/components/dashboard/SmallGroupInsightCard";
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
        <h2 className="text-[16px] font-semibold text-[var(--foreground)]">{t("Học sinh cần giáo viên xem trước")}</h2>
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
          <h2 className="text-[16px] font-semibold text-[var(--foreground)]">{t("Học sinh cần giáo viên xem trước")}</h2>
          <p className="mt-1 text-[13px] text-[var(--muted-foreground)]">
            {t("Mỗi thẻ đi từ điều hệ thống quan sát được đến hướng can thiệp gợi ý, để giáo viên quyết định nhanh hơn trong lớp học.")}
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

      <div className="mt-4 grid gap-4 xl:grid-cols-[1.8fr_1fr]">
        <div className="space-y-4">
          {insights.students.map((student) => (
            <StudentInsightCard key={student.student_id} student={student} t={t} />
          ))}
        </div>

        <div className="space-y-4">
          <div className="rounded-2xl border border-[var(--border)] bg-[var(--muted)]/40 p-4">
            <div className="text-[12px] font-semibold uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
              {t("Gợi ý cho nhóm học sinh")}
            </div>
            <p className="mt-2 text-[13px] text-[var(--muted-foreground)]">
              {t("Khi nhiều học sinh cùng vướng một điểm, giáo viên có thể xử lý theo một hướng chung để tiết kiệm thời gian trên lớp.")}
            </p>
          </div>

          {insights.small_groups.length > 0 ? (
            insights.small_groups.map((group) => (
              <SmallGroupInsightCard key={`${group.topic}:${group.diagnosis_type}`} group={group} t={t} />
            ))
          ) : (
            <div className="rounded-2xl bg-[var(--muted)]/50 p-4 text-[13px] text-[var(--muted-foreground)]">
              {t("Chưa có nhóm học sinh nào cần gộp để can thiệp chung.")}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
