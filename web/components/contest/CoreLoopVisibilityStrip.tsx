"use client";

import { useTranslation } from "react-i18next";

export type CoreLoopStep =
  | "Knowledge Pack"
  | "Assessment"
  | "Tutor"
  | "Diagnosis"
  | "Intervention";

const CORE_LOOP_STEPS: CoreLoopStep[] = [
  "Knowledge Pack",
  "Assessment",
  "Tutor",
  "Diagnosis",
  "Intervention",
];

interface CoreLoopVisibilityStripProps {
  currentStep: CoreLoopStep;
  nextStep?: CoreLoopStep;
  helperText?: string;
  compact?: boolean;
}

export function CoreLoopVisibilityStrip({
  currentStep,
  nextStep,
  helperText,
  compact = false,
}: CoreLoopVisibilityStripProps) {
  const { t } = useTranslation();

  return (
    <section
      className={`rounded-2xl border border-[var(--border)] bg-[var(--background)]/70 ${
        compact ? "px-3 py-3" : "px-4 py-4"
      }`}
    >
      <div className="flex flex-col gap-2">
        <div className="text-[11px] font-semibold uppercase tracking-[0.12em] text-[var(--muted-foreground)]">
          {t("Contest loop")}
        </div>
        <p className={`${compact ? "text-[12px]" : "text-[13px]"} text-[var(--muted-foreground)]`}>
          {helperText || t("Track the same teacher-guided adaptive loop across the product.")}
        </p>
      </div>

      <div className={`mt-3 flex flex-wrap gap-2 ${compact ? "text-[11px]" : "text-[12px]"}`}>
        {CORE_LOOP_STEPS.map((step) => {
          const isCurrent = step === currentStep;
          const isNext = step === nextStep;

          return (
            <span
              key={step}
              className={`inline-flex items-center rounded-full border px-3 py-1.5 font-medium transition-colors ${
                isCurrent
                  ? "border-[var(--foreground)] bg-[var(--foreground)] text-[var(--background)]"
                  : isNext
                    ? "border-amber-300 bg-amber-50 text-amber-900 dark:border-amber-900/40 dark:bg-amber-950/20 dark:text-amber-200"
                    : "border-[var(--border)] bg-[var(--card)] text-[var(--muted-foreground)]"
              }`}
            >
              {step}
            </span>
          );
        })}
      </div>
    </section>
  );
}
