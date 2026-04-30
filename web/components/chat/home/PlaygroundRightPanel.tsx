"use client";

import type { ReactNode } from "react";

interface PlaygroundRightPanelProps {
  badge: string;
  title: string;
  description?: string;
  headerActions?: ReactNode;
  children: ReactNode;
}

export function PlaygroundRightPanel({
  badge,
  title,
  description,
  headerActions,
  children,
}: PlaygroundRightPanelProps) {
  return (
    <div className="flex h-full min-h-0 flex-col">
      <div className="border-b border-[var(--border)]/60 bg-[var(--background)]/45 px-4 py-4">
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-[var(--muted-foreground)]">
              {badge}
            </p>
            <h2 className="mt-1.5 text-base font-semibold tracking-tight text-[var(--foreground)]">
              {title}
            </h2>
          </div>
          {headerActions ? <div className="shrink-0">{headerActions}</div> : null}
        </div>
        {description ? (
          <p className="mt-1.5 max-w-[28rem] text-[12px] leading-5 text-[var(--muted-foreground)]/95">{description}</p>
        ) : null}
      </div>
      <div className="min-h-0 flex-1 overflow-y-auto px-4 py-4">{children}</div>
    </div>
  );
}
