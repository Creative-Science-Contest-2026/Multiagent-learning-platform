"use client";

import { useEffect, useState } from "react";
import {
  createTeacherOverride,
  type CreateTeacherOverrideRequest,
  type TeacherOverrideReason,
  type TeacherOverrideRecord,
  type TeacherSelectedMove,
  updateTeacherOverride,
} from "@/lib/dashboard-api";

const OVERRIDE_REASONS: TeacherOverrideReason[] = [
  "different_strategy",
  "needs_more_context",
  "not_classroom_fit",
];

const SELECTED_MOVES: TeacherSelectedMove[] = [
  "reteach_concept",
  "scaffolded_practice",
  "review_prerequisite",
  "small_group_remediation",
];

export function TeacherOverrideComposer({
  triggerLabel,
  defaultPayload,
  existingOverride,
  onSaved,
  t,
}: {
  triggerLabel: string;
  defaultPayload: Omit<CreateTeacherOverrideRequest, "override_reason" | "teacher_selected_move" | "teacher_note">;
  existingOverride?: TeacherOverrideRecord | null;
  onSaved: (record: TeacherOverrideRecord) => void;
  t: (value: string, options?: Record<string, string | number>) => string;
}) {
  const [open, setOpen] = useState(false);
  const [overrideReason, setOverrideReason] = useState<TeacherOverrideReason>(
    existingOverride?.override_reason ?? "different_strategy",
  );
  const [teacherSelectedMove, setTeacherSelectedMove] = useState<TeacherSelectedMove>(
    existingOverride?.teacher_selected_move ?? "reteach_concept",
  );
  const [teacherNote, setTeacherNote] = useState(existingOverride?.teacher_note ?? "");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    setOverrideReason(existingOverride?.override_reason ?? "different_strategy");
    setTeacherSelectedMove(existingOverride?.teacher_selected_move ?? "reteach_concept");
    setTeacherNote(existingOverride?.teacher_note ?? "");
  }, [existingOverride]);

  async function handleSubmit() {
    setSubmitting(true);
    try {
      const record = existingOverride
        ? await updateTeacherOverride(existingOverride.id, {
            override_reason: overrideReason,
            teacher_selected_move: teacherSelectedMove,
            teacher_note: teacherNote,
          })
        : await createTeacherOverride({
            source_recommendation_id: defaultPayload.source_recommendation_id,
            target_type: defaultPayload.target_type,
            target_id: defaultPayload.target_id,
            override_reason: overrideReason,
            teacher_selected_move: teacherSelectedMove,
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
              {t("Override reason")}
              <select
                value={overrideReason}
                onChange={(e) => setOverrideReason(e.target.value as TeacherOverrideReason)}
                className="mt-1 w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)]"
              >
                {OVERRIDE_REASONS.map((value) => (
                  <option key={value} value={value}>
                    {value}
                  </option>
                ))}
              </select>
            </label>
            <label className="text-[12px] text-[var(--muted-foreground)]">
              {t("Teacher-selected move")}
              <select
                value={teacherSelectedMove}
                onChange={(e) => setTeacherSelectedMove(e.target.value as TeacherSelectedMove)}
                className="mt-1 w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)]"
              >
                {SELECTED_MOVES.map((value) => (
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
              {submitting ? t("Saving...") : existingOverride ? t("Update teacher override") : t("Save teacher override")}
            </button>
          </div>
        </div>
      ) : null}
    </div>
  );
}
