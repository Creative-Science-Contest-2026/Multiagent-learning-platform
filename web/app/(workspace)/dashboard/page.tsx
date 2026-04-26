"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { Activity, ArrowRight, BookOpen, CheckCircle2, Filter, Loader2, PenLine, Search, Users } from "lucide-react";
import { useTranslation } from "react-i18next";
import { TeacherInsightPanel } from "@/components/dashboard/TeacherInsightPanel";
import {
  getDashboardInsights,
  getDashboardOverview,
  type DashboardActivity,
  type DashboardInsights,
  type DashboardOverview,
  type DashboardOverviewFilters,
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

function scoreDeltaTone(value: number): string {
  if (value > 0) return "text-emerald-600";
  if (value < 0) return "text-rose-600";
  return "text-[var(--muted-foreground)]";
}

export default function DashboardPage() {
  const { t } = useTranslation();
  const [overview, setOverview] = useState<DashboardOverview | null>(null);
  const [insights, setInsights] = useState<DashboardInsights | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [activityType, setActivityType] = useState("");
  const [knowledgeBase, setKnowledgeBase] = useState("");
  const [minScore, setMinScore] = useState("");

  const filters = useMemo<DashboardOverviewFilters>(
    () => ({
      type: activityType || undefined,
      knowledge_base: knowledgeBase || undefined,
      search: searchTerm.trim() || undefined,
      min_score: minScore ? Number(minScore) : undefined,
    }),
    [activityType, knowledgeBase, minScore, searchTerm],
  );

  useEffect(() => {
    let cancelled = false;
    Promise.all([
      getDashboardOverview(50, filters),
      getDashboardInsights(50, { knowledge_base: filters.knowledge_base }),
    ])
      .then(([overviewData, insightData]) => {
        if (!cancelled) {
          setOverview(overviewData);
          setInsights(insightData);
          setError(null);
        }
      })
      .catch((err) => {
        if (!cancelled) setError(err instanceof Error ? err.message : String(err));
      })
      .finally(() => undefined);
    return () => {
      cancelled = true;
    };
  }, [filters]);

  const loading = overview === null;

  const totals = overview?.totals;
  const analytics = overview?.analytics;
  const focusTopics = analytics?.learning_signals.focus_topics ?? [];
  const masteredTopics = analytics?.learning_signals.mastered_topics ?? [];
  const cards = useMemo(
    () => [
      {
        label: t("Students with signals"),
        value: insights?.students.length ?? 0,
        icon: Users,
      },
      {
        label: t("Small-group actions"),
        value: insights?.small_groups.length ?? 0,
        icon: BookOpen,
      },
      {
        label: t("Recent assessments"),
        value: totals?.assessments ?? 0,
        icon: PenLine,
      },
      {
        label: t("Active sessions"),
        value: totals?.running ?? 0,
        icon: Activity,
      },
    ],
    [insights, t, totals],
  );
  const activeFilterCount = [searchTerm, activityType, knowledgeBase, minScore].filter(Boolean).length;
  const nextActionLabel =
    insights?.students?.[0]?.recommended_actions?.[0]?.rationale ??
    (focusTopics.length > 0
      ? t("Review the weakest topics first")
      : t("Open the latest session and confirm the student is ready for the next pack"));
  const recentActivity = overview?.recent_activity ?? [];
  const knowledgePackActivity = overview?.knowledge_packs ?? [];

  return (
    <main className="h-full overflow-y-auto bg-[var(--background)]">
      <div className="mx-auto flex w-full max-w-[1080px] flex-col gap-6 px-6 py-8">
        <header className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-5 shadow-sm">
          <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="text-[12px] font-semibold uppercase tracking-[0.12em] text-[var(--muted-foreground)]">
                {t("Teacher Workflow")}
              </p>
              <h1 className="mt-2 text-[28px] font-semibold tracking-tight text-[var(--foreground)]">
                {t("Observed, diagnosed, and ready for action")}
              </h1>
              <p className="mt-2 max-w-[680px] text-[14px] leading-6 text-[var(--muted-foreground)]">
                {t("Review observed facts first, then decide the clearest next classroom move for each student or group.")}
              </p>
            </div>
            <Link
              href="/dashboard/student"
              className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--background)] px-4 py-2 text-[13px] font-medium text-[var(--foreground)] transition hover:border-[var(--foreground)]"
            >
              {t("Open student progress")}
              <ArrowRight size={15} />
            </Link>
          </div>
          <div className="mt-4 grid gap-3 md:grid-cols-3">
            <div className="rounded-xl bg-[var(--background)] px-4 py-3">
              <div className="text-[11px] uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
                {t("Next Steps")}
              </div>
              <div className="mt-1 text-[13px] font-medium text-[var(--foreground)]">
                {nextActionLabel}
              </div>
            </div>
            <div className="rounded-xl bg-[var(--background)] px-4 py-3">
              <div className="text-[11px] uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
                {t("Needs attention")}
              </div>
              <div className="mt-1 text-[13px] font-medium text-[var(--foreground)]">
                {focusTopics.length > 0 ? focusTopics[0]?.topic : t("No weak topics yet")}
              </div>
            </div>
            <div className="rounded-xl bg-[var(--background)] px-4 py-3">
              <div className="text-[11px] uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
                {t("Strong areas")}
              </div>
              <div className="mt-1 text-[13px] font-medium text-[var(--foreground)]">
                {masteredTopics.length > 0 ? masteredTopics[0]?.topic : t("No strong topics yet")}
              </div>
            </div>
          </div>
        </header>

        <TeacherInsightPanel insights={insights} />

        <section className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-4 shadow-sm">
          <div className="mb-3 flex items-center justify-between gap-3">
            <div className="flex items-center gap-2 text-[13px] font-medium text-[var(--muted-foreground)]">
              <Filter size={14} />
              {t("History filters")}
            </div>
            {activeFilterCount > 0 && (
              <button
                onClick={() => {
                  setSearchTerm("");
                  setActivityType("");
                  setKnowledgeBase("");
                  setMinScore("");
                }}
                className="text-[12px] text-[var(--muted-foreground)] underline-offset-4 hover:text-[var(--foreground)] hover:underline"
              >
                {t("Clear filters")}
              </button>
            )}
          </div>
          <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
            <label className="block">
              <span className="mb-1 block text-[12px] font-medium text-[var(--foreground)]">
                {t("Search")}
              </span>
              <div className="flex items-center gap-2 rounded-md border border-[var(--border)] bg-[var(--background)] px-3 py-2">
                <Search size={14} className="text-[var(--muted-foreground)]" />
                <input
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder={t("Search title, summary, KB")}
                  className="w-full bg-transparent text-[13px] outline-none"
                />
              </div>
            </label>

            <label className="block">
              <span className="mb-1 block text-[12px] font-medium text-[var(--foreground)]">
                {t("Activity type")}
              </span>
              <select
                value={activityType}
                onChange={(e) => setActivityType(e.target.value)}
                className="w-full rounded-md border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px]"
              >
                <option value="">{t("All activity")}</option>
                <option value="assessment">{t("Assessment")}</option>
                <option value="tutoring">{t("Tutoring")}</option>
              </select>
            </label>

            <label className="block">
              <span className="mb-1 block text-[12px] font-medium text-[var(--foreground)]">
                {t("Knowledge Pack")}
              </span>
              <input
                value={knowledgeBase}
                onChange={(e) => setKnowledgeBase(e.target.value)}
                placeholder={t("e.g. algebra-pack")}
                className="w-full rounded-md border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px]"
              />
            </label>

            <label className="block">
              <span className="mb-1 block text-[12px] font-medium text-[var(--foreground)]">
                {t("Minimum score")}
              </span>
              <select
                value={minScore}
                onChange={(e) => setMinScore(e.target.value)}
                className="w-full rounded-md border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px]"
              >
                <option value="">{t("Any score")}</option>
                <option value="50">50%+</option>
                <option value="70">70%+</option>
                <option value="80">80%+</option>
                <option value="90">90%+</option>
              </select>
            </label>
          </div>
        </section>

        {error && (
          <div className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-[13px] text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
            {t("Failed to load teacher dashboard")}: {error}
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

        <section className="grid gap-4 lg:grid-cols-3">
            <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-4 shadow-sm">
            <div className="flex items-center justify-between gap-3">
              <h2 className="text-[16px] font-semibold text-[var(--foreground)]">
                {t("Engagement")}
              </h2>
              <Activity size={16} className="text-[var(--muted-foreground)]" />
            </div>
            <div className="mt-4 grid gap-3 sm:grid-cols-3 lg:grid-cols-1">
              <div className="rounded-lg bg-[var(--background)] px-3 py-3">
                <div className="text-[12px] text-[var(--muted-foreground)]">{t("Active days")}</div>
                <div className="mt-2 text-[24px] font-semibold text-[var(--foreground)]">
                  {loading ? "-" : analytics?.engagement.active_days ?? 0}
                </div>
              </div>
              <div className="rounded-lg bg-[var(--background)] px-3 py-3">
                <div className="text-[12px] text-[var(--muted-foreground)]">{t("Streak")}</div>
                <div className="mt-2 text-[24px] font-semibold text-[var(--foreground)]">
                  {loading ? "-" : analytics?.engagement.streak_days ?? 0}
                </div>
              </div>
              <div className="rounded-lg bg-[var(--background)] px-3 py-3">
                <div className="text-[12px] text-[var(--muted-foreground)]">{t("Knowledge Packs used")}</div>
                <div className="mt-2 text-[24px] font-semibold text-[var(--foreground)]">
                  {loading ? "-" : analytics?.engagement.knowledge_packs_used ?? 0}
                </div>
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-4 shadow-sm">
            <div className="flex items-center justify-between gap-3">
              <h2 className="text-[16px] font-semibold text-[var(--foreground)]">
                {t("Assessment trend")}
              </h2>
              <PenLine size={16} className="text-[var(--muted-foreground)]" />
            </div>
            <div className="mt-4 space-y-3">
              <div className="rounded-lg bg-[var(--background)] px-3 py-3">
                <div className="text-[12px] text-[var(--muted-foreground)]">{t("Average score")}</div>
                <div className="mt-2 text-[24px] font-semibold text-[var(--foreground)]">
                  {loading ? "-" : `${analytics?.assessment_trend.average_score_percent ?? 0}%`}
                </div>
              </div>
              <div className="grid gap-3 sm:grid-cols-2">
                <div className="rounded-lg bg-[var(--background)] px-3 py-3">
                  <div className="text-[12px] text-[var(--muted-foreground)]">{t("Latest score")}</div>
                  <div className="mt-2 text-[18px] font-semibold text-[var(--foreground)]">
                    {loading ? "-" : `${analytics?.assessment_trend.latest_score_percent ?? 0}%`}
                  </div>
                </div>
                <div className="rounded-lg bg-[var(--background)] px-3 py-3">
                  <div className="text-[12px] text-[var(--muted-foreground)]">{t("Score delta")}</div>
                  <div
                    className={`mt-2 text-[18px] font-semibold ${scoreDeltaTone(
                      analytics?.assessment_trend.score_delta ?? 0,
                    )}`}
                  >
                    {loading
                      ? "-"
                      : `${(analytics?.assessment_trend.score_delta ?? 0) > 0 ? "+" : ""}${analytics?.assessment_trend.score_delta ?? 0}`}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-4 shadow-sm">
            <div className="flex items-center justify-between gap-3">
              <h2 className="text-[16px] font-semibold text-[var(--foreground)]">
                {t("Learning signals")}
              </h2>
              <BookOpen size={16} className="text-[var(--muted-foreground)]" />
            </div>
            <div className="mt-4 grid gap-4">
              <div>
                <div className="text-[12px] font-medium text-[var(--muted-foreground)]">
                  {t("Needs attention")}
                </div>
                <div className="mt-2 flex flex-wrap gap-2">
                  {focusTopics.length > 0 ? (
                    focusTopics.map((topic) => (
                      <span
                        key={`focus-${topic.topic}`}
                        className="rounded-full bg-rose-50 px-3 py-1 text-[12px] text-rose-700"
                      >
                        {topic.topic}
                      </span>
                    ))
                  ) : (
                    <span className="text-[13px] text-[var(--muted-foreground)]">
                      {loading ? t("Loading") : t("No weak topics yet")}
                    </span>
                  )}
                </div>
              </div>
              <div>
                <div className="text-[12px] font-medium text-[var(--muted-foreground)]">
                  {t("Strong areas")}
                </div>
                <div className="mt-2 flex flex-wrap gap-2">
                  {masteredTopics.length > 0 ? (
                    masteredTopics.map((topic) => (
                      <span
                        key={`mastered-${topic.topic}`}
                        className="rounded-full bg-emerald-50 px-3 py-1 text-[12px] text-emerald-700"
                      >
                        {topic.topic}
                      </span>
                    ))
                  ) : (
                    <span className="text-[13px] text-[var(--muted-foreground)]">
                      {loading ? t("Loading") : t("No strong topics yet")}
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
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
            <div className="overflow-hidden rounded-2xl border border-[var(--border)] shadow-sm">
              {recentActivity.length > 0 ? (
                recentActivity.map((activity) => {
                  const activityHref =
                    activity.type === "assessment" && activity.review_ref
                      ? `/${activity.review_ref}`
                      : activity.type === "tutoring" && activity.replay_ref
                        ? `/${activity.replay_ref}`
                        : null;
                  return (
                    <article
                      key={activity.id}
                      className="border-b border-[var(--border)] bg-[var(--card)] px-4 py-3 last:border-b-0"
                    >
                      <div className="flex flex-wrap items-start justify-between gap-3">
                        <div className="min-w-0 flex-1">
                          {activityHref ? (
                            <Link
                              href={activityHref}
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
                    : activeFilterCount > 0
                      ? t("No activity matches the current filters.")
                      : t("No learning activity yet. Generate an assessment or start a tutoring chat.")}
                </div>
              )}
            </div>
          </div>

          <aside>
            <h2 className="mb-3 text-[16px] font-semibold text-[var(--foreground)]">
              {t("Knowledge Packs")}
            </h2>
            <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)] shadow-sm">
              {knowledgePackActivity.length > 0 ? (
                knowledgePackActivity.map((pack) => (
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
                  {activeFilterCount > 0
                    ? t("No Knowledge Pack activity matches the current filters.")
                    : t("Knowledge Pack activity will appear here.")}
                </div>
              )}
            </div>
          </aside>
        </section>
      </div>
    </main>
  );
}
