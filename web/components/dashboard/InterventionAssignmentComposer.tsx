"use client";

import { useState } from "react";
import {
  createInterventionAssignment,
  type CreateInterventionAssignmentRequest,
  type InterventionAssignmentRecord,
  type InterventionAssignmentType,
  type TeacherActionRecord,
} from "@/lib/dashboard-api";

const ASSIGNMENT_TYPES: InterventionAssignmentType[] = [
  "practice_set",
  "reteach_session",
  "prerequisite_review",
  "small_group_activity",
];

function defaultAssignmentType(actionType: TeacherActionRecord["action_type"]): InterventionAssignmentType {
  if (actionType === "small_group_remediation") return "small_group_activity";
  if (actionType === "review_prerequisite") return "prerequisite_review";
  if (actionType === "scaffolded_practice") return "practice_set";
  return "reteach_session";
}

function defaultTitle(action: TeacherActionRecord): string {
  return `${action.topic}: ${action.action_type.replaceAll("_", " ")}`;
}

export function InterventionAssignmentComposer({
  triggerLabel,
  teacherAction,
  onCreated,
  t,
}: {
  triggerLabel: string;
  teacherAction: TeacherActionRecord;
  onCreated: (record: InterventionAssignmentRecord) => void;
  t: (value: string, options?: Record<string, string | number>) => string;
}) {
  const [open, setOpen] = useState(false);
  const [assignmentType, setAssignmentType] = useState<InterventionAssignmentType>(
    defaultAssignmentType(teacherAction.action_type),
  );
  const [title, setTitle] = useState(defaultTitle(teacherAction));
  const [teacherNote, setTeacherNote] = useState(teacherAction.teacher_instruction);
  const [practiceNote, setPracticeNote] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit() {
    setSubmitting(true);
    try {
      const payload: CreateInterventionAssignmentRequest = {
        teacher_action_id: teacherAction.id,
        assignment_type: assignmentType,
        title,
        teacher_note: teacherNote,
        practice_note: practiceNote,
      };
      const record = await createInterventionAssignment(payload);
      onCreated(record);
      setOpen(false);
      setAssignmentType(defaultAssignmentType(teacherAction.action_type));
      setTitle(defaultTitle(teacherAction));
      setTeacherNote(teacherAction.teacher_instruction);
      setPracticeNote("");
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
              {t("Assignment type")}
              <select
                value={assignmentType}
                onChange={(e) => setAssignmentType(e.target.value as InterventionAssignmentType)}
                className="mt-1 w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)]"
              >
                {ASSIGNMENT_TYPES.map((value) => (
                  <option key={value} value={value}>
                    {value}
                  </option>
                ))}
              </select>
            </label>
            <label className="text-[12px] text-[var(--muted-foreground)]">
              {t("Title")}
              <input
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="mt-1 w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)]"
              />
            </label>
            <label className="text-[12px] text-[var(--muted-foreground)]">
              {t("Teacher note")}
              <textarea
                value={teacherNote}
                onChange={(e) => setTeacherNote(e.target.value)}
                className="mt-1 min-h-[80px] w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)]"
              />
            </label>
            <label className="text-[12px] text-[var(--muted-foreground)]">
              {t("Practice note")}
              <textarea
                value={practiceNote}
                onChange={(e) => setPracticeNote(e.target.value)}
                className="mt-1 min-h-[80px] w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)]"
              />
            </label>
            <button
              type="button"
              disabled={submitting || title.trim().length === 0 || teacherNote.trim().length === 0 || practiceNote.trim().length === 0}
              onClick={handleSubmit}
              className="rounded-xl bg-[var(--foreground)] px-3 py-2 text-[13px] font-medium text-[var(--background)] disabled:opacity-60"
            >
              {submitting ? t("Saving...") : t("Create assignment")}
            </button>
          </div>
        </div>
      ) : null}
    </div>
  );
}
