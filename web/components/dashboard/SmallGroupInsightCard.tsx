"use client";

import { useState } from "react";
import { InterventionAssignmentComposer } from "@/components/dashboard/InterventionAssignmentComposer";
import { InsightSectionLabel } from "@/components/dashboard/InsightSectionLabel";
import { RecommendationAckComposer } from "@/components/dashboard/RecommendationAckComposer";
import { RecommendationFeedbackComposer } from "@/components/dashboard/RecommendationFeedbackComposer";
import { TeacherActionComposer } from "@/components/dashboard/TeacherActionComposer";
import { TeacherOverrideComposer } from "@/components/dashboard/TeacherOverrideComposer";
import type {
  DashboardInsights,
  InterventionAssignmentRecord,
  RecommendationFeedbackRecord,
  RecommendationAckRecord,
  TeacherActionRecord,
  TeacherOverrideRecord,
} from "@/lib/dashboard-api";

type SmallGroupInsight = DashboardInsights["small_groups"][number];

export function SmallGroupInsightCard({
  group,
  t,
}: {
  group: SmallGroupInsight;
  t: (value: string, options?: Record<string, string | number>) => string;
}) {
  const [teacherAction, setTeacherAction] = useState<TeacherActionRecord | null>(group.teacher_action ?? null);
  const [recommendationAck, setRecommendationAck] = useState<RecommendationAckRecord | null>(
    group.recommendation_ack ?? null,
  );
  const [recommendationFeedback, setRecommendationFeedback] = useState<RecommendationFeedbackRecord | null>(
    group.recommendation_feedback ?? null,
  );
  const [teacherOverride, setTeacherOverride] = useState<TeacherOverrideRecord | null>(
    group.teacher_override ?? null,
  );
  const [interventionAssignment, setInterventionAssignment] = useState<InterventionAssignmentRecord | null>(
    group.intervention_assignment ?? null,
  );
  const reasonTrace = group.reason_trace;

  return (
    <article className="rounded-3xl border border-[var(--border)] bg-[var(--background)] p-4 shadow-sm">
      <div className="flex items-start justify-between gap-3">
        <InsightSectionLabel eyebrow={t("Shared signal")} title={group.topic}>
          {group.diagnosis_type}
        </InsightSectionLabel>
        <span className="rounded-full bg-[var(--muted)] px-2.5 py-1 text-[11px] text-[var(--muted-foreground)]">
          {t("{{count}} students", { count: group.student_ids.length })}
        </span>
      </div>

      <div className="mt-4 rounded-2xl bg-emerald-50 p-3">
        <InsightSectionLabel
          eyebrow={t("Teacher move")}
          title={group.recommended_action}
          toneClassName="text-emerald-700"
        />
        <div className="mt-3 text-[12px] text-emerald-900/80">
          {reasonTrace
            ? t("Why these students are grouped: same topic, diagnosis, and suggested move.")
            : t("Why these students are grouped: they show the same dominant learning signal.")}
        </div>
        <div className="mt-3 text-[12px] text-[var(--muted-foreground)]">
          {t("Students: {{students}}", { students: group.student_ids.join(", ") })}
        </div>
        {reasonTrace ? (
          <div className="mt-3 rounded-2xl border border-emerald-200 bg-white/80 p-3 text-[12px] text-emerald-900/80">
            <div className="font-medium">
              {t("Trust trace: {{confidence}} confidence", { confidence: reasonTrace.confidence_tag })}
            </div>
            <div className="mt-1">
              {t("Rule: {{rule}}", { rule: reasonTrace.grouping_rule })}
            </div>
            {reasonTrace.shared_evidence?.length ? (
              <ul className="mt-2 space-y-1">
                {reasonTrace.shared_evidence.map((fact) => (
                  <li key={`${group.target_id ?? group.topic}-${fact}`}>• {fact}</li>
                ))}
              </ul>
            ) : null}
            <div className="mt-2 text-emerald-900/70">{reasonTrace.teacher_review_note}</div>
          </div>
        ) : null}
        <div className="mt-3">
          <RecommendationFeedbackComposer
            triggerLabel={
              recommendationFeedback ? t("Update recommendation feedback") : t("Review recommendation quality")
            }
            defaultPayload={{
              target_type: "small_group",
              target_id: group.target_id ?? `${group.topic}:${group.diagnosis_type}`,
              source_recommendation_id: `group:${group.topic}:${group.diagnosis_type}`,
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
          <TeacherOverrideComposer
            triggerLabel={teacherOverride ? t("Update teacher override") : t("Log teacher override")}
            defaultPayload={{
              target_type: "small_group",
              target_id: group.target_id ?? `${group.topic}:${group.diagnosis_type}`,
              source_recommendation_id: `group:${group.topic}:${group.diagnosis_type}`,
            }}
            existingOverride={teacherOverride}
            onSaved={setTeacherOverride}
            t={t}
          />
        </div>
        {teacherOverride ? (
          <div className="mt-3 rounded-2xl border border-emerald-200 bg-white/80 p-3 text-[12px] text-emerald-900/80">
            <div className="font-medium">
              {t("Teacher override: {{move}}", { move: teacherOverride.teacher_selected_move })}
            </div>
            <div className="mt-1">
              {t("Reason: {{reason}}", { reason: teacherOverride.override_reason })}
            </div>
            {teacherOverride.teacher_note ? <div className="mt-1">{teacherOverride.teacher_note}</div> : null}
          </div>
        ) : null}
        <div className="mt-3">
          <RecommendationAckComposer
            triggerLabel={recommendationAck ? t("Update acknowledgement") : t("Acknowledge recommendation")}
            defaultPayload={{
              target_type: "small_group",
              target_id: group.target_id ?? `${group.topic}:${group.diagnosis_type}`,
              source_recommendation_id: `group:${group.topic}:${group.diagnosis_type}`,
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
            triggerLabel={t("Create group action")}
            defaultPayload={{
              target_type: "small_group",
              target_id: group.target_id ?? `${group.topic}:${group.diagnosis_type}`,
              source_recommendation_id: `group:${group.topic}:${group.diagnosis_type}`,
              topic: group.topic,
              defaultActionType: "small_group_remediation",
            }}
            onCreated={(record) => setTeacherAction(record)}
            t={t}
          />
        </div>
        {teacherAction ? (
          <div className="mt-3">
            <InterventionAssignmentComposer
              triggerLabel={t("Convert to assignment")}
              teacherAction={teacherAction}
              onCreated={(record) => setInterventionAssignment(record)}
              t={t}
            />
          </div>
        ) : null}
        {teacherAction ? (
          <div className="mt-3 rounded-2xl bg-white/70 p-3 text-[12px] text-emerald-900/80">
            <div className="font-medium">{teacherAction.action_type}</div>
            <div className="mt-1">{teacherAction.teacher_instruction}</div>
            <div className="mt-2 text-[11px] text-emerald-900/70">
              {t("Status: {{status}} • Priority: {{priority}}", {
                status: teacherAction.status,
                priority: teacherAction.priority,
              })}
            </div>
          </div>
        ) : null}
        {interventionAssignment ? (
          <div className="mt-3 rounded-2xl border border-emerald-200 bg-white/80 p-3 text-[12px] text-emerald-900/80">
            <div className="font-medium">{interventionAssignment.assignment_type}</div>
            <div className="mt-1">{interventionAssignment.title}</div>
            <div className="mt-2 text-[11px] text-emerald-900/70">
              {t("Assignment status: {{status}}", { status: interventionAssignment.status })}
            </div>
          </div>
        ) : null}
      </div>
    </article>
  );
}
