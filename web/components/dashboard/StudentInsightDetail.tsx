"use client";

import { useState } from "react";
import { DiagnosisFeedbackComposer } from "@/components/dashboard/DiagnosisFeedbackComposer";
import { InsightSectionLabel } from "@/components/dashboard/InsightSectionLabel";
import {
  type DiagnosisFeedbackRecord,
  type InterventionHistoryItem,
  type InterventionAssignmentRecord,
  type InterventionAssignmentStatus,
  type RecommendationAckRecord,
  type TeacherActionRecord,
  type TeacherActionStatus,
  type TeacherInsightStudent,
  updateInterventionAssignmentStatus,
  updateTeacherActionStatus,
} from "@/lib/dashboard-api";

function formatLatency(seconds: number | undefined): string | null {
  if (seconds == null) return null;
  if (seconds < 1) return `≈${Math.round(seconds * 1000)} ms`;
  return `${Math.round(seconds)} s`;
}

function formatEventTime(timestamp: number | undefined): string | null {
  if (!timestamp) return null;
  const value = timestamp > 10_000_000_000 ? timestamp : timestamp * 1000;
  return new Intl.DateTimeFormat(undefined, {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

function historyLabel(item: InterventionHistoryItem, t: (value: string, options?: Record<string, string | number>) => string): string {
  switch (item.item_type) {
    case "recommendation_ack":
      return t("Recommendation acknowledgement");
    case "teacher_action":
      return t("Teacher action");
    case "intervention_assignment":
      return t("Intervention assignment");
    case "diagnosis_feedback":
      return t("Diagnosis feedback");
    default:
      return item.item_type;
  }
}

export function StudentInsightDetail({
  student,
  t,
}: {
  student: TeacherInsightStudent | null;
  t: (value: string, options?: Record<string, string | number>) => string;
}) {
  const [diagnosisFeedback, setDiagnosisFeedback] = useState<DiagnosisFeedbackRecord | null>(
    student?.diagnosis_feedback ?? null,
  );
  const [teacherActions, setTeacherActions] = useState<TeacherActionRecord[]>(student?.teacher_actions ?? []);
  const [recommendationAck] = useState<RecommendationAckRecord | null>(student?.recommendation_ack ?? null);
  const [interventionAssignments, setInterventionAssignments] = useState<InterventionAssignmentRecord[]>(
    student?.intervention_assignments ?? [],
  );
  const [interventionHistory] = useState<InterventionHistoryItem[]>(student?.intervention_history ?? []);

  const diagnosis = student?.inferred[0];
  const recommendation = student?.recommended_actions[0];

  if (!student) {
    return (
      <section className="rounded-[28px] border border-dashed border-[var(--border)] bg-[var(--card)] px-5 py-8 text-center text-[13px] text-[var(--muted-foreground)]">
        {t("Choose a student from the dashboard to inspect evidence and next steps.")}
      </section>
    );
  }

  return (
    <section className="grid gap-4 xl:grid-cols-[1.15fr_0.85fr]">
      <div className="space-y-4">
        <section className="rounded-[28px] border border-[var(--border)] bg-[var(--card)] p-5 shadow-sm">
          <InsightSectionLabel eyebrow={t("Observed")} title={student.observed?.topic ?? t("No recent evidence")} />
          <div className="mt-4 grid gap-3 sm:grid-cols-3">
            <div className="rounded-2xl bg-[var(--muted)]/50 p-3 text-[12px] text-[var(--foreground)]">
              <div className="font-semibold text-[var(--muted-foreground)]">{t("Miss count")}</div>
              <div className="mt-2 text-[18px] font-semibold text-[var(--foreground)]">
                {student.observed?.miss_count ?? 0}
              </div>
            </div>
            <div className="rounded-2xl bg-[var(--muted)]/50 p-3 text-[12px] text-[var(--foreground)]">
              <div className="font-semibold text-[var(--muted-foreground)]">{t("Average latency")}</div>
              <div className="mt-2 text-[18px] font-semibold text-[var(--foreground)]">
                {formatLatency(student.observed?.avg_latency_seconds) ?? t("Unknown")}
              </div>
            </div>
            <div className="rounded-2xl bg-[var(--muted)]/50 p-3 text-[12px] text-[var(--foreground)]">
              <div className="font-semibold text-[var(--muted-foreground)]">{t("Confidence trend")}</div>
              <div className="mt-2 text-[18px] font-semibold text-[var(--foreground)]">
                {student.student_state?.confidence_trend ?? t("Unknown")}
              </div>
            </div>
          </div>
        </section>

        <section className="rounded-[28px] border border-[var(--border)] bg-[var(--card)] p-5 shadow-sm">
          <InsightSectionLabel
            eyebrow={t("Inferred")}
            title={diagnosis?.diagnosis_type ?? t("No diagnosis")}
            toneClassName="text-amber-700"
          >
            {t("Confidence: {{value}}", { value: diagnosis?.confidence_tag ?? "N/A" })}
          </InsightSectionLabel>
          <div className="mt-4 rounded-2xl bg-amber-50 p-4">
            <div className="text-[13px] font-medium text-[var(--foreground)]">
              {diagnosis?.topic ? t("Likely topic gap: {{topic}}", { topic: diagnosis.topic }) : t("No inferred topic")}
            </div>
            {diagnosis?.evidence?.length ? (
              <ul className="mt-3 space-y-2 text-[12px] text-[var(--muted-foreground)]">
                {diagnosis.evidence.map((fact) => (
                  <li key={`${student.student_id}-${fact}`}>• {fact}</li>
                ))}
              </ul>
            ) : (
              <div className="mt-3 text-[12px] text-[var(--muted-foreground)]">
                {t("No structured rationale was provided in the payload.")}
              </div>
            )}
            {diagnosis ? (
              <div className="mt-4">
                <DiagnosisFeedbackComposer
                  triggerLabel={diagnosisFeedback ? t("Update diagnosis feedback") : t("Review diagnosis")}
                  defaultPayload={{
                    student_id: student.student_id,
                    source_topic: diagnosis.topic,
                    source_diagnosis_type: diagnosis.diagnosis_type,
                  }}
                  existingFeedback={diagnosisFeedback}
                  onSaved={setDiagnosisFeedback}
                  t={t}
                />
              </div>
            ) : null}
            {diagnosisFeedback ? (
              <div className="mt-4 rounded-2xl border border-amber-200 bg-white/80 p-3 text-[12px] text-amber-900/80">
                <div className="font-medium">
                  {t("Diagnosis feedback: {{label}}", { label: diagnosisFeedback.feedback_label })}
                </div>
                {diagnosisFeedback.teacher_note ? (
                  <div className="mt-1 text-[12px] text-amber-900/80">{diagnosisFeedback.teacher_note}</div>
                ) : (
                  <div className="mt-1 text-[12px] text-amber-900/70">
                    {t("No teacher note was recorded for this diagnosis feedback.")}
                  </div>
                )}
              </div>
            ) : null}
          </div>
        </section>
      </div>

      <section className="rounded-[28px] border border-[var(--border)] bg-[var(--card)] p-5 shadow-sm">
        <InsightSectionLabel
          eyebrow={t("Teacher move")}
          title={recommendation?.action_type ?? t("No next move")}
          toneClassName="text-emerald-700"
        >
          {t("Use this as the next teacher move, not as an automatic intervention.")}
        </InsightSectionLabel>

        <div className="mt-4 rounded-2xl bg-emerald-50 p-4">
          <div className="text-[14px] font-medium text-[var(--foreground)]">
            {recommendation?.rationale ?? t("No recommendation available")}
          </div>
          <div className="mt-3 text-[12px] text-emerald-900/80">
            {diagnosis?.evidence?.[0]
              ? t("Why this move: {{reason}}", { reason: diagnosis.evidence[0] })
              : t("Why this move: based on the strongest recent learning signal.")}
          </div>
          <div className="mt-4 space-y-2 text-[12px] text-[var(--muted-foreground)]">
            <div>{t("Topic: {{topic}}", { topic: recommendation?.topic ?? diagnosis?.topic ?? t("Unknown") })}</div>
            <div>
              {t("Targets: {{count}} student(s)", {
                count: recommendation?.target_student_ids.length ?? 0,
              })}
            </div>
            {student.student_state?.support_level ? (
              <div>{t("Support level: {{value}}", { value: student.student_state.support_level })}</div>
            ) : null}
          </div>
        </div>
      </section>

      <section className="rounded-[28px] border border-[var(--border)] bg-[var(--card)] p-5 shadow-sm xl:col-span-2">
        <InsightSectionLabel
          eyebrow={t("Recommendation acknowledgement")}
          title={recommendationAck ? recommendationAck.status : t("No acknowledgement yet")}
        >
          {t("Teacher response to the recommendation before or alongside execution.")}
        </InsightSectionLabel>
        <div className="mt-4 rounded-2xl bg-[var(--muted)]/50 p-4 text-[13px] text-[var(--foreground)]">
          {recommendationAck ? (
            <>
              <div className="font-medium">{t("Current status: {{status}}", { status: recommendationAck.status })}</div>
              {recommendationAck.teacher_note ? (
                <div className="mt-2 text-[12px] text-[var(--muted-foreground)]">{recommendationAck.teacher_note}</div>
              ) : (
                <div className="mt-2 text-[12px] text-[var(--muted-foreground)]">
                  {t("No teacher note was recorded for this acknowledgement.")}
                </div>
              )}
            </>
          ) : (
            <div className="text-[13px] text-[var(--muted-foreground)]">
              {t("Acknowledge the recommendation from the dashboard overview to record the teacher response here.")}
            </div>
          )}
        </div>
      </section>

      <section className="rounded-[28px] border border-[var(--border)] bg-[var(--card)] p-5 shadow-sm xl:col-span-2">
        <InsightSectionLabel
          eyebrow={t("Teacher actions")}
          title={
            teacherActions.length
              ? t("{{count}} recorded actions", { count: teacherActions.length })
              : t("No actions yet")
          }
        />
        <div className="mt-4 space-y-3">
          {teacherActions.length ? (
            teacherActions.map((action) => (
              <div key={action.id} className="rounded-2xl bg-[var(--muted)]/50 p-4">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div>
                    <div className="text-[13px] font-medium text-[var(--foreground)]">{action.action_type}</div>
                    <div className="mt-1 text-[12px] text-[var(--muted-foreground)]">{action.topic}</div>
                  </div>
                  <select
                    value={action.status}
                    onChange={async (e) => {
                      const updated = await updateTeacherActionStatus(
                        action.id,
                        e.target.value as TeacherActionStatus,
                      );
                      setTeacherActions((current) =>
                        current.map((row) => (row.id === updated.id ? updated : row)),
                      );
                    }}
                    className="rounded-xl border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[12px] text-[var(--foreground)]"
                  >
                    <option value="planned">{t("planned")}</option>
                    <option value="done">{t("done")}</option>
                    <option value="dismissed">{t("dismissed")}</option>
                  </select>
                </div>
                <div className="mt-3 text-[13px] text-[var(--foreground)]">{action.teacher_instruction}</div>
                <div className="mt-2 text-[11px] text-[var(--muted-foreground)]">
                  {t("Priority: {{priority}}", { priority: action.priority })}
                </div>
              </div>
            ))
          ) : (
            <div className="rounded-2xl bg-[var(--muted)]/50 p-4 text-[13px] text-[var(--muted-foreground)]">
              {t("Create a teacher action from the dashboard overview to track a concrete remediation move here.")}
            </div>
          )}
        </div>
      </section>

      <section className="rounded-[28px] border border-[var(--border)] bg-[var(--card)] p-5 shadow-sm xl:col-span-2">
        <InsightSectionLabel
          eyebrow={t("Intervention assignments")}
          title={
            interventionAssignments.length
              ? t("{{count}} recorded assignments", { count: interventionAssignments.length })
              : t("No assignments yet")
          }
        />
        <div className="mt-4 space-y-3">
          {interventionAssignments.length ? (
            interventionAssignments.map((assignment) => (
              <div key={assignment.id} className="rounded-2xl bg-[var(--muted)]/50 p-4">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div>
                    <div className="text-[13px] font-medium text-[var(--foreground)]">{assignment.assignment_type}</div>
                    <div className="mt-1 text-[12px] text-[var(--muted-foreground)]">{assignment.title}</div>
                  </div>
                  <select
                    value={assignment.status}
                    onChange={async (e) => {
                      const updated = await updateInterventionAssignmentStatus(
                        assignment.id,
                        e.target.value as InterventionAssignmentStatus,
                      );
                      setInterventionAssignments((current) =>
                        current.map((row) => (row.id === updated.id ? updated : row)),
                      );
                    }}
                    className="rounded-xl border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[12px] text-[var(--foreground)]"
                  >
                    <option value="planned">{t("planned")}</option>
                    <option value="done">{t("done")}</option>
                    <option value="dismissed">{t("dismissed")}</option>
                  </select>
                </div>
                <div className="mt-3 text-[12px] text-[var(--muted-foreground)]">{assignment.topic}</div>
                <div className="mt-3 text-[13px] text-[var(--foreground)]">{assignment.teacher_note}</div>
                <div className="mt-2 text-[12px] text-[var(--muted-foreground)]">{assignment.practice_note}</div>
              </div>
            ))
          ) : (
            <div className="rounded-2xl bg-[var(--muted)]/50 p-4 text-[13px] text-[var(--muted-foreground)]">
              {t("Convert a teacher action into an intervention assignment from the dashboard overview to track a concrete remediation shell here.")}
            </div>
          )}
        </div>
      </section>

      <section className="rounded-[28px] border border-[var(--border)] bg-[var(--card)] p-5 shadow-sm xl:col-span-2">
        <InsightSectionLabel
          eyebrow={t("Intervention history")}
          title={
            interventionHistory.length
              ? t("{{count}} recorded steps", { count: interventionHistory.length })
              : t("No intervention history yet")
          }
        >
          {t("A descriptive timeline of teacher response, execution, assignment, and diagnosis review for this student.")}
        </InsightSectionLabel>
        <div className="mt-4 space-y-3">
          {interventionHistory.length ? (
            interventionHistory.map((item) => (
              <div key={item.id} className="rounded-2xl bg-[var(--muted)]/50 p-4">
                <div className="flex flex-wrap items-start justify-between gap-2">
                  <div>
                    <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[var(--muted-foreground)]">
                      {historyLabel(item, t)}
                    </div>
                    <div className="mt-1 text-[13px] font-medium text-[var(--foreground)]">{item.title}</div>
                    {item.topic ? (
                      <div className="mt-1 text-[12px] text-[var(--muted-foreground)]">
                        {t("Topic: {{topic}}", { topic: item.topic })}
                      </div>
                    ) : null}
                  </div>
                  <div className="rounded-full border border-[var(--border)] bg-[var(--background)] px-3 py-1 text-[11px] font-medium text-[var(--foreground)]">
                    {item.status}
                  </div>
                </div>
                <div className="mt-3 text-[13px] text-[var(--foreground)]">{item.detail}</div>
                <div className="mt-2 text-[11px] text-[var(--muted-foreground)]">
                  {formatEventTime(item.timestamp) ?? t("Unknown time")}
                </div>
              </div>
            ))
          ) : (
            <div className="rounded-2xl bg-[var(--muted)]/50 p-4 text-[13px] text-[var(--muted-foreground)]">
              {t("Recommendation acknowledgements, teacher actions, intervention assignments, and diagnosis feedback will appear here once recorded.")}
            </div>
          )}
        </div>
      </section>
    </section>
  );
}
