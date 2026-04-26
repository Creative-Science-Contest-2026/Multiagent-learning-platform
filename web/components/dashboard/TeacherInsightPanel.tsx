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
        <h2 className="text-[16px] font-semibold text-[var(--foreground)]">{t("Teacher insights")}</h2>
        <p className="mt-2 text-[13px] leading-6 text-[var(--muted-foreground)]">
          {t("No structured evidence yet. Complete at least one assessment to unlock diagnosis and next-step actions.")}
        </p>
      </section>
    );
  }

  return (
    <section className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-[16px] font-semibold text-[var(--foreground)]">{t("Teacher insights")}</h2>
          <p className="mt-1 text-[13px] text-[var(--muted-foreground)]">
            {t("Evidence-backed diagnosis for individual students and small groups.")}
          </p>
        </div>
        <div className="rounded-full bg-[var(--muted)] px-3 py-1 text-[12px] text-[var(--muted-foreground)]">
          {t("{{count}} students", { count: insights.students.length })}
        </div>
      </div>

      <div className="mt-4 grid gap-4 xl:grid-cols-[1.4fr_1fr]">
        <div className="space-y-3">
          {insights.students.map((student) => {
            const diagnosis = student.inferred[0];
            const recommendation = student.recommended_actions[0];
            return (
              <article key={student.student_id} className="rounded-2xl bg-[var(--muted)]/50 p-4">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <div className="text-[12px] font-semibold uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
                      {student.student_id}
                    </div>
                    <div className="mt-1 text-[15px] font-medium text-[var(--foreground)]">
                      {student.observed?.topic ?? t("No dominant topic")}
                    </div>
                  </div>
                  <span className="rounded-full bg-[var(--card)] px-2.5 py-1 text-[11px] text-[var(--muted-foreground)]">
                    {t("{{confidence}} confidence", { confidence: diagnosis?.confidence_tag ?? "n/a" })}
                  </span>
                </div>
                <div className="mt-3 text-[13px] text-[var(--muted-foreground)]">
                  {t("Diagnosis")}: <span className="text-[var(--foreground)]">{diagnosis?.diagnosis_type ?? t("None")}</span>
                </div>
                <div className="mt-2 text-[13px] leading-6 text-[var(--foreground)]">
                  {recommendation?.rationale ?? t("No recommendation")}
                </div>
                {diagnosis?.evidence?.length ? (
                  <div className="mt-3 flex flex-wrap gap-2">
                    {diagnosis.evidence.map((item) => (
                      <span
                        key={`${student.student_id}-${item}`}
                        className="rounded-full bg-[var(--card)] px-2.5 py-1 text-[11px] text-[var(--muted-foreground)]"
                      >
                        {item}
                      </span>
                    ))}
                  </div>
                ) : null}
              </article>
            );
          })}
        </div>

        <div className="space-y-3">
          <div className="rounded-2xl bg-[var(--muted)]/40 p-4">
            <div className="text-[12px] font-semibold uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
              {t("Small-group recommendations")}
            </div>
          </div>
          {insights.small_groups.length > 0 ? (
            insights.small_groups.map((group) => (
              <article
                key={`${group.topic}:${group.diagnosis_type}`}
                className="rounded-2xl bg-[var(--muted)]/50 p-4"
              >
                <div className="text-[14px] font-medium text-[var(--foreground)]">{group.topic}</div>
                <div className="mt-1 text-[12px] text-[var(--muted-foreground)]">
                  {group.diagnosis_type} · {group.student_ids.join(", ")}
                </div>
                <div className="mt-3 text-[13px] text-[var(--foreground)]">
                  {t("Recommended action")}: {group.recommended_action}
                </div>
              </article>
            ))
          ) : (
            <div className="rounded-2xl bg-[var(--muted)]/50 p-4 text-[13px] text-[var(--muted-foreground)]">
              {t("No shared misconception cluster yet.")}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
