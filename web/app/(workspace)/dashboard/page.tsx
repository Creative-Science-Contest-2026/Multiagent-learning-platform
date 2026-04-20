"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { Activity, ArrowRight, BookOpen, CheckCircle2, Loader2, PenLine, Users } from "lucide-react";
import { useTranslation } from "react-i18next";
import {
  getDashboardOverview,
  type DashboardActivity,
  type DashboardOverview,
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

function activityLabel(activity: DashboardActivity): string {
  if (activity.type === "assessment") return "Assessment";
  if (activity.type === "tutoring") return "Tutoring";
  return activity.type.replaceAll("_", " ");
}

export default function DashboardPage() {
  const { t } = useTranslation();
  const [overview, setOverview] = useState<DashboardOverview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    getDashboardOverview()
      .then((data) => {
        if (!cancelled) {
          setOverview(data);
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
  const cards = useMemo(
    () => [
      {
        label: t("Sessions"),
        value: totals?.total_sessions ?? 0,
        icon: Activity,
      },
      {
        label: t("Assessments"),
        value: totals?.assessments ?? 0,
        icon: PenLine,
      },
      {
        label: t("Tutoring"),
        value: totals?.tutoring_sessions ?? 0,
        icon: Users,
      },
      {
        label: t("Running"),
        value: totals?.running ?? 0,
        icon: Loader2,
      },
    ],
    [t, totals],
  );

  return (
    <main className="h-full overflow-y-auto bg-[var(--background)]">
      <div className="mx-auto flex w-full max-w-[1080px] flex-col gap-6 px-6 py-8">
        <header className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-[12px] font-semibold uppercase tracking-[0.12em] text-[var(--muted-foreground)]">
              {t("Teacher Dashboard")}
            </p>
            <h1 className="mt-2 text-[28px] font-semibold tracking-tight text-[var(--foreground)]">
              {t("Class activity")}
            </h1>
            <p className="mt-2 max-w-[680px] text-[14px] leading-6 text-[var(--muted-foreground)]">
              {t("Review recent assessments, tutoring sessions, and Knowledge Pack usage.")}
            </p>
          </div>
          <Link
            href="/dashboard/student"
            className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--card)] px-4 py-2 text-[13px] font-medium text-[var(--foreground)] transition hover:border-[var(--foreground)]"
          >
            {t("Open student progress")}
            <ArrowRight size={15} />
          </Link>
        </header>

        {error && (
          <div className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-[13px] text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
            {error}
          </div>
        )}

        <section className="grid gap-3 md:grid-cols-4">
          {cards.map((card) => (
            <div
              key={card.label}
              className="rounded-lg border border-[var(--border)] bg-[var(--card)] px-4 py-3"
            >
              <div className="flex items-center justify-between gap-3">
                <span className="text-[12px] font-medium text-[var(--muted-foreground)]">
                  {card.label}
                </span>
                <card.icon size={16} className="text-[var(--muted-foreground)]" />
              </div>
              <div className="mt-3 text-[28px] font-semibold text-[var(--foreground)]">
                {loading ? "-" : card.value}
              </div>
            </div>
          ))}
        </section>

        <section className="grid gap-5 lg:grid-cols-[1fr_320px]">
          <div>
            <div className="mb-3 flex items-center justify-between">
              <h2 className="text-[16px] font-semibold text-[var(--foreground)]">
                {t("Recent activity")}
              </h2>
              {loading && (
                <span className="flex items-center gap-2 text-[12px] text-[var(--muted-foreground)]">
                  <Loader2 size={13} className="animate-spin" />
                  {t("Loading")}
                </span>
              )}
            </div>
            <div className="overflow-hidden rounded-lg border border-[var(--border)]">
              {(overview?.recent_activity ?? []).length > 0 ? (
                overview?.recent_activity.map((activity) => {
                  const reviewHref =
                    activity.type === "assessment" && activity.review_ref
                      ? `/${activity.review_ref}`
                      : null;
                  return (
                    <article
                      key={activity.id}
                      className="border-b border-[var(--border)] bg-[var(--card)] px-4 py-3 last:border-b-0"
                    >
                      <div className="flex flex-wrap items-start justify-between gap-3">
                        <div className="min-w-0 flex-1">
                          {reviewHref ? (
                            <Link
                              href={reviewHref}
                              className="text-[14px] font-medium text-[var(--foreground)] underline-offset-4 hover:underline"
                            >
                              {activity.title || t("Untitled session")}
                            </Link>
                          ) : (
                            <div className="text-[14px] font-medium text-[var(--foreground)]">
                              {activity.title || t("Untitled session")}
                            </div>
                          )}
                          <div className="mt-1 text-[12px] text-[var(--muted-foreground)]">
                            {t(activityLabel(activity))} - {activity.status} -{" "}
                            {formatTime(activity.timestamp)}
                          </div>
                          {activity.assessment_summary && (
                            <div className="mt-2 text-[12px] text-[var(--muted-foreground)]">
                              {t("Score")}: {activity.assessment_summary.score_percent}% -{" "}
                              {activity.assessment_summary.correct_count}/
                              {activity.assessment_summary.total_questions}
                            </div>
                          )}
                          {activity.summary && (
                            <p className="mt-2 line-clamp-2 text-[13px] leading-5 text-[var(--muted-foreground)]">
                              {activity.summary}
                            </p>
                          )}
                        </div>
                        {activity.knowledge_bases.length > 0 && (
                          <div className="flex flex-wrap justify-end gap-1">
                            {activity.knowledge_bases.map((kb) => (
                              <span
                                key={`${activity.id}-${kb}`}
                                className="rounded-md bg-[var(--muted)] px-2 py-1 text-[11px] text-[var(--muted-foreground)]"
                              >
                                {kb}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    </article>
                  );
                })
              ) : (
                <div className="bg-[var(--card)] px-4 py-10 text-center text-[13px] text-[var(--muted-foreground)]">
                  {loading
                    ? t("Loading activity...")
                    : t("No learning activity yet. Generate an assessment or start a tutoring chat.")}
                </div>
              )}
            </div>
          </div>

          <aside>
            <h2 className="mb-3 text-[16px] font-semibold text-[var(--foreground)]">
              {t("Knowledge Packs")}
            </h2>
            <div className="rounded-lg border border-[var(--border)] bg-[var(--card)]">
              {(overview?.knowledge_packs ?? []).length > 0 ? (
                overview?.knowledge_packs.map((pack) => (
                  <div
                    key={pack.name}
                    className="flex items-center justify-between border-b border-[var(--border)] px-4 py-3 last:border-b-0"
                  >
                    <div className="flex min-w-0 items-center gap-2">
                      <BookOpen size={15} className="shrink-0 text-[var(--muted-foreground)]" />
                      <span className="truncate text-[13px] font-medium text-[var(--foreground)]">
                        {pack.name}
                      </span>
                    </div>
                    <span className="flex items-center gap-1 text-[12px] text-[var(--muted-foreground)]">
                      <CheckCircle2 size={13} />
                      {pack.session_count}
                    </span>
                  </div>
                ))
              ) : (
                <div className="px-4 py-8 text-center text-[13px] text-[var(--muted-foreground)]">
                  {t("Knowledge Pack activity will appear here.")}
                </div>
              )}
            </div>
          </aside>
        </section>
      </div>
    </main>
  );
}
