"use client";

import { useEffect } from "react";
import { useTranslation } from "react-i18next";

export default function AssessmentError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  const { t } = useTranslation();

  useEffect(() => {
    console.error("Assessment route error:", error);
  }, [error]);

  return (
    <main className="mx-auto flex min-h-[50vh] w-full max-w-[860px] flex-col items-center justify-center gap-4 px-6 py-10 text-center">
      <p className="text-[12px] font-semibold uppercase tracking-[0.12em] text-[var(--muted-foreground)]">
        {t("Assessment")}
      </p>
      <h1 className="text-[24px] font-semibold text-[var(--foreground)]">{t("Something went wrong")}</h1>
      <p className="max-w-[560px] text-[14px] text-[var(--muted-foreground)]">
        {t("We could not load this assessment session. Please retry.")}
      </p>
      <button
        type="button"
        onClick={reset}
        className="rounded-md bg-[var(--primary)] px-4 py-2 text-[13px] font-medium text-[var(--primary-foreground)]"
      >
        {t("Try again")}
      </button>
    </main>
  );
}
