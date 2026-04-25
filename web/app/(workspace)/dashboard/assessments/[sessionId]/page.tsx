"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { ArrowLeft, CheckCircle2, Download, Loader2, XCircle } from "lucide-react";
import { useTranslation } from "react-i18next";
import {
  downloadAssessmentExportPdf,
  getAssessmentAnalysis,
  getAssessmentReview,
  type AssessmentAnalysis,
  type AssessmentReview,
} from "@/lib/dashboard-api";
import { ProgressIndicator } from "@/components/assessment/ProgressIndicator";
import { LearningJourneySummary } from "@/components/assessment/LearningJourneySummary";

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

function formatDuration(seconds?: number | null): string {
  if (!seconds || seconds <= 0) return "";
  if (seconds < 60) return `${seconds}s`;
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  if (!remainingSeconds) return `${minutes}m`;
  return `${minutes}m ${remainingSeconds}s`;
}

export default function AssessmentReviewPage() {
  const { t } = useTranslation();
  const { sessionId } = useParams<{ sessionId: string }>();
  const [review, setReview] = useState<AssessmentReview | null>(null);
  const [analysis, setAnalysis] = useState<AssessmentAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [exporting, setExporting] = useState(false);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    Promise.all([getAssessmentReview(sessionId), getAssessmentAnalysis(sessionId)])
      .then(([reviewData, analysisData]) => {
        if (!cancelled) {
          setReview(reviewData);
          setAnalysis(analysisData);
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
  }, [sessionId]);

  const handleExportPdf = async () => {
    setExporting(true);
    try {
      const blob = await downloadAssessmentExportPdf(sessionId);
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `${sessionId}-assessment-report.pdf`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setExporting(false);
    }
  };

  if (loading) {
    return (
      <main className="flex h-full items-center justify-center bg-[var(--background)] text-[var(--muted-foreground)]">
        <Loader2 size={18} className="mr-2 animate-spin" />
        {t("Loading assessment review...")}
      </main>
    );
  }

  if (error) {
    return (
      <main className="h-full overflow-y-auto bg-[var(--background)] px-6 py-8">
        <div className="mx-auto max-w-[900px] rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
          {t("Failed to load assessment review")}: {error}
        </div>
      </main>
    );
  }

  if (!review) {
    return (
      <main className="h-full overflow-y-auto bg-[var(--background)] px-6 py-8">
        <div className="mx-auto max-w-[900px] text-sm text-[var(--muted-foreground)]">
          {t("Assessment review not found.")}
        </div>
      </main>
    );
  }

  return (
    <main className="h-full overflow-y-auto bg-[var(--background)]">
      <div className="mx-auto flex w-full max-w-[1080px] flex-col gap-6 px-6 py-8">
        <Link
          href="/dashboard"
          className="inline-flex w-fit items-center gap-2 text-[13px] text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
        >
          <ArrowLeft size={15} />
          {t("Back to Dashboard")}
        </Link>

        <header className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
          <div>
            <p className="text-[12px] font-semibold uppercase tracking-[0.12em] text-[var(--muted-foreground)]">
              {t("Assessment Review")}
            </p>
            <h1 className="mt-2 text-[28px] font-semibold tracking-tight text-[var(--foreground)]">
              {review.title || t("Untitled assessment")}
            </h1>
            <p className="mt-2 text-[14px] text-[var(--muted-foreground)]">
              {formatTime(review.timestamp)} - {review.status}
            </p>
            {review.knowledge_bases.length > 0 && (
              <div className="mt-3 flex flex-wrap gap-2">
                {review.knowledge_bases.map((kb) => (
                  <span
                    key={kb}
                    className="rounded-md bg-[var(--muted)] px-2 py-1 text-[12px] text-[var(--muted-foreground)]"
                  >
                    {kb}
                  </span>
                ))}
              </div>
            )}
          </div>

          <button
            type="button"
            onClick={handleExportPdf}
            disabled={exporting}
            className="inline-flex items-center justify-center gap-2 rounded-md border border-[var(--border)] bg-[var(--card)] px-3 py-2 text-[13px] font-medium text-[var(--foreground)] transition-colors hover:bg-[var(--muted)] disabled:opacity-50"
          >
            {exporting ? <Loader2 size={15} className="animate-spin" /> : <Download size={15} />}
            {exporting ? t("Exporting PDF...") : t("Export PDF")}
          </button>
        </header>

        <section className="grid gap-3 md:grid-cols-3">
          <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-4 shadow-sm">
            <div className="text-[11px] uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
              {t("Next Steps")}
            </div>
            <div className="mt-1 text-[13px] font-medium text-[var(--foreground)]">
              {review.summary.score_percent < 75
                ? t("Review challenging topics")
                : t("Take another assessment to track improvement")}
            </div>
          </div>
          <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-4 shadow-sm">
            <div className="text-[11px] uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
              {t("Knowledge Pack")}
            </div>
            <div className="mt-1 text-[13px] font-medium text-[var(--foreground)]">
              {review.knowledge_bases[0] || t("Assessment review not found.")}
            </div>
          </div>
          <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-4 shadow-sm">
            <div className="text-[11px] uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
              {t("Overall Score")}
            </div>
            <div className="mt-1 text-[13px] font-medium text-[var(--foreground)]">
              {review.summary.score_percent}%
            </div>
          </div>
        </section>

        <ProgressIndicator
          totalQuestions={review.summary.total_questions}
          correctCount={review.summary.correct_count}
          incorrectCount={review.summary.incorrect_count}
          scorePercent={review.summary.score_percent}
          knowledgeBases={review.knowledge_bases}
          analysis={analysis}
        />

        <LearningJourneySummary
          timestamp={review.timestamp}
          estimatedTimeSpent={review.summary.estimated_time_spent}
          masteredTopics={
            review.summary.score_percent >= 75
              ? review.knowledge_bases
              : undefined
          }
          nextTopics={
            review.summary.score_percent < 90 && review.knowledge_bases.length > 0
              ? review.knowledge_bases
              : undefined
          }
        />

        {(review.summary.estimated_time_spent || review.summary.average_time_per_question) && (
          <section className="grid gap-3 md:grid-cols-2">
            {review.summary.estimated_time_spent ? (
              <div className="rounded-lg border border-[var(--border)] bg-[var(--card)] p-4">
                <p className="text-[12px] font-medium uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
                  {t("Time spent")}
                </p>
                <p className="mt-2 text-[20px] font-semibold text-[var(--foreground)]">
                  {formatDuration(review.summary.estimated_time_spent)}
                </p>
              </div>
            ) : null}
            {review.summary.average_time_per_question ? (
              <div className="rounded-lg border border-[var(--border)] bg-[var(--card)] p-4">
                <p className="text-[12px] font-medium uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
                  {t("Average per question")}
                </p>
                <p className="mt-2 text-[20px] font-semibold text-[var(--foreground)]">
                  {formatDuration(review.summary.average_time_per_question)}
                </p>
              </div>
            ) : null}
          </section>
        )}

        <h2 className="mt-8 text-[18px] font-semibold text-[var(--foreground)]">
          {t("Question-by-Question Breakdown")}
        </h2>

        <section className="space-y-4">
          {review.results.length > 0 ? (
            review.results.map((result, index) => (
              <article
                key={result.question_id || `${index}`}
                className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-4 shadow-sm"
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="text-[12px] text-[var(--muted-foreground)]">
                      {t("Question")} {index + 1}
                    </p>
                    <h2 className="mt-1 text-[15px] font-medium leading-6 text-[var(--foreground)]">
                      {result.question}
                    </h2>
                  </div>
                  {result.is_correct ? (
                    <CheckCircle2 size={19} className="shrink-0 text-emerald-600" />
                  ) : (
                    <XCircle size={19} className="shrink-0 text-red-600" />
                  )}
                </div>
                <div className="mt-3 grid gap-2 rounded-xl bg-[var(--background)] p-3 text-[13px] text-[var(--muted-foreground)] md:grid-cols-2">
                  <p>
                    <span className="font-medium text-[var(--foreground)]">
                      {t("Student answer")}:
                    </span>{" "}
                    {result.user_answer || t("(blank)")}
                  </p>
                  <p>
                    <span className="font-medium text-[var(--foreground)]">
                      {t("Correct answer")}:
                    </span>{" "}
                    {result.correct_answer || t("(not recorded)")}
                  </p>
                  {result.duration_seconds ? (
                    <p>
                      <span className="font-medium text-[var(--foreground)]">
                        {t("Response time")}:
                      </span>{" "}
                      {formatDuration(result.duration_seconds)}
                    </p>
                  ) : null}
                </div>
              </article>
            ))
          ) : (
            <div className="rounded-lg border border-[var(--border)] bg-[var(--card)] p-6 text-center text-[13px] text-[var(--muted-foreground)]">
              {t("This assessment session does not have question-level review data yet.")}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
