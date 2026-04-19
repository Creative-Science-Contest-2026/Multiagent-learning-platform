"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { ArrowLeft, CheckCircle2, Loader2, XCircle } from "lucide-react";
import { useTranslation } from "react-i18next";
import { getAssessmentReview, type AssessmentReview } from "@/lib/dashboard-api";
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

export default function AssessmentReviewPage() {
  const { t } = useTranslation();
  const { sessionId } = useParams<{ sessionId: string }>();
  const [review, setReview] = useState<AssessmentReview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    getAssessmentReview(sessionId)
      .then((data) => {
        if (!cancelled) {
          setReview(data);
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

        <header>
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
        </header>

        <ProgressIndicator
          totalQuestions={review.summary.total_questions}
          correctCount={review.summary.correct_count}
          incorrectCount={review.summary.incorrect_count}
          scorePercent={review.summary.score_percent}
          knowledgeBases={review.knowledge_bases}
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

        <h2 className="mt-8 text-[18px] font-semibold text-[var(--foreground)]">
          {t("Question-by-Question Breakdown")}
        </h2>

        <section className="space-y-4">
          {review.results.length > 0 ? (
            review.results.map((result, index) => (
              <article
                key={result.question_id || `${index}`}
                className="rounded-lg border border-[var(--border)] bg-[var(--card)] p-4"
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
                <div className="mt-3 grid gap-2 text-[13px] text-[var(--muted-foreground)] md:grid-cols-2">
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
