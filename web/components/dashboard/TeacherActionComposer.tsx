"use client";

import { useState } from "react";
import {
  createTeacherAction,
  type CreateTeacherActionRequest,
  type TeacherActionPriority,
  type TeacherActionRecord,
  type TeacherActionType,
} from "@/lib/dashboard-api";

const ACTION_TYPES: TeacherActionType[] = [
  "reteach_concept",
  "scaffolded_practice",
  "review_prerequisite",
  "small_group_remediation",
];

const PRIORITIES: TeacherActionPriority[] = ["low", "medium", "high"];

export function TeacherActionComposer({
  triggerLabel,
  defaultPayload,
  onCreated,
  t,
}: {
  triggerLabel: string;
  defaultPayload: Omit<CreateTeacherActionRequest, "teacher_instruction" | "priority" | "action_type"> & {
    defaultActionType: TeacherActionType;
  };
  onCreated: (record: TeacherActionRecord) => void;
  t: (value: string, options?: Record<string, string | number>) => string;
}) {
  const [open, setOpen] = useState(false);
  const [actionType, setActionType] = useState<TeacherActionType>(defaultPayload.defaultActionType);
  const [topic, setTopic] = useState(defaultPayload.topic);
  const [teacherInstruction, setTeacherInstruction] = useState("");
  const [priority, setPriority] = useState<TeacherActionPriority>("medium");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit() {
    setSubmitting(true);
    try {
      const record = await createTeacherAction({
        target_type: defaultPayload.target_type,
        target_id: defaultPayload.target_id,
        source_recommendation_id: defaultPayload.source_recommendation_id,
        action_type: actionType,
        topic,
        teacher_instruction: teacherInstruction,
        priority,
      });
      onCreated(record);
      setOpen(false);
      setTeacherInstruction("");
      setPriority("medium");
      setActionType(defaultPayload.defaultActionType);
      setTopic(defaultPayload.topic);
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
              {t("Action type")}
              <select
                value={actionType}
                onChange={(e) => setActionType(e.target.value as TeacherActionType)}
                className="mt-1 w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)]"
              >
                {ACTION_TYPES.map((value) => (
                  <option key={value} value={value}>
                    {value}
                  </option>
                ))}
              </select>
            </label>
            <label className="text-[12px] text-[var(--muted-foreground)]">
              {t("Topic")}
              <input
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                className="mt-1 w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)]"
              />
            </label>
            <label className="text-[12px] text-[var(--muted-foreground)]">
              {t("Teacher instruction")}
              <textarea
                value={teacherInstruction}
                onChange={(e) => setTeacherInstruction(e.target.value)}
                className="mt-1 min-h-[96px] w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)]"
              />
            </label>
            <label className="text-[12px] text-[var(--muted-foreground)]">
              {t("Priority")}
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value as TeacherActionPriority)}
                className="mt-1 w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)]"
              >
                {PRIORITIES.map((value) => (
                  <option key={value} value={value}>
                    {value}
                  </option>
                ))}
              </select>
            </label>
            <button
              type="button"
              disabled={submitting || teacherInstruction.trim().length === 0}
              onClick={handleSubmit}
              className="rounded-xl bg-[var(--foreground)] px-3 py-2 text-[13px] font-medium text-[var(--background)] disabled:opacity-60"
            >
              {submitting ? t("Saving...") : t("Create action")}
            </button>
          </div>
        </div>
      ) : null}
    </div>
  );
}
