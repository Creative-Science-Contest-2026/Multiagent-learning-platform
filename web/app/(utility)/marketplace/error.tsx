"use client";

import { useEffect } from "react";
import { useTranslation } from "react-i18next";

export default function MarketplaceError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  const { t } = useTranslation();

  useEffect(() => {
    // Keep route-level exceptions visible in browser console for quick triage.
    console.error("Marketplace route error:", error);
  }, [error]);

  return (
    <main className="mx-auto flex min-h-[60vh] w-full max-w-[920px] items-center justify-center px-6 py-12">
      <div className="w-full rounded-3xl border border-[var(--border)] bg-[var(--card)] px-6 py-8 text-center shadow-sm">
        <p className="text-[12px] font-semibold uppercase tracking-[0.12em] text-[var(--muted-foreground)]">
          {t("Knowledge Marketplace")}
        </p>
        <h1 className="mt-3 text-[24px] font-semibold text-[var(--foreground)]">
          {t("Something went wrong")}
        </h1>
        <p className="mx-auto mt-3 max-w-[560px] text-[14px] leading-6 text-[var(--muted-foreground)]">
          {t("We could not load the marketplace right now. Please try again.")}
        </p>
        <button
          type="button"
          onClick={reset}
          className="mt-6 rounded-full bg-[var(--primary)] px-5 py-2.5 text-[13px] font-medium text-[var(--primary-foreground)]"
        >
          {t("Try again")}
        </button>
      </div>
    </main>
  );
}
