"use client";

import { useState } from "react";
import { ChevronDown, TrendingUp } from "lucide-react";
import { useTranslation } from "react-i18next";

export interface ProgressIndicatorProps {
  totalQuestions: number;
  correctCount: number;
  incorrectCount: number;
  scorePercent: number;
  knowledgeBases: string[];
}

export function ProgressIndicator({
  totalQuestions,
  correctCount,
  incorrectCount,
  scorePercent,
  knowledgeBases,
}: ProgressIndicatorProps) {
  const { t } = useTranslation();
  const [expanded, setExpanded] = useState(false);

  // Score rating
  const getScoreRating = (score: number): { label: string; color: string } => {
    if (score >= 90) return { label: t("Excellent"), color: "text-emerald-600" };
    if (score >= 75) return { label: t("Good"), color: "text-blue-600" };
    if (score >= 60) return { label: t("Fair"), color: "text-yellow-600" };
    return { label: t("Needs improvement"), color: "text-red-600" };
  };

  const rating = getScoreRating(scorePercent);
  const percentageCorrect = totalQuestions > 0 ? (correctCount / totalQuestions) * 100 : 0;

  return (
    <div className="space-y-4">
      {/* Main Progress Card */}
      <div className="rounded-lg border border-[var(--border)] bg-gradient-to-br from-[var(--card)] to-[var(--card)]/50 p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <TrendingUp size={20} className={rating.color} />
            <h3 className="text-[14px] font-semibold text-[var(--foreground)]">
              {t("Learning Progress")}
            </h3>
          </div>
          <span className={`text-[12px] font-medium px-2 py-1 rounded ${rating.color} opacity-80`}>
            {rating.label}
          </span>
        </div>

        {/* Main Progress Bar */}
        <div className="mb-4">
          <div className="flex justify-between mb-2">
            <span className="text-[12px] text-[var(--muted-foreground)]">
              {t("Overall Score")}
            </span>
            <span className="text-[14px] font-semibold text-[var(--foreground)]">
              {scorePercent}%
            </span>
          </div>
          <div className="w-full h-3 rounded-full bg-[var(--muted)] overflow-hidden">
            <div
              className={`h-full transition-all duration-300 ${
                scorePercent >= 75 ? "bg-emerald-500" : scorePercent >= 60 ? "bg-yellow-500" : "bg-red-500"
              }`}
              style={{ width: `${scorePercent}%` }}
            />
          </div>
        </div>

        {/* Question-by-Question Progress */}
        <div className="grid grid-cols-3 gap-3 mb-4">
          <div className="rounded-md bg-[var(--muted)] p-3">
            <p className="text-[11px] text-[var(--muted-foreground)] uppercase tracking-wide">
              {t("Total")}
            </p>
            <p className="text-[18px] font-semibold text-[var(--foreground)] mt-1">
              {totalQuestions}
            </p>
          </div>
          <div className="rounded-md bg-emerald-50 p-3 dark:bg-emerald-950/30">
            <p className="text-[11px] text-emerald-700 dark:text-emerald-300 uppercase tracking-wide">
              {t("Correct")}
            </p>
            <p className="text-[18px] font-semibold text-emerald-600 mt-1">
              {correctCount}
            </p>
          </div>
          <div className="rounded-md bg-red-50 p-3 dark:bg-red-950/30">
            <p className="text-[11px] text-red-700 dark:text-red-300 uppercase tracking-wide">
              {t("Incorrect")}
            </p>
            <p className="text-[18px] font-semibold text-red-600 mt-1">
              {incorrectCount}
            </p>
          </div>
        </div>

        {/* KB Context Section */}
        {knowledgeBases.length > 0 && (
          <div className="border-t border-[var(--border)] pt-4">
            <p className="text-[12px] font-medium text-[var(--foreground)] mb-2">
              {t("Knowledge Bases Used")}
            </p>
            <div className="flex flex-wrap gap-2">
              {knowledgeBases.map((kb) => (
                <span
                  key={kb}
                  className="inline-flex items-center gap-1 rounded-full bg-blue-100 px-3 py-1 text-[11px] font-medium text-blue-700 dark:bg-blue-900/40 dark:text-blue-300"
                >
                  <span className="w-2 h-2 rounded-full bg-blue-500" />
                  {kb}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Expandable Recommendations */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full rounded-lg border border-[var(--border)] bg-[var(--card)] p-4 hover:bg-[var(--card)]/80 transition-colors"
      >
        <div className="flex items-center justify-between">
          <h3 className="text-[13px] font-semibold text-[var(--foreground)]">
            {t("Personalized Recommendations")}
          </h3>
          <ChevronDown
            size={18}
            className={`transition-transform ${expanded ? "rotate-180" : ""} text-[var(--muted-foreground)]`}
          />
        </div>
        {!expanded && (
          <p className="text-[12px] text-[var(--muted-foreground)] mt-1">
            {t("Click to view recommendations based on your performance")}
          </p>
        )}
      </button>

      {expanded && (
        <div className="rounded-lg border border-[var(--border)] bg-[var(--card)] p-4 space-y-3">
          {scorePercent < 75 && (
            <div className="p-3 rounded-md bg-yellow-50 dark:bg-yellow-950/30 border border-yellow-200 dark:border-yellow-800">
              <p className="text-[12px] font-medium text-yellow-900 dark:text-yellow-300">
                {t("Review challenging topics")}
              </p>
              <p className="text-[11px] text-yellow-800 dark:text-yellow-400 mt-1">
                {t("Focus on the incorrect questions above to strengthen your understanding.")}
              </p>
            </div>
          )}

          {scorePercent >= 75 && scorePercent < 90 && (
            <div className="p-3 rounded-md bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800">
              <p className="text-[12px] font-medium text-blue-900 dark:text-blue-300">
                {t("Great progress! Keep pushing.")}
              </p>
              <p className="text-[11px] text-blue-800 dark:text-blue-400 mt-1">
                {t("Review a few tricky questions to reach excellence.")}
              </p>
            </div>
          )}

          {scorePercent >= 90 && (
            <div className="p-3 rounded-md bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800">
              <p className="text-[12px] font-medium text-emerald-900 dark:text-emerald-300">
                {t("Excellent performance!")}
              </p>
              <p className="text-[11px] text-emerald-800 dark:text-emerald-400 mt-1">
                {t("You have mastered this topic. Consider exploring advanced materials.")}
              </p>
            </div>
          )}

          {knowledgeBases.length > 0 && (
            <div className="p-3 rounded-md bg-purple-50 dark:bg-purple-950/30 border border-purple-200 dark:border-purple-800">
              <p className="text-[12px] font-medium text-purple-900 dark:text-purple-300">
                {t("Related knowledge")}
              </p>
              <p className="text-[11px] text-purple-800 dark:text-purple-400 mt-1">
                {t("Review the {{count}} knowledge bases above to reinforce learning.", {
                  count: knowledgeBases.length,
                })}
              </p>
            </div>
          )}

          <div className="p-3 rounded-md bg-[var(--muted)]">
            <p className="text-[12px] font-medium text-[var(--foreground)]">
              {t("Next Steps")}
            </p>
            <ul className="text-[11px] text-[var(--muted-foreground)] mt-2 space-y-1 list-disc list-inside">
              <li>{t("Review your incorrect answers")}</li>
              <li>{t("Study related concepts in the knowledge bases")}</li>
              <li>{t("Take another assessment to track improvement")}</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
