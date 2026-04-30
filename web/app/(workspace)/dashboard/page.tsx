"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  ArrowRight,
  BookOpen,
  CheckCircle2,
  Filter,
  Loader2,
  PenLine,
  Search,
  Users,
} from "lucide-react";
import { useTranslation } from "react-i18next";
import {
  buildDashboardPrioritySummary,
  formatActivityStatusLabel,
  formatActivityTypeLabel,
} from "@/components/dashboard/dashboard-presenters";
import { TeacherInsightPanel } from "@/components/dashboard/TeacherInsightPanel";
import { CoreLoopVisibilityStrip } from "@/components/contest/CoreLoopVisibilityStrip";
import {
  getDashboardInsights,
  getDashboardOverview,
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
  const groupSummaries = insights?.small_groups ?? [];
  const cards = useMemo(
    () => [
      {
        label: t("Học sinh cần hỗ trợ"),
        value: insights?.students.length ?? 0,
        icon: Users,
      },
      {
        label: t("Gợi ý theo nhóm"),
        value: groupSummaries.length ?? 0,
        icon: BookOpen,
      },
      {
        label: t("Bài đánh giá gần đây"),
        value: totals?.assessments ?? 0,
        icon: PenLine,
      },
      {
        label: t("Phiên học đang mở"),
        value: totals?.running ?? 0,
        icon: Activity,
      },
    ],
    [groupSummaries.length, insights?.students.length, t, totals],
  );
  const activeFilterCount = [searchTerm, activityType, knowledgeBase, minScore].filter(Boolean).length;
  const nextActionLabel =
    insights?.students?.[0]?.recommended_actions?.[0]?.rationale ??
    (focusTopics.length > 0
      ? t("Ưu tiên xem lại chủ đề yếu nhất trước")
      : t("Mở phiên học hoặc bài đánh giá gần nhất để xác nhận bước hỗ trợ tiếp theo"));
  const recentActivity = overview?.recent_activity ?? [];
  const knowledgePackActivity = overview?.knowledge_packs ?? [];
  const prioritySummary = buildDashboardPrioritySummary({
    nextActionRationale: nextActionLabel,
    focusTopic: focusTopics[0]?.topic,
    masteredTopic: masteredTopics[0]?.topic,
  });
  const reviewSteps = [
    {
      title: t("Bước 1: Chọn học sinh cần xem ngay"),
      body: prioritySummary.priorityBody,
    },
    {
      title: t("Bước 2: Chốt chủ đề cần hỗ trợ"),
      body: prioritySummary.focusBody,
    },
    {
      title: t("Bước 3: Quyết định việc nên làm tiếp"),
      body: prioritySummary.strengthBody,
    },
  ];

  return (
    <main className="h-full overflow-y-auto bg-[var(--background)]">
      <div className="mx-auto flex w-full max-w-[1180px] flex-col gap-6 px-4 py-8 sm:px-6">
        <header className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-5 shadow-sm">
          <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="text-[12px] font-semibold uppercase tracking-[0.12em] text-[var(--muted-foreground)]">
                {t("Bảng điều khiển giáo viên")}
              </p>
              <h1 className="mt-2 text-[28px] font-semibold tracking-tight text-[var(--foreground)]">
                {t("Hôm nay giáo viên nên quyết định gì trước?")}
              </h1>
              <p className="mt-2 max-w-[680px] text-[14px] leading-6 text-[var(--muted-foreground)]">
                {t("Đi theo đúng thứ tự: xem học sinh nào đang vướng, chốt chủ đề cần hỗ trợ, rồi mới quyết định bước can thiệp tiếp theo cho lớp.")}
              </p>
            </div>
            <Link
              href="/dashboard/student"
              className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--background)] px-4 py-2 text-[13px] font-medium text-[var(--foreground)] transition hover:border-[var(--foreground)]"
            >
              {t("Xem tiến độ từng học sinh")}
              <ArrowRight size={15} />
            </Link>
          </div>
          <div className="mt-4">
            <CoreLoopVisibilityStrip
              currentStep="Diagnosis"
              nextStep="Intervention"
              helperText={t("Màn hình này giúp giáo viên nối kết quả học tập với bước can thiệp tiếp theo; hệ thống chỉ gợi ý, giáo viên là người quyết định.")}
            />
          </div>
          <div className="mt-4 rounded-2xl border border-[var(--border)] bg-[var(--background)]/60 p-4">
            <div className="flex flex-col gap-2 md:flex-row md:items-start md:justify-between">
              <div>
                <div className="text-[12px] font-semibold uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
                  {t("Bước giáo viên nên đi theo trên màn hình này")}
                </div>
                <p className="mt-1 max-w-[640px] text-[13px] leading-6 text-[var(--muted-foreground)]">
                  {t("Mỗi ô dưới đây trả lời một câu hỏi: cần xem ai trước, đang vướng ở đâu, và nên làm gì tiếp ngay trong buổi học này.")}
                </p>
              </div>
              <div className="rounded-full bg-[var(--card)] px-3 py-1 text-[12px] text-[var(--muted-foreground)]">
                {t("Ưu tiên quyết định trước, xem số liệu sau")}
              </div>
            </div>
            <div className="mt-4 grid gap-3 md:grid-cols-3">
              {reviewSteps.map((step) => (
                <div key={step.title} className="rounded-xl bg-[var(--card)] px-4 py-3 shadow-sm">
                  <div className="text-[11px] uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
                    {step.title}
                  </div>
                  <div className="mt-2 text-[13px] font-medium text-[var(--foreground)]">{step.body}</div>
                </div>
              ))}
            </div>
          </div>
        </header>

        <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          {cards.map((card) => (
            <div
              key={card.label}
              className="rounded-2xl border border-[var(--border)] bg-[var(--card)] px-4 py-4 shadow-sm"
            >
              <div className="flex items-center justify-between gap-3">
                <span className="text-[12px] font-medium text-[var(--muted-foreground)]">
                  {card.label}
                </span>
                <card.icon size={16} className="text-[var(--muted-foreground)]" />
              </div>
              <div className="mt-3 text-[30px] font-semibold text-[var(--foreground)]">
                {loading ? "-" : card.value}
              </div>
            </div>
          ))}
        </section>

        {error && (
          <div className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-[13px] text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
            {t("Failed to load teacher dashboard")}: {error}
          </div>
        )}

        <section className="grid gap-4 xl:grid-cols-[1.35fr_0.85fr]">
          <TeacherInsightPanel insights={insights} />

          <aside className="space-y-4">
            <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-4 shadow-sm">
              <div className="text-[12px] font-semibold uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
                {prioritySummary.priorityTitle}
              </div>
              <div className="mt-2 text-[15px] font-semibold text-[var(--foreground)]">
                {prioritySummary.priorityBody}
              </div>
            </div>

            <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-4 shadow-sm">
              <div className="flex items-center justify-between gap-3">
                <h2 className="text-[14px] font-semibold text-[var(--foreground)]">
                  {t("Chủ đề cần hỗ trợ")}
                </h2>
                <BookOpen size={15} className="text-[var(--muted-foreground)]" />
              </div>
              <div className="mt-3 space-y-2">
                {focusTopics.length > 0 ? (
                  focusTopics.map((topic) => (
                    <div
                      key={`focus-${topic.topic}`}
                      className="flex items-center justify-between rounded-xl bg-[var(--background)] px-3 py-3"
                    >
                      <span className="text-[13px] text-[var(--foreground)]">{topic.topic}</span>
                      <span className="rounded-full bg-rose-50 px-2.5 py-1 text-[11px] font-medium text-rose-700">
                        {topic.incorrect_count}
                      </span>
                    </div>
                  ))
                ) : (
                  <div className="rounded-xl bg-[var(--background)] px-3 py-4 text-[12px] text-[var(--muted-foreground)]">
                    {loading ? t("Đang tải") : t("Chưa có chủ đề cần chú ý")}
                  </div>
                )}
              </div>
            </div>

            <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-4 shadow-sm">
              <h2 className="text-[14px] font-semibold text-[var(--foreground)]">
                {t("Chủ đề lớp đang làm tốt")}
              </h2>
              <div className="mt-3 space-y-2">
                {masteredTopics.length > 0 ? (
                  masteredTopics.map((topic) => (
                    <div
                      key={`mastered-${topic.topic}`}
                      className="flex items-center justify-between rounded-xl bg-[var(--background)] px-3 py-3"
                    >
                      <span className="text-[13px] text-[var(--foreground)]">{topic.topic}</span>
                      <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-[11px] font-medium text-emerald-700">
                        {topic.correct_count}
                      </span>
                    </div>
                  ))
                ) : (
                  <div className="rounded-xl bg-[var(--background)] px-3 py-4 text-[12px] text-[var(--muted-foreground)]">
                    {loading ? t("Đang tải") : t("Chưa có điểm mạnh nổi bật")}
                  </div>
                )}
              </div>
            </div>

            <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-4 shadow-sm">
              <h2 className="text-[14px] font-semibold text-[var(--foreground)]">
                {t("Gợi ý nhóm")}
              </h2>
              <div className="mt-3 space-y-2">
                {groupSummaries.length > 0 ? (
                  groupSummaries.map((group) => (
                    <div
                      key={`${group.topic}:${group.diagnosis_type}`}
                      className="rounded-xl bg-[var(--background)] px-3 py-3"
                    >
                      <div className="flex items-center justify-between gap-3">
                        <span className="text-[13px] font-medium text-[var(--foreground)]">{group.topic}</span>
                        <span className="rounded-full bg-[var(--muted)] px-2.5 py-1 text-[11px] text-[var(--muted-foreground)]">
                          {t("{{count}} học sinh", { count: group.student_ids.length })}
                        </span>
                      </div>
                      <div className="mt-1 text-[12px] text-[var(--muted-foreground)]">
                        {group.reason_trace?.teacher_review_note ?? t("Nên xử lý theo một hướng chung để tiết kiệm thời gian trên lớp.")}
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="rounded-xl bg-[var(--background)] px-3 py-4 text-[12px] text-[var(--muted-foreground)]">
                    {t("Chưa có nhóm học sinh nào cần gộp để can thiệp chung.")}
                  </div>
                )}
              </div>
            </div>
          </aside>
        </section>

        <section className="grid gap-4 lg:grid-cols-[0.9fr_1.1fr]">
          <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-4 shadow-sm">
            <div className="flex items-center justify-between gap-3">
              <h2 className="text-[16px] font-semibold text-[var(--foreground)]">
                {t("Số liệu lớp để tham khảo sau khi đã chốt ưu tiên")}
              </h2>
              <PenLine size={16} className="text-[var(--muted-foreground)]" />
            </div>
            <p className="mt-1 text-[13px] text-[var(--muted-foreground)]">
              {t("Dùng phần này để kiểm tra nhanh bức tranh chung của lớp sau khi giáo viên đã quyết định học sinh và chủ đề cần hỗ trợ trước.")}
            </p>
            <div className="mt-4 grid gap-3 sm:grid-cols-3">
              <div className="rounded-xl bg-[var(--background)] px-3 py-3">
                <div className="text-[12px] text-[var(--muted-foreground)]">{t("Điểm trung bình")}</div>
                <div className="mt-2 text-[24px] font-semibold text-[var(--foreground)]">
                  {loading ? "-" : `${analytics?.assessment_trend.average_score_percent ?? 0}%`}
                </div>
              </div>
              <div className="rounded-xl bg-[var(--background)] px-3 py-3">
                <div className="text-[12px] text-[var(--muted-foreground)]">{t("Điểm gần nhất")}</div>
                <div className="mt-2 text-[18px] font-semibold text-[var(--foreground)]">
                  {loading ? "-" : `${analytics?.assessment_trend.latest_score_percent ?? 0}%`}
                </div>
              </div>
              <div className="rounded-xl bg-[var(--background)] px-3 py-3">
                <div className="text-[12px] text-[var(--muted-foreground)]">{t("Mức thay đổi")}</div>
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

          <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-4 shadow-sm">
            <div className="mb-3 flex items-center justify-between gap-3">
              <div className="flex items-center gap-2 text-[13px] font-medium text-[var(--muted-foreground)]">
                <Filter size={14} />
                {t("Lọc lịch sử hoạt động")}
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
                  {t("Xóa bộ lọc")}
                </button>
              )}
            </div>
            <div className="grid gap-3 lg:grid-cols-[1.2fr_0.8fr_0.8fr_0.6fr]">
              <label className="block">
                <span className="mb-1 block text-[12px] font-medium text-[var(--foreground)]">
                  {t("Tìm nhanh")}
                </span>
                <div className="flex items-center gap-2 rounded-md border border-[var(--border)] bg-[var(--background)] px-3 py-2">
                  <Search size={14} className="text-[var(--muted-foreground)]" />
                  <input
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    placeholder={t("Tìm theo tiêu đề, tóm tắt, gói kiến thức")}
                    className="w-full bg-transparent text-[13px] outline-none"
                  />
                </div>
              </label>

              <label className="block">
                <span className="mb-1 block text-[12px] font-medium text-[var(--foreground)]">
                  {t("Loại hoạt động")}
                </span>
                <select
                  value={activityType}
                  onChange={(e) => setActivityType(e.target.value)}
                  className="w-full rounded-md border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px]"
                >
                  <option value="">{t("Tất cả hoạt động")}</option>
                  <option value="assessment">{t("Bài đánh giá")}</option>
                  <option value="tutoring">{t("Phiên học với gia sư")}</option>
                </select>
              </label>

              <label className="block">
                <span className="mb-1 block text-[12px] font-medium text-[var(--foreground)]">
                  {t("Gói kiến thức")}
                </span>
                <input
                  value={knowledgeBase}
                  onChange={(e) => setKnowledgeBase(e.target.value)}
                  placeholder={t("ví dụ: dai-so-10")}
                  className="w-full rounded-md border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px]"
                />
              </label>

              <label className="block">
                <span className="mb-1 block text-[12px] font-medium text-[var(--foreground)]">
                  {t("Từ mức điểm")}
                </span>
                <select
                  value={minScore}
                  onChange={(e) => setMinScore(e.target.value)}
                  className="w-full rounded-md border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px]"
                >
                  <option value="">{t("Mọi mức điểm")}</option>
                  <option value="50">50%+</option>
                  <option value="70">70%+</option>
                  <option value="80">80%+</option>
                  <option value="90">90%+</option>
                </select>
              </label>
            </div>
          </div>
        </section>

        <section className="grid gap-5 lg:grid-cols-[1fr_320px]">
          <div>
            <div className="mb-3 flex items-center justify-between">
              <h2 className="text-[16px] font-semibold text-[var(--foreground)]">
                {t("Hoạt động gần đây")}
              </h2>
              {loading && (
                <span className="flex items-center gap-2 text-[12px] text-[var(--muted-foreground)]">
              <Loader2 size={13} className="animate-spin" />
                  {t("Đang tải")}
                </span>
              )}
            </div>
            <div className="overflow-hidden rounded-2xl border border-[var(--border)] shadow-sm">
              {recentActivity.length > 0 ? (
                <div className="divide-y divide-[var(--border)] bg-[var(--card)]">
                  {recentActivity.map((activity) => {
                    const activityHref =
                      activity.type === "assessment" && activity.review_ref
                        ? `/${activity.review_ref}`
                        : activity.type === "tutoring" && activity.replay_ref
                          ? `/${activity.replay_ref}`
                          : null;
                    return (
                      <article key={activity.id} className="grid gap-2 px-4 py-3 md:grid-cols-[1.2fr_0.8fr_0.7fr]">
                        <div className="min-w-0">
                          {activityHref ? (
                            <Link
                              href={activityHref}
                              className="text-[13px] font-medium text-[var(--foreground)] underline-offset-4 hover:underline"
                            >
                              {activity.title || t("Phiên học chưa có tiêu đề")}
                            </Link>
                          ) : (
                            <div className="text-[13px] font-medium text-[var(--foreground)]">
                              {activity.title || t("Phiên học chưa có tiêu đề")}
                            </div>
                          )}
                          <div className="mt-1 text-[12px] text-[var(--muted-foreground)]">
                            {formatTime(activity.timestamp)}
                          </div>
                        </div>
                        <div className="text-[12px] text-[var(--muted-foreground)]">
                          {formatActivityTypeLabel(activity.type)}
                        </div>
                        <div className="text-[12px] text-[var(--muted-foreground)]">
                          {formatActivityStatusLabel(activity.status)}
                        </div>
                      </article>
                    );
                  })}
                </div>
              ) : (
                <div className="bg-[var(--card)] px-4 py-10 text-center text-[13px] text-[var(--muted-foreground)]">
                  {loading
                    ? t("Đang tải hoạt động...")
                    : activeFilterCount > 0
                      ? t("Không có hoạt động nào khớp với bộ lọc hiện tại.")
                      : t("Chưa có hoạt động học tập nào. Hãy tạo bài đánh giá hoặc bắt đầu một phiên học với gia sư.")}
                </div>
              )}
            </div>
          </div>

          <aside>
            <h2 className="mb-3 text-[16px] font-semibold text-[var(--foreground)]">
              {t("Gói kiến thức đang dùng")}
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
                    ? t("Không có hoạt động gói kiến thức nào khớp với bộ lọc hiện tại.")
                    : t("Hoạt động của gói kiến thức sẽ xuất hiện tại đây.")}
                </div>
              )}
            </div>
          </aside>
        </section>
      </div>
    </main>
  );
}
