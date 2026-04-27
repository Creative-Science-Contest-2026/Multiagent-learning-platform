"use client";

import { useEffect, useState } from "react";
import {
  createAssessmentRubricReview,
  type AssessmentRubricDecision,
  type AssessmentRubricLevel,
  type TeacherAssessmentReviewRecord,
  updateAssessmentRubricReview,
} from "@/lib/dashboard-api";

const RUBRIC_LEVELS: AssessmentRubricLevel[] = ["strong", "acceptable", "weak"];
const REVIEW_DECISIONS: AssessmentRubricDecision[] = [
  "approved_for_reuse",
  "needs_edit_before_reuse",
  "not_ready",
];

export function AssessmentRubricReviewCard({
  sessionId,
  existingReview,
  t,
}: {
  sessionId: string;
  existingReview?: TeacherAssessmentReviewRecord | null;
  t: (value: string, options?: Record<string, string | number>) => string;
}) {
  const [savedReview, setSavedReview] = useState<TeacherAssessmentReviewRecord | null>(existingReview ?? null);
  const [wordingQuality, setWordingQuality] = useState<AssessmentRubricLevel>(
    existingReview?.wording_quality ?? "acceptable",
  );
  const [distractorQuality, setDistractorQuality] = useState<AssessmentRubricLevel>(
    existingReview?.distractor_quality ?? "acceptable",
  );
  const [explanationClarity, setExplanationClarity] = useState<AssessmentRubricLevel>(
    existingReview?.explanation_clarity ?? "acceptable",
  );
  const [overallDecision, setOverallDecision] = useState<AssessmentRubricDecision>(
    existingReview?.overall_decision ?? "needs_edit_before_reuse",
  );
  const [teacherNote, setTeacherNote] = useState(existingReview?.teacher_note ?? "");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    setSavedReview(existingReview ?? null);
    setWordingQuality(existingReview?.wording_quality ?? "acceptable");
    setDistractorQuality(existingReview?.distractor_quality ?? "acceptable");
    setExplanationClarity(existingReview?.explanation_clarity ?? "acceptable");
    setOverallDecision(existingReview?.overall_decision ?? "needs_edit_before_reuse");
    setTeacherNote(existingReview?.teacher_note ?? "");
  }, [existingReview]);

  async function handleSubmit() {
    setSubmitting(true);
    try {
      const payload = {
        wording_quality: wordingQuality,
        distractor_quality: distractorQuality,
        explanation_clarity: explanationClarity,
        overall_decision: overallDecision,
        teacher_note: teacherNote,
      };
      const record = savedReview
        ? await updateAssessmentRubricReview(sessionId, payload)
        : await createAssessmentRubricReview(sessionId, payload);
      setSavedReview(record);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-4 shadow-sm">
      <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-[var(--muted-foreground)]">
        {t("Teacher Review Rubric")}
      </div>
      <div className="mt-3 grid gap-3 md:grid-cols-2">
        <label className="text-[12px] text-[var(--muted-foreground)]">
          {t("Question wording")}
          <select
            value={wordingQuality}
            onChange={(e) => setWordingQuality(e.target.value as AssessmentRubricLevel)}
            className="mt-1 w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)]"
          >
            {RUBRIC_LEVELS.map((value) => (
              <option key={value} value={value}>
                {value}
              </option>
            ))}
          </select>
        </label>
        <label className="text-[12px] text-[var(--muted-foreground)]">
          {t("Distractor quality")}
          <select
            value={distractorQuality}
            onChange={(e) => setDistractorQuality(e.target.value as AssessmentRubricLevel)}
            className="mt-1 w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)]"
          >
            {RUBRIC_LEVELS.map((value) => (
              <option key={value} value={value}>
                {value}
              </option>
            ))}
          </select>
        </label>
        <label className="text-[12px] text-[var(--muted-foreground)]">
          {t("Explanation clarity")}
          <select
            value={explanationClarity}
            onChange={(e) => setExplanationClarity(e.target.value as AssessmentRubricLevel)}
            className="mt-1 w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)]"
          >
            {RUBRIC_LEVELS.map((value) => (
              <option key={value} value={value}>
                {value}
              </option>
            ))}
          </select>
        </label>
        <label className="text-[12px] text-[var(--muted-foreground)]">
          {t("Overall reuse decision")}
          <select
            value={overallDecision}
            onChange={(e) => setOverallDecision(e.target.value as AssessmentRubricDecision)}
            className="mt-1 w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)]"
          >
            {REVIEW_DECISIONS.map((value) => (
              <option key={value} value={value}>
                {value}
              </option>
            ))}
          </select>
        </label>
      </div>
      <label className="mt-3 block text-[12px] text-[var(--muted-foreground)]">
        {t("Teacher note")}
        <textarea
          value={teacherNote}
          onChange={(e) => setTeacherNote(e.target.value)}
          className="mt-1 min-h-[88px] w-full rounded-xl border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)]"
        />
      </label>
      <button
        type="button"
        disabled={submitting}
        onClick={handleSubmit}
        className="mt-3 rounded-xl bg-[var(--foreground)] px-3 py-2 text-[13px] font-medium text-[var(--background)] disabled:opacity-60"
      >
        {submitting ? t("Saving...") : savedReview ? t("Update rubric review") : t("Save rubric review")}
      </button>
      {savedReview ? (
        <div className="mt-3 rounded-2xl border border-[var(--border)] bg-[var(--muted)]/50 p-3 text-[12px] text-[var(--foreground)]">
          <div className="font-medium">
            {t("Overall decision: {{value}}", { value: savedReview.overall_decision })}
          </div>
          <div className="mt-1 text-[var(--muted-foreground)]">
            {t("Wording: {{wording}} • Distractors: {{distractors}} • Explanation: {{explanation}}", {
              wording: savedReview.wording_quality,
              distractors: savedReview.distractor_quality,
              explanation: savedReview.explanation_clarity,
            })}
          </div>
          {savedReview.teacher_note ? <div className="mt-2">{savedReview.teacher_note}</div> : null}
        </div>
      ) : null}
    </section>
  );
}
