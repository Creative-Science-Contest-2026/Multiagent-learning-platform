"use client";

import { useEffect, useState } from "react";
import {
  createRecommendationFeedback,
  type CreateRecommendationFeedbackRequest,
  type RecommendationFeedbackLabel,
  type RecommendationFeedbackRecord,
  updateRecommendationFeedback,
} from "@/lib/dashboard-api";

const FEEDBACK_LABELS: RecommendationFeedbackLabel[] = ["practical", "relevant", "too_generic"];

export function RecommendationFeedbackComposer({
  triggerLabel,
  defaultPayload,
  existingFeedback,
  onSaved,
  t,
}: {
  triggerLabel: string;
  defaultPayload: Omit<CreateRecommendationFeedbackRequest, "feedback_label" | "teacher_note">;
  existingFeedback?: RecommendationFeedbackRecord | null;
  onSaved: (record: RecommendationFeedbackRecord) => void;
  t: (value: string, options?: Record<string, string | number>) => string;
}) {
  const [open, setOpen] = useState(false);
  const [feedbackLabel, setFeedbackLabel] = useState<RecommendationFeedbackLabel>(
    existingFeedback?.feedback_label ?? "practical",
  );
  const [teacherNote, setTeacherNote] = useState(existingFeedback?.teacher_note ?? "");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    setFeedbackLabel(existingFeedback?.feedback_label ?? "practical");
    setTeacherNote(existingFeedback?.teacher_note ?? "");
  }, [existingFeedback]);

  async function handleSubmit() {
    setSubmitting(true);
    try {
      const record = existingFeedback
        ? await updateRecommendationFeedback(existingFeedback.id, {
            feedback_label: feedbackLabel,
            teacher_note: teacherNote,
          })
        : await createRecommendationFeedback({
            source_recommendation_id: defaultPayload.source_recommendation_id,
            target_type: defaultPayload.target_type,
            target_id: defaultPayload.target_id,
            feedback_label: feedbackLabel,
            teacher_note: teacherNote,
          });
      onSaved(record);
      setOpen(false);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="space-y-3">
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        className="inline-flex items-center rounded-full border border-[var(--border)] px-3 py-1 text-[12px] font-medium text-[var(--foreground)] transition hover:border-[var(--foreground)]"
      >
        {triggerLabel}
      </button>
      {open ? (
        <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-3">
          <div className="grid gap-3">
            <label className="text-[12px] text-[var(--muted-foreground)]">
              {t("Recommendation quality")}
              <select
                value={feedbackLabel}
                onChange={(e) => setFeedbackLabel(e.target.value as RecommendationFeedbackLabel)}
                className="mt-1 w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)]"
              >
                {FEEDBACK_LABELS.map((value) => (
                  <option key={value} value={value}>
                    {value}
                  </option>
                ))}
              </select>
            </label>
            <label className="text-[12px] text-[var(--muted-foreground)]">
              {t("Teacher note")}
              <textarea
                value={teacherNote}
                onChange={(e) => setTeacherNote(e.target.value)}
                className="mt-1 min-h-[80px] w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)]"
              />
            </label>
            <button
              type="button"
              disabled={submitting}
              onClick={handleSubmit}
              className="rounded-xl bg-[var(--foreground)] px-3 py-2 text-[13px] font-medium text-[var(--background)] disabled:opacity-60"
            >
              {submitting ? t("Saving...") : existingFeedback ? t("Update recommendation feedback") : t("Save recommendation feedback")}
            </button>
          </div>
        </div>
      ) : null}
    </div>
  );
}
