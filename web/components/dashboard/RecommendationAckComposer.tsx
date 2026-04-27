"use client";

import { useEffect, useState } from "react";
import {
  createRecommendationAck,
  type CreateRecommendationAckRequest,
  type RecommendationAckRecord,
  type RecommendationAckStatus,
  updateRecommendationAck,
} from "@/lib/dashboard-api";

const ACK_STATUSES: RecommendationAckStatus[] = ["accepted", "deferred", "dismissed", "completed"];

export function RecommendationAckComposer({
  triggerLabel,
  defaultPayload,
  existingAck,
  onSaved,
  t,
}: {
  triggerLabel: string;
  defaultPayload: Omit<CreateRecommendationAckRequest, "status" | "teacher_note">;
  existingAck?: RecommendationAckRecord | null;
  onSaved: (record: RecommendationAckRecord) => void;
  t: (value: string, options?: Record<string, string | number>) => string;
}) {
  const [open, setOpen] = useState(false);
  const [status, setStatus] = useState<RecommendationAckStatus>(existingAck?.status ?? "accepted");
  const [teacherNote, setTeacherNote] = useState(existingAck?.teacher_note ?? "");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    setStatus(existingAck?.status ?? "accepted");
    setTeacherNote(existingAck?.teacher_note ?? "");
  }, [existingAck]);

  async function handleSubmit() {
    setSubmitting(true);
    try {
      const record = existingAck
        ? await updateRecommendationAck(existingAck.id, {
            status,
            teacher_note: teacherNote,
          })
        : await createRecommendationAck({
            source_recommendation_id: defaultPayload.source_recommendation_id,
            target_type: defaultPayload.target_type,
            target_id: defaultPayload.target_id,
            status,
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
              {t("Recommendation status")}
              <select
                value={status}
                onChange={(e) => setStatus(e.target.value as RecommendationAckStatus)}
                className="mt-1 w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)]"
              >
                {ACK_STATUSES.map((value) => (
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
              {submitting ? t("Saving...") : existingAck ? t("Update acknowledgement") : t("Save acknowledgement")}
            </button>
          </div>
        </div>
      ) : null}
    </div>
  );
}
