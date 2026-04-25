"use client";

import { useTranslation } from "react-i18next";
import { Calendar, Clock, Target, TrendingUp } from "lucide-react";

export interface LearningJourneySummaryProps {
  timestamp: number;
  estimatedTimeSpent?: number;
  masteredTopics?: string[];
  nextTopics?: string[];
}

export function LearningJourneySummary({
  timestamp,
  estimatedTimeSpent,
  masteredTopics = [],
  nextTopics = [],
}: LearningJourneySummaryProps) {
  const { t } = useTranslation();

  const formatTime = (value: number): string => {
    if (!value) return "";
    const timestamp_ms = value < 10_000_000_000 ? value * 1000 : value;
    return new Intl.DateTimeFormat(undefined, {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(new Date(timestamp_ms));
  };

  const formatDuration = (minutes?: number): string => {
    if (!minutes) return t("Unknown");
    if (minutes < 60) return `${minutes} ${t("min")}`;
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
  };

  return (
    <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-6 shadow-sm">
      <div className="flex items-center gap-2 mb-4">
        <TrendingUp size={18} className="text-blue-600" />
        <h3 className="text-[14px] font-semibold text-[var(--foreground)]">
          {t("Session recap")}
        </h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {/* Session Date */}
        <div className="flex items-start gap-3 p-3 rounded-md bg-[var(--muted)]/50">
          <Calendar size={16} className="text-[var(--muted-foreground)] mt-0.5 shrink-0" />
          <div className="min-w-0">
            <p className="text-[11px] text-[var(--muted-foreground)] uppercase tracking-wide">
              {t("Session Date")}
            </p>
            <p className="text-[12px] font-medium text-[var(--foreground)] mt-1">
              {formatTime(timestamp)}
            </p>
          </div>
        </div>

        {/* Time Spent */}
        <div className="flex items-start gap-3 p-3 rounded-md bg-[var(--muted)]/50">
          <Clock size={16} className="text-[var(--muted-foreground)] mt-0.5 shrink-0" />
          <div className="min-w-0">
            <p className="text-[11px] text-[var(--muted-foreground)] uppercase tracking-wide">
              {t("Time Spent")}
            </p>
            <p className="text-[12px] font-medium text-[var(--foreground)] mt-1">
              {formatDuration(estimatedTimeSpent)}
            </p>
          </div>
        </div>

        {/* Session Status */}
        <div className="flex items-start gap-3 p-3 rounded-md bg-[var(--muted)]/50">
          <Target size={16} className="text-[var(--muted-foreground)] mt-0.5 shrink-0" />
          <div className="min-w-0">
            <p className="text-[11px] text-[var(--muted-foreground)] uppercase tracking-wide">
              {t("Session")}
            </p>
            <p className="text-[12px] font-medium text-[var(--foreground)] mt-1">
              {t("Learning in progress")}
            </p>
          </div>
        </div>
      </div>

      <div className="mb-6 rounded-xl bg-[var(--background)] px-4 py-3 text-[13px] text-[var(--muted-foreground)]">
        {nextTopics.length > 0
          ? t("Next Steps")
          : t("Review your incorrect answers")}
      </div>

      {/* Mastered Topics */}
      {masteredTopics.length > 0 && (
        <div className="mb-4 p-4 rounded-md bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800">
          <p className="text-[12px] font-semibold text-emerald-900 dark:text-emerald-300 mb-2">
            {t("Topics You've Mastered")}
          </p>
          <div className="flex flex-wrap gap-2">
            {masteredTopics.map((topic) => (
              <span
                key={topic}
                className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-medium bg-emerald-100 text-emerald-800 dark:bg-emerald-900/50 dark:text-emerald-200"
              >
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-600" />
                {topic}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Recommended Topics */}
      {nextTopics.length > 0 && (
        <div className="p-4 rounded-md bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800">
          <p className="text-[12px] font-semibold text-blue-900 dark:text-blue-300 mb-2">
            {t("Recommended Topics to Explore")}
          </p>
          <div className="flex flex-wrap gap-2">
            {nextTopics.map((topic) => (
              <span
                key={topic}
                className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-200"
              >
                <span className="w-1.5 h-1.5 rounded-full bg-blue-600" />
                {topic}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
