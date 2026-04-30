"use client";

import Link from "next/link";
import { ArrowRight, BookOpen, Bot, LayoutDashboard, MessageSquare, Store } from "lucide-react";
import { useTranslation } from "react-i18next";
import { CoreLoopVisibilityStrip } from "@/components/contest/CoreLoopVisibilityStrip";
import {
  getTeacherCockpitPrimaryActions,
  getTeacherCockpitSupportActions,
} from "@/components/contest/teacher-cockpit-content";

const ACTION_ICONS = {
  "/knowledge": BookOpen,
  "/agents": Bot,
  "/dashboard": LayoutDashboard,
  "/marketplace": Store,
  "/playground": MessageSquare,
} as const;

export function TeacherCockpit() {
  const { t } = useTranslation();
  const primaryActions = getTeacherCockpitPrimaryActions();
  const supportActions = getTeacherCockpitSupportActions();

  return (
    <main className="h-full overflow-y-auto bg-[var(--background)]">
      <div className="mx-auto flex w-full max-w-[1200px] flex-col gap-6 px-4 py-8 sm:px-6">
        <section className="rounded-3xl border border-[var(--border)] bg-[var(--card)] p-6 shadow-sm">
          <div className="flex flex-col gap-4">
            <div>
              <p className="text-[12px] font-semibold uppercase tracking-[0.12em] text-[var(--muted-foreground)]">
                {t("Teacher-controlled adaptive loop")}
              </p>
              <h1 className="mt-2 text-[30px] font-semibold tracking-tight text-[var(--foreground)]">
                {t("Classroom setup comes first")}
              </h1>
              <p className="mt-2 max-w-[720px] text-[14px] leading-6 text-[var(--muted-foreground)]">
                {t("Prepare the Knowledge Pack, shape the class tutor, then move into assessment and teacher review with one bounded classroom flow.")}
              </p>
            </div>

            <CoreLoopVisibilityStrip
              currentStep="Knowledge Pack"
              nextStep="Assessment"
              helperText={t("Start from teacher-owned classroom context, then move forward through assessment, tutoring, diagnosis, and intervention.")}
            />
          </div>
        </section>

        <section className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-5 shadow-sm">
          <div className="mb-4">
            <div className="text-[12px] font-semibold uppercase tracking-[0.12em] text-[var(--muted-foreground)]">
              {t("Quick Actions")}
            </div>
            <h2 className="mt-1 text-[22px] font-semibold tracking-tight text-[var(--foreground)]">
              {t("Move through the teacher workflow")}
            </h2>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            {primaryActions.map((action) => {
              const Icon = ACTION_ICONS[action.href as keyof typeof ACTION_ICONS] ?? BookOpen;
              return (
                <Link
                  key={action.href}
                  href={action.href}
                  className="group rounded-2xl border border-[var(--border)] bg-[var(--background)] p-4 transition hover:border-[var(--foreground)]/30 hover:bg-[var(--background)]/80"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="rounded-xl bg-[var(--secondary)] p-3 text-[var(--foreground)]">
                      <Icon className="h-5 w-5" />
                    </div>
                    <ArrowRight className="mt-1 h-4 w-4 text-[var(--muted-foreground)] transition group-hover:text-[var(--foreground)]" />
                  </div>
                  <div className="mt-4 min-w-0">
                    <div className="text-[15px] font-medium text-[var(--foreground)]">{t(action.title)}</div>
                    <p className="mt-1 break-words text-[13px] leading-6 text-[var(--muted-foreground)]">
                      {t(action.description)}
                    </p>
                  </div>
                </Link>
              );
            })}
          </div>
        </section>

        <section className="rounded-2xl border border-[var(--border)] bg-[var(--card)] p-5 shadow-sm">
          <div className="mb-3 text-[12px] font-semibold uppercase tracking-[0.12em] text-[var(--muted-foreground)]">
            {t("Secondary tools")}
          </div>
          <div className="grid gap-4 md:grid-cols-2">
            {supportActions.map((action) => {
              const Icon = ACTION_ICONS[action.href as keyof typeof ACTION_ICONS] ?? MessageSquare;
              return (
                <Link
                  key={action.href}
                  href={action.href}
                  className="rounded-2xl border border-dashed border-[var(--border)] bg-[var(--background)] p-4 transition hover:border-[var(--foreground)]/30"
                >
                  <div className="flex items-start gap-3">
                    <div className="rounded-xl bg-[var(--secondary)] p-3 text-[var(--foreground)]">
                      <Icon className="h-5 w-5" />
                    </div>
                    <div className="min-w-0">
                      <div className="text-[15px] font-medium text-[var(--foreground)]">{t(action.title)}</div>
                      <p className="mt-1 break-words text-[13px] leading-6 text-[var(--muted-foreground)]">
                        {t(action.description)}
                      </p>
                    </div>
                  </div>
                </Link>
              );
            })}
          </div>
        </section>
      </div>
    </main>
  );
}
