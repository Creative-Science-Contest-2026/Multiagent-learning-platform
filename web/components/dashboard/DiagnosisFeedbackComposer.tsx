"use client";

import { useEffect, useState } from "react";
import {
  createDiagnosisFeedback,
  type CreateDiagnosisFeedbackRequest,
  type DiagnosisFeedbackLabel,
  type DiagnosisFeedbackRecord,
  updateDiagnosisFeedback,
} from "@/lib/dashboard-api";

const FEEDBACK_LABELS: DiagnosisFeedbackLabel[] = ["helpful", "wrong", "incomplete"];

export function DiagnosisFeedbackComposer({
  triggerLabel,
  defaultPayload,
  existingFeedback,
  onSaved,
  t,
}: {
  triggerLabel: string;
  defaultPayload: Omit<CreateDiagnosisFeedbackRequest, "feedback_label" | "teacher_note">;
  existingFeedback?: DiagnosisFeedbackRecord | null;
  onSaved: (record: DiagnosisFeedbackRecord) => void;
  t: (value: string, options?: Record<string, string | number>) => string;
}) {
  const [open, setOpen] = useState(false);
  const [feedbackLabel, setFeedbackLabel] = useState<DiagnosisFeedbackLabel>(
    existingFeedback?.feedback_label ?? "helpful",
  );
  const [teacherNote, setTeacherNote] = useState(existingFeedback?.teacher_note ?? "");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    setFeedbackLabel(existingFeedback?.feedback_label ?? "helpful");
    setTeacherNote(existingFeedback?.teacher_note ?? "");
  }, [existingFeedback]);

  async function handleSubmit() {
    setSubmitting(true);
    try {
      const record = existingFeedback
        ? await updateDiagnosisFeedback(existingFeedback.id, {
            feedback_label: feedbackLabel,
            teacher_note: teacherNote,
          })
        : await createDiagnosisFeedback({
            student_id: defaultPayload.student_id,
            source_topic: defaultPayload.source_topic,
            source_diagnosis_type: defaultPayload.source_diagnosis_type,
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
              {t("Diagnosis feedback")}
              <select
                value={feedbackLabel}
                onChange={(e) => setFeedbackLabel(e.target.value as DiagnosisFeedbackLabel)}
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
              {submitting ? t("Saving...") : existingFeedback ? t("Update diagnosis feedback") : t("Save diagnosis feedback")}
            </button>
          </div>
        </div>
      ) : null}
    </div>
  );
}
