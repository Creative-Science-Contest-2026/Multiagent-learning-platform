"use client";

import Link from "next/link";
import { useState } from "react";
import { ArrowRight } from "lucide-react";
import { DiagnosisFeedbackComposer } from "@/components/dashboard/DiagnosisFeedbackComposer";
import {
  formatConfidenceLabel,
  formatDiagnosisLabel,
  formatStudentDisplayName,
  formatSupportLevelLabel,
  formatTeacherFacingLabel,
  formatTeacherMoveLabel,
} from "@/components/dashboard/dashboard-presenters";
import { InterventionAssignmentComposer } from "@/components/dashboard/InterventionAssignmentComposer";
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

function formatLatency(seconds: number | undefined, fallback: string): string {
  if (seconds == null) return fallback;
  if (seconds < 1) return `≈${Math.round(seconds * 1000)} ms`;
  return `${Math.round(seconds)} s`;
}

function getPriorityLabel(student: TeacherInsightStudent, t: (value: string, options?: Record<string, string | number>) => string): string {
  const missCount = student.observed?.miss_count ?? 0;
  const confidenceTag = student.inferred[0]?.confidence_tag?.toLowerCase();
  if (missCount >= 3 || confidenceTag === "high") return t("Ưu tiên cao");
  if (missCount >= 1 || confidenceTag === "medium") return t("Nên xem sớm");
  return t("Cần theo dõi");
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
  const studentDisplayName = formatStudentDisplayName(student.student_id);
  const studentHref = `/dashboard/student?student=${encodeURIComponent(student.student_id)}`;
  const priorityLabel = getPriorityLabel(student, t);
  const ackPayload = {
    target_type: "student" as const,
    target_id: student.student_id,
    source_recommendation_id: recommendation?.action_id ?? `student:${student.student_id}`,
  };

  return (
    <article className="rounded-3xl border border-[var(--border)] bg-[var(--background)] p-4 shadow-sm">
      <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
        <div>
          <div className="text-[16px] font-semibold text-[var(--foreground)]">{studentDisplayName}</div>
          <div className="mt-2 flex flex-wrap gap-2">
            <span className="rounded-full bg-amber-50 px-2.5 py-1 text-[11px] font-medium text-amber-700">
              {priorityLabel}
            </span>
            <span className="rounded-full bg-[var(--muted)] px-2.5 py-1 text-[11px] text-[var(--muted-foreground)]">
              {confidenceLabel}
            </span>
          </div>
        </div>
        <Link
          href={studentHref}
          className="inline-flex items-center gap-1 rounded-full border border-[var(--border)] px-3 py-1.5 text-[11px] font-medium text-[var(--foreground)] transition hover:border-[var(--foreground)]"
        >
          {t("Xem hồ sơ học sinh")}
          <ArrowRight size={12} />
        </Link>
      </div>

      <div className="mt-4 grid gap-3 xl:grid-cols-3">
        <section className="rounded-2xl bg-[var(--muted)]/35 px-4 py-3">
          <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
            {t("1. Dấu hiệu hệ thống vừa thấy")}
          </div>
          <div className="mt-1 text-[15px] font-semibold text-[var(--foreground)]">
            {student.observed?.topic ?? diagnosis?.topic ?? t("Chưa có chủ đề nổi bật")}
          </div>
          <div className="mt-2 text-[12px] text-[var(--muted-foreground)]">
            {t("Đây là phần giáo viên nên xem đầu tiên để biết học sinh đang vướng ở tín hiệu nào rõ nhất.")}
          </div>
          <div className="mt-3 flex flex-wrap gap-2">
            <span className="rounded-full bg-[var(--background)] px-2.5 py-1 text-[11px] text-[var(--muted-foreground)]">
              {t("{{count}} câu cần xem lại", { count: student.observed?.miss_count ?? 0 })}
            </span>
            <span className="rounded-full bg-[var(--background)] px-2.5 py-1 text-[11px] text-[var(--muted-foreground)]">
              {t("Hỗ trợ hiện tại: {{value}}", { value: supportLevelLabel })}
            </span>
            <span className="rounded-full bg-[var(--background)] px-2.5 py-1 text-[11px] text-[var(--muted-foreground)]">
              {t("Phản hồi gần đây: {{value}}", {
                value: formatLatency(student.observed?.avg_latency_seconds, t("Chưa rõ")),
              })}
            </span>
          </div>
        </section>

        <section className="rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3">
          <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-amber-700">
            {t("2. Cách hệ thống đang hiểu")}
          </div>
          <div className="mt-1 text-[15px] font-semibold text-amber-950">{diagnosisLabel}</div>
          <div className="mt-1 text-[12px] leading-6 text-amber-950/80">
            {t("Phần này tóm tắt cách hệ thống đang đọc các dấu hiệu, để giáo viên quyết định có đồng ý hay cần sửa lại nhận định.")}
          </div>
          {diagnosis?.topic ? (
            <div className="mt-2 text-[12px] text-amber-950/85">{t("Trọng tâm hiện tại: {{topic}}", { topic: diagnosis.topic })}</div>
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
        </section>

        <section className="rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3">
          <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-emerald-700">
            {t("3. Việc giáo viên có thể làm tiếp")}
          </div>
          <div className="mt-1 text-[15px] font-semibold text-emerald-950">{nextMoveLabel}</div>
          <div className="mt-1 text-[12px] leading-6 text-emerald-950/80">
            {recommendation?.rationale ?? t("Chưa có gợi ý cụ thể")}
          </div>
          <div className="mt-2 text-[12px] text-emerald-950/80">
            {t("Chỉ sau khi xem dấu hiệu và nhận định ở hai ô trước, giáo viên mới cần chốt bước can thiệp hoặc điều chỉnh hướng riêng của mình.")}
          </div>
        </section>
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        <Link
          href={studentHref}
          className="inline-flex items-center justify-center rounded-full bg-[var(--foreground)] px-4 py-2 text-[12px] font-medium text-[var(--background)]"
        >
          {t("Xem hồ sơ học sinh")}
        </Link>
        <RecommendationAckComposer
          triggerLabel={recommendationAck ? t("Cập nhật trạng thái đã xem") : t("Đánh dấu đã xem")}
          defaultPayload={ackPayload}
          existingAck={recommendationAck}
          onSaved={setRecommendationAck}
          t={t}
        />
      </div>

      {(recommendationAck || teacherOverride || diagnosisFeedback || latestAction || latestAssignment) && (
        <div className="mt-4 grid gap-3 md:grid-cols-2">
          {recommendationAck ? (
            <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)]/70 p-3 text-[12px] text-[var(--foreground)]/85">
              <div className="font-medium">{t("Trạng thái đã xem")}</div>
              <div className="mt-1">{formatTeacherFacingLabel(recommendationAck.status)}</div>
            </div>
          ) : null}
          {teacherOverride ? (
            <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)]/70 p-3 text-[12px] text-[var(--foreground)]/85">
              <div className="font-medium">{t("Giáo viên chọn hướng khác")}</div>
              <div className="mt-1">{formatTeacherMoveLabel(teacherOverride.teacher_selected_move)}</div>
            </div>
          ) : null}
          {diagnosisFeedback ? (
            <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)]/70 p-3 text-[12px] text-[var(--foreground)]/85">
              <div className="font-medium">{t("Phản hồi nhận định")}</div>
              <div className="mt-1">{formatTeacherFacingLabel(diagnosisFeedback.feedback_label)}</div>
            </div>
          ) : null}
          {latestAction ? (
            <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)]/70 p-3 text-[12px] text-[var(--foreground)]/85">
              <div className="font-medium">{t("Việc giáo viên đang theo dõi")}</div>
              <div className="mt-1">{formatTeacherMoveLabel(latestAction.action_type)}</div>
            </div>
          ) : null}
          {latestAssignment ? (
            <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)]/70 p-3 text-[12px] text-[var(--foreground)]/85">
              <div className="font-medium">{t("Đầu việc đã giao")}</div>
              <div className="mt-1">{latestAssignment.title}</div>
            </div>
          ) : null}
        </div>
      )}

      <details className="mt-4 rounded-2xl border border-[var(--border)] bg-[var(--card)]/60 p-3">
        <summary className="cursor-pointer text-[12px] font-medium text-[var(--muted-foreground)]">
          {t("Chi tiết hệ thống")}
        </summary>
        <div className="mt-3 space-y-3">
          <div className="rounded-2xl border border-[var(--border)] bg-[var(--background)]/70 p-3 text-[12px] text-[var(--foreground)]/85">
            <div className="font-medium">{t("Vì sao hệ thống gợi ý như vậy")}</div>
            <div className="mt-1">
              {trustTrace?.recommendation_rationale ||
                (diagnosis?.evidence?.[0]
                  ? t("Dấu hiệu rõ nhất hiện tại là: {{reason}}", { reason: diagnosis.evidence[0] })
                  : t("Gợi ý này dựa trên tín hiệu học tập nổi bật gần nhất của học sinh."))}
            </div>
            <div className="mt-2 text-[11px] text-[var(--muted-foreground)]">
              {trustTrace?.teacher_review_required
                ? t("Cần giáo viên xác nhận trước khi xem đây là kết luận cuối cùng.")
                : t("Đây là gợi ý để giáo viên tham khảo khi quyết định bước tiếp theo.")}
            </div>
          </div>

          {diagnosis ? (
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
          ) : null}

          <div className="grid gap-3 lg:grid-cols-2">
            <RecommendationFeedbackComposer
              triggerLabel={
                recommendationFeedback ? t("Cập nhật đánh giá về gợi ý") : t("Đánh giá chất lượng gợi ý")
              }
              defaultPayload={ackPayload}
              existingFeedback={recommendationFeedback}
              onSaved={setRecommendationFeedback}
              t={t}
            />
            <TeacherOverrideComposer
              triggerLabel={teacherOverride ? t("Cập nhật quyết định của giáo viên") : t("Ghi lại quyết định riêng của giáo viên")}
              defaultPayload={ackPayload}
              existingOverride={teacherOverride}
              onSaved={setTeacherOverride}
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
            {latestAction ? (
              <InterventionAssignmentComposer
                triggerLabel={t("Chuyển thành đầu việc giao thực hiện")}
                teacherAction={latestAction}
                onCreated={(record) => setInterventionAssignments((current) => [record, ...current])}
                t={t}
              />
            ) : null}
          </div>
        </div>
      </details>
    </article>
  );
}
