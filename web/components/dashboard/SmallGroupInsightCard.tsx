"use client";

import { InsightSectionLabel } from "@/components/dashboard/InsightSectionLabel";
import type { DashboardInsights } from "@/lib/dashboard-api";

type SmallGroupInsight = DashboardInsights["small_groups"][number];

export function SmallGroupInsightCard({
  group,
  t,
}: {
  group: SmallGroupInsight;
  t: (value: string, options?: Record<string, string | number>) => string;
}) {
  return (
    <article className="rounded-3xl border border-[var(--border)] bg-[var(--background)] p-4 shadow-sm">
      <div className="flex items-start justify-between gap-3">
        <InsightSectionLabel eyebrow={t("Shared signal")} title={group.topic}>
          {group.diagnosis_type}
        </InsightSectionLabel>
        <span className="rounded-full bg-[var(--muted)] px-2.5 py-1 text-[11px] text-[var(--muted-foreground)]">
          {t("{{count}} students", { count: group.student_ids.length })}
        </span>
      </div>

      <div className="mt-4 rounded-2xl bg-emerald-50 p-3">
        <InsightSectionLabel
          eyebrow={t("Teacher move")}
          title={group.recommended_action}
          toneClassName="text-emerald-700"
        />
        <div className="mt-3 text-[12px] text-emerald-900/80">
          {t("Why these students are grouped: they show the same dominant learning signal.")}
        </div>
        <div className="mt-3 text-[12px] text-[var(--muted-foreground)]">
          {t("Students: {{students}}", { students: group.student_ids.join(", ") })}
        </div>
      </div>
    </article>
  );
}
