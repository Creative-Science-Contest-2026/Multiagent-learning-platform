"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { ArrowLeft, Bot, Loader2, UserRound } from "lucide-react";
import { useTranslation } from "react-i18next";
import {
  getDashboardActivityDetail,
  type DashboardActivityDetail,
} from "@/lib/dashboard-api";

function formatTime(value: number): string {
  if (!value) return "";
  const timestamp = value < 10_000_000_000 ? value * 1000 : value;
  return new Intl.DateTimeFormat(undefined, {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(timestamp));
}

export default function SessionReplayPage() {
  const { t } = useTranslation();
  const { sessionId } = useParams<{ sessionId: string }>();
  const [detail, setDetail] = useState<DashboardActivityDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    getDashboardActivityDetail(sessionId)
      .then((data) => {
        if (!cancelled) {
          setDetail(data);
          setError(null);
        }
      })
      .catch((err) => {
        if (!cancelled) setError(err instanceof Error ? err.message : String(err));
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [sessionId]);

  const replayMessages = useMemo(
    () =>
      (detail?.content.messages ?? []).filter((message) =>
        ["user", "assistant", "system"].includes(message.role),
      ),
    [detail],
  );

  if (loading) {
    return (
      <main className="flex h-full items-center justify-center bg-[var(--background)] text-[var(--muted-foreground)]">
        <Loader2 size={18} className="mr-2 animate-spin" />
        {t("Loading session replay...")}
      </main>
    );
  }

  if (error) {
    return (
      <main className="h-full overflow-y-auto bg-[var(--background)] px-6 py-8">
        <div className="mx-auto max-w-[900px] rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
          {t("Failed to load tutoring session replay")}: {error}
        </div>
      </main>
    );
  }

  if (!detail) {
    return (
      <main className="h-full overflow-y-auto bg-[var(--background)] px-6 py-8">
        <div className="mx-auto max-w-[900px] text-sm text-[var(--muted-foreground)]">
          {t("Session replay not found.")}
        </div>
      </main>
    );
  }

  return (
    <main className="h-full overflow-y-auto bg-[var(--background)]">
      <div className="mx-auto flex w-full max-w-[960px] flex-col gap-6 px-6 py-8">
        <Link
          href="/dashboard"
          className="inline-flex w-fit items-center gap-2 text-[13px] text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
        >
          <ArrowLeft size={15} />
          {t("Back to Dashboard")}
        </Link>

        <header>
          <p className="text-[12px] font-semibold uppercase tracking-[0.12em] text-[var(--muted-foreground)]">
            {t("Tutoring Session Replay")}
          </p>
          <h1 className="mt-2 text-[28px] font-semibold tracking-tight text-[var(--foreground)]">
            {detail.title || t("Untitled session")}
          </h1>
          <p className="mt-2 text-[14px] text-[var(--muted-foreground)]">
            {formatTime(detail.timestamp)} - {detail.content.status}
          </p>
          {detail.knowledge_bases.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-2">
              {detail.knowledge_bases.map((kb) => (
                <span
                  key={kb}
                  className="rounded-md bg-[var(--muted)] px-2 py-1 text-[12px] text-[var(--muted-foreground)]"
                >
                  {kb}
                </span>
              ))}
            </div>
          )}
        </header>

        <section className="space-y-4">
          {replayMessages.length > 0 ? (
            replayMessages.map((message) => {
              const isUser = message.role === "user";
              return (
                <article
                  key={message.id}
                  className="rounded-lg border border-[var(--border)] bg-[var(--card)] p-4"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex items-center gap-2 text-[13px] font-medium text-[var(--foreground)]">
                      {isUser ? <UserRound size={16} /> : <Bot size={16} />}
                      {isUser ? t("Student") : message.role === "assistant" ? t("Tutor") : t("System")}
                    </div>
                    <span className="text-[12px] text-[var(--muted-foreground)]">
                      {formatTime(message.created_at)}
                    </span>
                  </div>
                  <div className="mt-3 whitespace-pre-wrap text-[14px] leading-6 text-[var(--foreground)]">
                    {message.content}
                  </div>
                </article>
              );
            })
          ) : (
            <div className="rounded-lg border border-[var(--border)] bg-[var(--card)] p-6 text-center text-[13px] text-[var(--muted-foreground)]">
              {t("This tutoring session does not have replayable message content yet.")}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
