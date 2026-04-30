"use client";

import Link from "next/link";
import { useState } from "react";
import { ArrowRight } from "lucide-react";
import { DiagnosisFeedbackComposer } from "@/components/dashboard/DiagnosisFeedbackComposer";
import {
  formatConfidenceLabel,
  formatDiagnosisLabel,
  formatSupportLevelLabel,
  formatTeacherFacingLabel,
  formatTeacherMoveLabel,
} from "@/components/dashboard/dashboard-presenters";
import { InterventionAssignmentComposer } from "@/components/dashboard/InterventionAssignmentComposer";
import { InsightSectionLabel } from "@/components/dashboard/InsightSectionLabel";
import { RecommendationAckComposer } from "@/components/dashboard/RecommendationAckComposer";
import { RecommendationFeedbackComposer } from "@/components/dashboard/RecommendationFeedbackComposer";
import { TeacherActionComposer } from "@/components/dashboard/TeacherActionComposer";
import { TeacherOverrideComposer } from "@/components/dashboard/TeacherOverrideComposer";
import type {
  DiagnosisFeedbackRecord,
  InterventionAssignmentRecord,
  RecommendationFeedbackRecord,
  RecommendationAckRecord,
  TeacherActionRecord,
  TeacherOverrideRecord,
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
  const [teacherOverride, setTeacherOverride] = useState<TeacherOverrideRecord | null>(
    student.teacher_override ?? null,
  );
  const [teacherActions, setTeacherActions] = useState<TeacherActionRecord[]>(student.teacher_actions ?? []);
  const [interventionAssignments, setInterventionAssignments] = useState<InterventionAssignmentRecord[]>(
    student.intervention_assignments ?? [],
  );
  const latestAction = teacherActions[0] ?? null;
  const latestAssignment = interventionAssignments[0] ?? null;
  const trustTrace = student.reason_trace;
  const confidenceLabel = formatConfidenceLabel(diagnosis?.confidence_tag);
  const diagnosisLabel = formatDiagnosisLabel(diagnosis?.diagnosis_type);
  const nextMoveLabel = formatTeacherMoveLabel(recommendation?.action_type);
  const supportLevelLabel = formatSupportLevelLabel(student.student_state?.support_level);

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
            {confidenceLabel}
          </span>
          <Link
            href={`/dashboard/student?student=${encodeURIComponent(student.student_id)}`}
            className="inline-flex items-center gap-1 rounded-full border border-[var(--border)] px-3 py-1 text-[11px] font-medium text-[var(--foreground)] transition hover:border-[var(--foreground)]"
          >
            {t("Xem chi tiết")}
            <ArrowRight size={12} />
          </Link>
        </div>
      </div>

      <div className="mt-4 grid gap-4 xl:grid-cols-[0.95fr_1.25fr]">
        <div className="space-y-3">
          <section className="rounded-2xl border border-[var(--border)] bg-[var(--muted)]/30 p-3">
            <InsightSectionLabel eyebrow={t("Điều hệ thống vừa ghi nhận")} title={student.observed?.topic ?? t("Chưa có dữ liệu mới")} />
            <div className="mt-3 grid gap-2 text-[12px] text-[var(--foreground)] sm:grid-cols-2">
              <div>{t("Số câu cần xem lại: {{count}}", { count: student.observed?.miss_count ?? 0 })}</div>
              <div>{t("Thời gian phản hồi: {{value}}", { value: formatLatency(student.observed?.avg_latency_seconds) ?? t("Chưa rõ") })}</div>
              <div className="sm:col-span-2">{t("Mức hỗ trợ hiện tại: {{value}}", { value: supportLevelLabel })}</div>
            </div>
          </section>

          <section className="rounded-2xl border border-amber-200 bg-amber-50 p-3">
            <InsightSectionLabel
              eyebrow={t("Nhận định tạm thời")}
              title={diagnosisLabel}
              toneClassName="text-amber-700"
            >
              {diagnosis?.topic ? t("Trọng tâm hiện tại: {{topic}}", { topic: diagnosis.topic }) : t("Chưa có chủ đề nổi bật")}
            </InsightSectionLabel>
            {diagnosis?.evidence?.length ? (
              <div className="mt-3 flex flex-wrap gap-2">
                {diagnosis.evidence.slice(0, 3).map((fact) => (
                  <span
                    key={`${student.student_id}-${fact}`}
                    className="rounded-full bg-white/80 px-2.5 py-1 text-[11px] text-amber-900/80"
                  >
                    {fact}
                  </span>
                ))}
              </div>
            ) : null}
            {diagnosis ? (
              <div className="mt-3">
                <DiagnosisFeedbackComposer
                  triggerLabel={diagnosisFeedback ? t("Cập nhật nhận xét của giáo viên") : t("Giáo viên rà soát nhận định")}
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
              <div className="mt-3 rounded-2xl border border-amber-200 bg-white/90 p-3 text-[12px] text-amber-900/80">
                <div className="font-medium">{t("Giáo viên đã phản hồi: {{label}}", { label: formatTeacherFacingLabel(diagnosisFeedback.feedback_label) })}</div>
                {diagnosisFeedback.teacher_note ? <div className="mt-1">{diagnosisFeedback.teacher_note}</div> : null}
              </div>
            ) : null}
          </section>
        </div>

        <section className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4">
          <InsightSectionLabel
            eyebrow={t("Hướng can thiệp nên làm tiếp")}
            title={nextMoveLabel}
            toneClassName="text-emerald-700"
          >
            {recommendation?.rationale ?? t("Chưa có gợi ý cụ thể")}
          </InsightSectionLabel>
          <div className="mt-3 rounded-2xl border border-emerald-200/80 bg-white/80 p-3 text-[12px] text-emerald-950/85">
            <div className="font-medium">{t("Vì sao hệ thống gợi ý như vậy")}</div>
            <div className="mt-1">
              {trustTrace?.recommendation_rationale ||
                (diagnosis?.evidence?.[0]
                  ? t("Dấu hiệu rõ nhất hiện tại là: {{reason}}", { reason: diagnosis.evidence[0] })
                  : t("Gợi ý này dựa trên tín hiệu học tập nổi bật gần nhất của học sinh."))}
            </div>
            <div className="mt-2 text-[11px] text-emerald-900/75">
              {trustTrace?.teacher_review_required
                ? t("Giáo viên nên xác nhận lại trước khi xem đây là kết luận cuối cùng.")
                : t("Đây là gợi ý để giáo viên tham khảo khi quyết định bước tiếp theo.")}
            </div>
          </div>

          <div className="mt-4 grid gap-3 lg:grid-cols-2">
            <RecommendationFeedbackComposer
              triggerLabel={
                recommendationFeedback ? t("Cập nhật đánh giá về gợi ý") : t("Đánh giá chất lượng gợi ý")
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
            <TeacherOverrideComposer
              triggerLabel={teacherOverride ? t("Cập nhật quyết định của giáo viên") : t("Ghi lại quyết định riêng của giáo viên")}
              defaultPayload={{
                target_type: "student",
                target_id: student.student_id,
                source_recommendation_id: recommendation?.action_id ?? `student:${student.student_id}`,
              }}
              existingOverride={teacherOverride}
              onSaved={setTeacherOverride}
              t={t}
            />
            <RecommendationAckComposer
              triggerLabel={recommendationAck ? t("Cập nhật trạng thái tiếp nhận") : t("Đánh dấu đã xem gợi ý")}
              defaultPayload={{
                target_type: "student",
                target_id: student.student_id,
                source_recommendation_id: recommendation?.action_id ?? `student:${student.student_id}`,
              }}
              existingAck={recommendationAck}
              onSaved={setRecommendationAck}
              t={t}
            />
            <TeacherActionComposer
              triggerLabel={t("Tạo việc cần làm cho giáo viên")}
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
                triggerLabel={t("Chuyển thành đầu việc giao thực hiện")}
                teacherAction={latestAction}
                onCreated={(record) => setInterventionAssignments((current) => [record, ...current])}
                t={t}
              />
            </div>
          ) : null}

          <div className="mt-4 grid gap-3 md:grid-cols-3">
            {recommendationFeedback ? (
              <div className="rounded-2xl border border-emerald-200 bg-white/85 p-3 text-[12px] text-emerald-900/85">
                <div className="font-medium">{t("Giáo viên đánh giá gợi ý")}</div>
                <div className="mt-1">{formatTeacherFacingLabel(recommendationFeedback.feedback_label)}</div>
                {recommendationFeedback.teacher_note ? <div className="mt-1">{recommendationFeedback.teacher_note}</div> : null}
              </div>
            ) : null}
            {teacherOverride ? (
              <div className="rounded-2xl border border-emerald-200 bg-white/85 p-3 text-[12px] text-emerald-900/85">
                <div className="font-medium">{t("Giáo viên chọn hướng khác")}</div>
                <div className="mt-1">{formatTeacherMoveLabel(teacherOverride.teacher_selected_move)}</div>
                <div className="mt-1">{t("Lý do: {{reason}}", { reason: formatTeacherFacingLabel(teacherOverride.override_reason) })}</div>
                {teacherOverride.teacher_note ? <div className="mt-1">{teacherOverride.teacher_note}</div> : null}
              </div>
            ) : null}
            {recommendationAck ? (
              <div className="rounded-2xl border border-emerald-200 bg-white/85 p-3 text-[12px] text-emerald-900/85">
                <div className="font-medium">{t("Trạng thái tiếp nhận")}</div>
                <div className="mt-1">{formatTeacherFacingLabel(recommendationAck.status)}</div>
                {recommendationAck.teacher_note ? <div className="mt-1">{recommendationAck.teacher_note}</div> : null}
              </div>
            ) : null}
          </div>

          {latestAction ? (
            <div className="mt-3 rounded-2xl bg-white/80 p-3 text-[12px] text-emerald-900/85">
              <div className="font-medium">{formatTeacherMoveLabel(latestAction.action_type)}</div>
              <div className="mt-1">{latestAction.teacher_instruction}</div>
              <div className="mt-2 text-[11px] text-emerald-900/70">
                {t("Trạng thái: {{status}} • Mức ưu tiên: {{priority}}", {
                  status: formatTeacherFacingLabel(latestAction.status),
                  priority: latestAction.priority,
                })}
              </div>
            </div>
          ) : null}
          {latestAssignment ? (
            <div className="mt-3 rounded-2xl border border-emerald-200 bg-white/85 p-3 text-[12px] text-emerald-900/85">
              <div className="font-medium">{formatTeacherFacingLabel(latestAssignment.assignment_type)}</div>
              <div className="mt-1">{latestAssignment.title}</div>
              <div className="mt-2 text-[11px] text-emerald-900/70">
                {t("Tiến độ giao việc: {{status}}", { status: formatTeacherFacingLabel(latestAssignment.status) })}
              </div>
            </div>
          ) : null}
        </section>
      </div>
    </article>
  );
}
