"use client";

import { InsightSectionLabel } from "@/components/dashboard/InsightSectionLabel";
import type { TeacherInsightStudent } from "@/lib/dashboard-api";

function formatLatency(seconds: number | undefined): string | null {
  if (seconds == null) return null;
  if (seconds < 1) return `≈${Math.round(seconds * 1000)} ms`;
  return `${Math.round(seconds)} s`;
}

export function StudentInsightDetail({
  student,
  t,
}: {
  student: TeacherInsightStudent | null;
  t: (value: string, options?: Record<string, string | number>) => string;
}) {
  const diagnosis = student?.inferred[0];
  const recommendation = student?.recommended_actions[0];

  if (!student) {
    return (
      <section className="rounded-[28px] border border-dashed border-[var(--border)] bg-[var(--card)] px-5 py-8 text-center text-[13px] text-[var(--muted-foreground)]">
        {t("Choose a student from the dashboard to inspect evidence and next steps.")}
      </section>
    );
  }

  return (
    <section className="grid gap-4 xl:grid-cols-[1.15fr_0.85fr]">
      <div className="space-y-4">
        <section className="rounded-[28px] border border-[var(--border)] bg-[var(--card)] p-5 shadow-sm">
          <InsightSectionLabel eyebrow={t("Observed")} title={student.observed?.topic ?? t("No recent evidence")} />
          <div className="mt-4 grid gap-3 sm:grid-cols-3">
            <div className="rounded-2xl bg-[var(--muted)]/50 p-3 text-[12px] text-[var(--foreground)]">
              <div className="font-semibold text-[var(--muted-foreground)]">{t("Miss count")}</div>
              <div className="mt-2 text-[18px] font-semibold text-[var(--foreground)]">
                {student.observed?.miss_count ?? 0}
              </div>
            </div>
            <div className="rounded-2xl bg-[var(--muted)]/50 p-3 text-[12px] text-[var(--foreground)]">
              <div className="font-semibold text-[var(--muted-foreground)]">{t("Average latency")}</div>
              <div className="mt-2 text-[18px] font-semibold text-[var(--foreground)]">
                {formatLatency(student.observed?.avg_latency_seconds) ?? t("Unknown")}
              </div>
            </div>
            <div className="rounded-2xl bg-[var(--muted)]/50 p-3 text-[12px] text-[var(--foreground)]">
              <div className="font-semibold text-[var(--muted-foreground)]">{t("Confidence trend")}</div>
              <div className="mt-2 text-[18px] font-semibold text-[var(--foreground)]">
                {student.student_state?.confidence_trend ?? t("Unknown")}
              </div>
            </div>
          </div>
        </section>

        <section className="rounded-[28px] border border-[var(--border)] bg-[var(--card)] p-5 shadow-sm">
          <InsightSectionLabel
            eyebrow={t("Inferred")}
            title={diagnosis?.diagnosis_type ?? t("No diagnosis")}
            toneClassName="text-amber-700"
          >
            {t("Confidence: {{value}}", { value: diagnosis?.confidence_tag ?? "N/A" })}
          </InsightSectionLabel>
          <div className="mt-4 rounded-2xl bg-amber-50 p-4">
            <div className="text-[13px] font-medium text-[var(--foreground)]">
              {diagnosis?.topic ? t("Likely topic gap: {{topic}}", { topic: diagnosis.topic }) : t("No inferred topic")}
            </div>
            {diagnosis?.evidence?.length ? (
              <ul className="mt-3 space-y-2 text-[12px] text-[var(--muted-foreground)]">
                {diagnosis.evidence.map((fact) => (
                  <li key={`${student.student_id}-${fact}`}>• {fact}</li>
                ))}
              </ul>
            ) : (
              <div className="mt-3 text-[12px] text-[var(--muted-foreground)]">
                {t("No structured rationale was provided in the payload.")}
              </div>
            )}
          </div>
        </section>
      </div>

      <section className="rounded-[28px] border border-[var(--border)] bg-[var(--card)] p-5 shadow-sm">
        <InsightSectionLabel
          eyebrow={t("Recommended Action")}
          title={recommendation?.action_type ?? t("No action")}
          toneClassName="text-emerald-700"
        >
          {t("Use this as the next teacher move, not as an automatic intervention.")}
        </InsightSectionLabel>

        <div className="mt-4 rounded-2xl bg-emerald-50 p-4">
          <div className="text-[14px] font-medium text-[var(--foreground)]">
            {recommendation?.rationale ?? t("No recommendation available")}
          </div>
          <div className="mt-4 space-y-2 text-[12px] text-[var(--muted-foreground)]">
            <div>{t("Topic: {{topic}}", { topic: recommendation?.topic ?? diagnosis?.topic ?? t("Unknown") })}</div>
            <div>
              {t("Targets: {{count}} student(s)", {
                count: recommendation?.target_student_ids.length ?? 0,
              })}
            </div>
            {student.student_state?.support_level ? (
              <div>{t("Support level: {{value}}", { value: student.student_state.support_level })}</div>
            ) : null}
          </div>
        </div>
      </section>
    </section>
  );
}
