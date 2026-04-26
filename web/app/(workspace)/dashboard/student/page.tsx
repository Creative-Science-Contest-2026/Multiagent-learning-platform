"use client";

import Link from "next/link";
import { Suspense, useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import { ArrowLeft, ArrowRight, BookOpen, Flame, LineChart, Loader2, Target } from "lucide-react";
import { useTranslation } from "react-i18next";
import { StudentInsightDetail } from "@/components/dashboard/StudentInsightDetail";
import {
  getDashboardInsights,
  getStudentProgress,
  type DashboardInsights,
  type StudentProgressAssessment,
  type StudentProgressOverview,
  type StudentProgressPathStep,
  type StudentProgressTopic,
} from "@/lib/dashboard-api";

function formatTime(value: number): string {
  if (!value) return "";
  const timestamp = value < 10_000_000_000 ? value * 1000 : value;
  return new Intl.DateTimeFormat(undefined, {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(timestamp));
}

function scoreTone(value: number): string {
  if (value >= 85) return "text-emerald-600";
  if (value >= 70) return "text-amber-600";
  return "text-rose-600";
}

function buildPathSourceLabel(
  row: StudentProgressPathStep,
  t: (value: string, options?: Record<string, string | number>) => string,
): string {
  if (row.source === "focus_topic") {
    return t("Triggered by recent weak-topic signals");
  }
  if (row.knowledge_base) {
    return t("Pulled from {{knowledgeBase}} objectives", { knowledgeBase: row.knowledge_base });
  }
  return t("Pulled from knowledge-pack objectives");
}

function TopicList({
  title,
  icon: Icon,
  rows,
  emptyLabel,
  t,
}: {
  title: string;
  icon: typeof Target;
  rows: StudentProgressTopic[];
  emptyLabel: string;
  t: (value: string, options?: Record<string, string | number>) => string;
}) {
  return (
    <section className="rounded-[28px] border border-[var(--border)] bg-[var(--card)] p-5">
      <div className="flex items-center gap-2">
        <Icon size={16} className="text-[var(--muted-foreground)]" />
        <h2 className="text-[16px] font-semibold text-[var(--foreground)]">{title}</h2>
      </div>
      {rows.length > 0 ? (
        <div className="mt-4 space-y-3">
          {rows.map((row) => (
            <div
              key={row.topic}
              className="rounded-2xl bg-[var(--muted)]/60 px-4 py-3"
            >
              <div className="flex items-center justify-between gap-3">
                <span className="text-[13px] font-medium text-[var(--foreground)]">{row.topic}</span>
                <span className={`text-[13px] font-semibold ${scoreTone(row.accuracy_percent)}`}>
                  {row.accuracy_percent}%
                </span>
              </div>
              <div className="mt-2 text-[12px] text-[var(--muted-foreground)]">
                {t("{{correct}}/{{total}} correct", {
                  correct: row.correct_count,
                  total: row.total_questions,
                })}
                {row.incorrect_count > 0
                  ? ` • ${t("{{incorrect}} to revisit", { incorrect: row.incorrect_count })}`
                  : ""}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="mt-4 rounded-2xl bg-[var(--muted)]/50 px-4 py-6 text-center text-[13px] text-[var(--muted-foreground)]">
          {emptyLabel}
        </div>
      )}
    </section>
  );
}

function AssessmentList({
  rows,
  emptyLabel,
  t,
}: {
  rows: StudentProgressAssessment[];
  emptyLabel: string;
  t: (value: string, options?: Record<string, string | number>) => string;
}) {
  if (rows.length === 0) {
    return (
      <div className="rounded-[28px] border border-dashed border-[var(--border)] bg-[var(--card)] px-5 py-8 text-center text-[13px] text-[var(--muted-foreground)]">
        {emptyLabel}
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {rows.map((row) => {
        const href = row.review_ref ? `/${row.review_ref}` : null;
        return (
          <article
            key={row.session_id}
            className="rounded-[28px] border border-[var(--border)] bg-[var(--card)] px-5 py-4"
          >
            <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
              <div className="min-w-0">
                {href ? (
                  <Link
                    href={href}
                    className="text-[15px] font-semibold text-[var(--foreground)] underline-offset-4 hover:underline"
                  >
                    {row.title || t("Untitled assessment")}
                  </Link>
                ) : (
                  <div className="text-[15px] font-semibold text-[var(--foreground)]">
                    {row.title || t("Untitled assessment")}
                  </div>
                )}
                <div className="mt-1 text-[12px] text-[var(--muted-foreground)]">
                  {formatTime(row.timestamp)}
                </div>
                {row.knowledge_bases.length > 0 && (
                  <div className="mt-3 flex flex-wrap gap-1">
                    {row.knowledge_bases.map((kb) => (
                      <span
                        key={`${row.session_id}-${kb}`}
                        className="rounded-full bg-[var(--muted)] px-2.5 py-1 text-[11px] text-[var(--muted-foreground)]"
                      >
                        {kb}
                      </span>
                    ))}
                  </div>
                )}
              </div>
              <div className="rounded-2xl bg-[var(--muted)]/70 px-4 py-3 text-right">
                <div className={`text-[24px] font-semibold ${scoreTone(row.score_percent)}`}>
                  {row.score_percent}%
                </div>
                <div className="text-[12px] text-[var(--muted-foreground)]">
                {t("{{correct}}/{{total}} correct", {
                  correct: row.correct_count,
                  total: row.total_questions,
                })}
                </div>
              </div>
            </div>
          </article>
        );
      })}
    </div>
  );
}

function LearningPathCard({
  rows,
  t,
}: {
  rows: StudentProgressPathStep[];
  t: (value: string) => string;
}) {
  return (
    <section className="rounded-[28px] border border-[var(--border)] bg-[var(--card)] p-5">
      <div className="flex items-center gap-2">
        <ArrowRight size={16} className="text-[var(--muted-foreground)]" />
        <h2 className="text-[16px] font-semibold text-[var(--foreground)]">
          {t("Suggested learning path")}
        </h2>
      </div>
      {rows.length > 0 ? (
        <div className="mt-4 space-y-3">
          {rows.map((row, index) => (
            <div key={`${row.topic}-${index}`} className="rounded-2xl bg-[var(--muted)]/60 px-4 py-3">
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <div className="text-[12px] font-semibold uppercase tracking-[0.12em] text-[var(--muted-foreground)]">
                    {t("Step")} {index + 1}
                  </div>
                  <div className="mt-1 text-[14px] font-medium text-[var(--foreground)]">
                    {row.topic}
                  </div>
                </div>
                <span className="rounded-full bg-[var(--card)] px-2.5 py-1 text-[11px] text-[var(--muted-foreground)]">
                  {row.status === "review" ? t("Review next") : t("Learn next")}
                </span>
              </div>
              <div className="mt-2 text-[12px] text-[var(--muted-foreground)]">
                {buildPathSourceLabel(row, t)}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="mt-4 rounded-2xl bg-[var(--muted)]/50 px-4 py-6 text-center text-[13px] text-[var(--muted-foreground)]">
          {t("No learning path suggestions yet. Complete an assessment or add pack objectives to unlock the next-step sequence.")}
        </div>
      )}
    </section>
  );
}

function StudentDashboardContent() {
  const { t } = useTranslation();
  const searchParams = useSearchParams();
  const studentId = searchParams.get("student") ?? "";
  const [overview, setOverview] = useState<StudentProgressOverview | null>(null);
  const [insights, setInsights] = useState<DashboardInsights | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    Promise.all([getStudentProgress(), getDashboardInsights(100)])
      .then(([progressData, insightData]) => {
        if (!cancelled) {
          setOverview(progressData);
          setInsights(insightData);
          setError(null);
        }
      })
      .catch((err) => {
        if (!cancelled) setError(err instanceof Error ? err.message : String(err));
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const totals = overview?.totals;
  const focusTopics = overview?.focus_topics ?? [];
  const masteredTopics = overview?.mastered_topics ?? [];
  const suggestedPath = overview?.suggested_learning_path ?? [];
  const activeStudent = insights?.students.find((row) => row.student_id === studentId) ?? null;
  const statCards = useMemo(
    () => [
      {
        label: t("Learning streak"),
        value: totals?.streak_days ?? 0,
        suffix: t("days"),
        icon: Flame,
      },
      {
        label: t("Average score"),
        value: totals?.average_score_percent ?? 0,
        suffix: "%",
        icon: LineChart,
      },
      {
        label: t("Assessments"),
        value: totals?.assessments_completed ?? 0,
        suffix: "",
        icon: ArrowRight,
      },
      {
        label: t("Knowledge Packs"),
        value: totals?.knowledge_packs_used ?? 0,
        suffix: "",
        icon: BookOpen,
      },
    ],
    [t, totals],
  );

  return (
    <main className="min-h-full bg-[radial-gradient(circle_at_top_left,_rgba(247,208,96,0.18),_transparent_32%),linear-gradient(180deg,_var(--background),_color-mix(in_oklab,_var(--background)_78%,_white))]">
      <div className="mx-auto flex w-full max-w-[1120px] flex-col gap-6 px-6 py-8">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 text-[13px] text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
          >
            <ArrowLeft size={15} />
            {t("Back to teacher dashboard")}
          </Link>
          <span className="rounded-full border border-[var(--border)] bg-[var(--card)] px-3 py-1 text-[12px] font-medium text-[var(--muted-foreground)]">
            {t("Student Detail")}
          </span>
        </div>

        <section className="rounded-[32px] border border-[var(--border)] bg-[var(--card)]/90 px-6 py-6 shadow-sm">
          <p className="text-[12px] font-semibold uppercase tracking-[0.14em] text-[var(--muted-foreground)]">
            {t("Teacher Drill-down")}
          </p>
          <div className="mt-3 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
            <div>
              <h1 className="text-[30px] font-semibold tracking-tight text-[var(--foreground)]">
                {activeStudent?.student_id || t("Inspect evidence before deciding the next move")}
              </h1>
              <p className="mt-2 max-w-[720px] text-[14px] leading-6 text-[var(--muted-foreground)]">
                {t("Review observed evidence first, then inspect diagnosis and the clearest next classroom move.")}
              </p>
            </div>
            {loading && (
              <div className="inline-flex items-center gap-2 text-[13px] text-[var(--muted-foreground)]">
                <Loader2 size={14} className="animate-spin" />
                {t("Loading progress")}
              </div>
            )}
          </div>
          <div className="mt-4 grid gap-3 md:grid-cols-3">
            <div className="rounded-2xl bg-[var(--muted)]/50 px-4 py-3">
              <div className="text-[11px] uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
                {t("Recommended action")}
              </div>
              <div className="mt-1 text-[13px] font-medium text-[var(--foreground)]">
                {activeStudent?.recommended_actions[0]?.rationale ??
                  (focusTopics.length > 0
                    ? t("Review the weakest topic before assigning a harder pack")
                    : t("No weak topics detected yet. The student is ready for a stretch goal."))}
              </div>
            </div>
            <div className="rounded-2xl bg-[var(--muted)]/50 px-4 py-3">
              <div className="text-[11px] uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
                {t("Observed topic")}
              </div>
              <div className="mt-1 text-[13px] font-medium text-[var(--foreground)]">
                {activeStudent?.observed?.topic || focusTopics[0]?.topic || t("No weak topics detected yet.")}
              </div>
            </div>
            <div className="rounded-2xl bg-[var(--muted)]/50 px-4 py-3">
              <div className="text-[11px] uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
                {t("Diagnosis")}
              </div>
              <div className="mt-1 text-[13px] font-medium text-[var(--foreground)]">
                {activeStudent?.inferred[0]?.diagnosis_type ||
                  t("No diagnosis available. Complete an assessment or tutoring session to generate evidence.")}
              </div>
            </div>
          </div>
        </section>

        <StudentInsightDetail key={activeStudent?.student_id ?? "no-student"} student={activeStudent} t={t} />

        {error && (
          <div className="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-[13px] text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
            {t("Failed to load student progress")}: {error}
          </div>
        )}

        <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          {statCards.map((card) => (
            <div
              key={card.label}
              className="rounded-[28px] border border-[var(--border)] bg-[var(--card)] px-5 py-4"
            >
              <div className="flex items-center justify-between gap-3">
                <span className="text-[12px] font-medium text-[var(--muted-foreground)]">
                  {card.label}
                </span>
                <card.icon size={16} className="text-[var(--muted-foreground)]" />
              </div>
              <div className="mt-4 flex items-end gap-2">
                <span className="text-[30px] font-semibold text-[var(--foreground)]">
                  {loading ? "-" : card.value}
                </span>
                {card.suffix && (
                  <span className="pb-1 text-[13px] text-[var(--muted-foreground)]">
                    {card.suffix}
                  </span>
                )}
              </div>
            </div>
          ))}
        </section>

        <section className="grid gap-6 xl:grid-cols-[1.3fr_0.7fr]">
          <div>
            <div className="mb-3 flex items-center justify-between">
              <h2 className="text-[18px] font-semibold text-[var(--foreground)]">
                {t("Recent assessments")}
              </h2>
              {overview?.score_trend && overview.score_trend.length > 1 && (
                <span className="text-[12px] text-[var(--muted-foreground)]">
                  {t("Trend")}: {overview.score_trend[0].score_percent}% {"->"}{" "}
                  {overview.score_trend[overview.score_trend.length - 1].score_percent}%
                </span>
              )}
            </div>
            <AssessmentList
              rows={overview?.recent_assessments ?? []}
              emptyLabel={t("No assessments yet. Generate a quiz to begin tracking progress.")}
              t={t}
            />
          </div>

          <div className="space-y-6">
            <LearningPathCard rows={overview?.suggested_learning_path ?? []} t={t} />
            <TopicList
              title={t("Focus next")}
              icon={Target}
              rows={overview?.focus_topics ?? []}
              emptyLabel={t("No weak topics detected yet. The student is ready for a stretch goal.")}
              t={t}
            />
            <TopicList
              title={t("Mastered topics")}
              icon={LineChart}
              rows={masteredTopics}
              emptyLabel={t("Mastered topics will appear after completed assessments.")}
              t={t}
            />
          </div>
        </section>
      </div>
    </main>
  );
}

export default function StudentDashboardPage() {
  const { t } = useTranslation();

  return (
    <Suspense
      fallback={
        <main className="min-h-full bg-[radial-gradient(circle_at_top_left,_rgba(247,208,96,0.18),_transparent_32%),linear-gradient(180deg,_var(--background),_color-mix(in_oklab,_var(--background)_78%,_white))]">
          <div className="mx-auto flex w-full max-w-[1120px] items-center justify-center px-6 py-16">
            <div className="inline-flex items-center gap-2 text-[13px] text-[var(--muted-foreground)]">
              <Loader2 size={14} className="animate-spin" />
              {t("Loading student detail")}
            </div>
          </div>
        </main>
      }
    >
      <StudentDashboardContent />
    </Suspense>
  );
}
