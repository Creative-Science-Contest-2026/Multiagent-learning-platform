"use client";

import Link from "next/link";
import { useState } from "react";
import { ArrowRight } from "lucide-react";
import { DiagnosisFeedbackComposer } from "@/components/dashboard/DiagnosisFeedbackComposer";
import { InterventionAssignmentComposer } from "@/components/dashboard/InterventionAssignmentComposer";
import { InsightSectionLabel } from "@/components/dashboard/InsightSectionLabel";
import { RecommendationAckComposer } from "@/components/dashboard/RecommendationAckComposer";
import { RecommendationFeedbackComposer } from "@/components/dashboard/RecommendationFeedbackComposer";
import { TeacherActionComposer } from "@/components/dashboard/TeacherActionComposer";
import type {
  DiagnosisFeedbackRecord,
  InterventionAssignmentRecord,
  RecommendationFeedbackRecord,
  RecommendationAckRecord,
  TeacherActionRecord,
  TeacherInsightStudent,
} from "@/lib/dashboard-api";

function formatLatency(seconds: number | undefined): string | null {
  if (seconds == null) return null;
  if (seconds < 1) return `≈${Math.round(seconds * 1000)} ms`;
  return `${Math.round(seconds)} s`;
}

export function StudentInsightCard({
  student,
  t,
}: {
  student: TeacherInsightStudent;
  t: (value: string, options?: Record<string, string | number>) => string;
}) {
  const diagnosis = student.inferred[0];
  const recommendation = student.recommended_actions[0];
  const [diagnosisFeedback, setDiagnosisFeedback] = useState<DiagnosisFeedbackRecord | null>(
    student.diagnosis_feedback ?? null,
  );
  const [recommendationAck, setRecommendationAck] = useState<RecommendationAckRecord | null>(
    student.recommendation_ack ?? null,
  );
  const [recommendationFeedback, setRecommendationFeedback] = useState<RecommendationFeedbackRecord | null>(
    student.recommendation_feedback ?? null,
  );
  const [teacherActions, setTeacherActions] = useState<TeacherActionRecord[]>(student.teacher_actions ?? []);
  const [interventionAssignments, setInterventionAssignments] = useState<InterventionAssignmentRecord[]>(
    student.intervention_assignments ?? [],
  );
  const latestAction = teacherActions[0] ?? null;
  const latestAssignment = interventionAssignments[0] ?? null;

  return (
    <article className="rounded-3xl border border-[var(--border)] bg-[var(--background)] p-4 shadow-sm">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <div className="text-[12px] font-semibold uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
            {student.student_id}
          </div>
          <div className="mt-1 text-[16px] font-semibold text-[var(--foreground)]">
            {student.observed?.topic ?? t("No dominant topic")}
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="rounded-full bg-[var(--muted)] px-2.5 py-1 text-[11px] text-[var(--muted-foreground)]">
            {t("{{confidence}} confidence", { confidence: diagnosis?.confidence_tag ?? "N/A" })}
          </span>
          <Link
            href={`/dashboard/student?student=${encodeURIComponent(student.student_id)}`}
            className="inline-flex items-center gap-1 rounded-full border border-[var(--border)] px-3 py-1 text-[11px] font-medium text-[var(--foreground)] transition hover:border-[var(--foreground)]"
          >
            {t("Open detail")}
            <ArrowRight size={12} />
          </Link>
        </div>
      </div>

      <div className="mt-4 grid gap-3 sm:grid-cols-3">
        <section className="rounded-2xl bg-[var(--muted)]/45 p-3">
          <InsightSectionLabel eyebrow={t("Observed")} title={student.observed?.topic ?? t("No recent evidence")} />
          <div className="mt-3 space-y-2 text-[12px] text-[var(--foreground)]">
            <div>{t("Missed items: {{count}}", { count: student.observed?.miss_count ?? 0 })}</div>
            <div>{t("Response time: {{value}}", { value: formatLatency(student.observed?.avg_latency_seconds) ?? t("Unknown") })}</div>
            {student.student_state?.support_level ? (
              <div>{t("Support: {{value}}", { value: student.student_state.support_level })}</div>
            ) : null}
          </div>
        </section>

        <section className="rounded-2xl bg-amber-50 p-3">
          <InsightSectionLabel
            eyebrow={t("Inferred")}
            title={diagnosis?.diagnosis_type ?? t("No diagnosis")}
            toneClassName="text-amber-700"
          >
            {diagnosis?.topic ? t("Topic: {{topic}}", { topic: diagnosis.topic }) : t("No inferred topic")}
          </InsightSectionLabel>
          {diagnosis?.evidence?.length ? (
            <div className="mt-3 flex flex-wrap gap-2">
              {diagnosis.evidence.slice(0, 3).map((fact) => (
                <span
                  key={`${student.student_id}-${fact}`}
                  className="rounded-full bg-white/70 px-2.5 py-1 text-[11px] text-amber-900/80"
                >
                  {fact}
                </span>
              ))}
            </div>
          ) : null}
          {diagnosis ? (
            <div className="mt-3">
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
            <div className="mt-3 rounded-2xl border border-amber-200 bg-white/80 p-3 text-[12px] text-amber-900/80">
              <div className="font-medium">{t("Diagnosis feedback: {{label}}", { label: diagnosisFeedback.feedback_label })}</div>
              {diagnosisFeedback.teacher_note ? <div className="mt-1">{diagnosisFeedback.teacher_note}</div> : null}
            </div>
          ) : null}
        </section>

        <section className="rounded-2xl bg-emerald-50 p-3">
          <InsightSectionLabel
            eyebrow={t("Teacher move")}
            title={recommendation?.action_type ?? t("No next move yet")}
            toneClassName="text-emerald-700"
          >
            {recommendation?.rationale ?? t("No recommendation available")}
          </InsightSectionLabel>
          <div className="mt-3 text-[12px] text-emerald-900/80">
            {diagnosis?.evidence?.[0]
              ? t("Why this move: {{reason}}", { reason: diagnosis.evidence[0] })
              : t("Why this move: based on the strongest recent learning signal.")}
          </div>
          <div className="mt-3">
            <RecommendationFeedbackComposer
              triggerLabel={
                recommendationFeedback ? t("Update recommendation feedback") : t("Review recommendation quality")
              }
              defaultPayload={{
                target_type: "student",
                target_id: student.student_id,
                source_recommendation_id: recommendation?.action_id ?? `student:${student.student_id}`,
              }}
              existingFeedback={recommendationFeedback}
              onSaved={setRecommendationFeedback}
              t={t}
            />
          </div>
          {recommendationFeedback ? (
            <div className="mt-3 rounded-2xl border border-emerald-200 bg-white/80 p-3 text-[12px] text-emerald-900/80">
              <div className="font-medium">
                {t("Recommendation feedback: {{label}}", { label: recommendationFeedback.feedback_label })}
              </div>
              {recommendationFeedback.teacher_note ? <div className="mt-1">{recommendationFeedback.teacher_note}</div> : null}
            </div>
          ) : null}
          <div className="mt-3">
            <RecommendationAckComposer
              triggerLabel={recommendationAck ? t("Update acknowledgement") : t("Acknowledge recommendation")}
              defaultPayload={{
                target_type: "student",
                target_id: student.student_id,
                source_recommendation_id: recommendation?.action_id ?? `student:${student.student_id}`,
              }}
              existingAck={recommendationAck}
              onSaved={setRecommendationAck}
              t={t}
            />
          </div>
          {recommendationAck ? (
            <div className="mt-3 rounded-2xl border border-emerald-200 bg-white/80 p-3 text-[12px] text-emerald-900/80">
              <div className="font-medium">{t("Recommendation status: {{status}}", { status: recommendationAck.status })}</div>
              {recommendationAck.teacher_note ? <div className="mt-1">{recommendationAck.teacher_note}</div> : null}
            </div>
          ) : null}
          <div className="mt-3">
            <TeacherActionComposer
              triggerLabel={t("Create action")}
              defaultPayload={{
                target_type: "student",
                target_id: student.student_id,
                source_recommendation_id: recommendation?.action_id ?? `student:${student.student_id}`,
                topic: recommendation?.topic ?? diagnosis?.topic ?? student.observed?.topic ?? "general",
                defaultActionType: "reteach_concept",
              }}
              onCreated={(record) => setTeacherActions((current) => [record, ...current])}
              t={t}
            />
          </div>
          {latestAction ? (
            <div className="mt-3">
              <InterventionAssignmentComposer
                triggerLabel={t("Convert to assignment")}
                teacherAction={latestAction}
                onCreated={(record) => setInterventionAssignments((current) => [record, ...current])}
                t={t}
              />
            </div>
          ) : null}
          {latestAction ? (
            <div className="mt-3 rounded-2xl bg-white/70 p-3 text-[12px] text-emerald-900/80">
              <div className="font-medium">{latestAction.action_type}</div>
              <div className="mt-1">{latestAction.teacher_instruction}</div>
              <div className="mt-2 text-[11px] text-emerald-900/70">
                {t("Status: {{status}} • Priority: {{priority}}", {
                  status: latestAction.status,
                  priority: latestAction.priority,
                })}
              </div>
            </div>
          ) : null}
          {latestAssignment ? (
            <div className="mt-3 rounded-2xl border border-emerald-200 bg-white/80 p-3 text-[12px] text-emerald-900/80">
              <div className="font-medium">{latestAssignment.assignment_type}</div>
              <div className="mt-1">{latestAssignment.title}</div>
              <div className="mt-2 text-[11px] text-emerald-900/70">
                {t("Assignment status: {{status}}", { status: latestAssignment.status })}
              </div>
            </div>
          ) : null}
        </section>
      </div>
    </article>
  );
}
