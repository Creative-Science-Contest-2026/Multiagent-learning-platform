"use client";

import type { ReactNode } from "react";

interface PlaygroundRightPanelProps {
  badge: string;
  title: string;
  description?: string;
  children: ReactNode;
}

export function PlaygroundRightPanel({
  badge,
  title,
  description,
  children,
}: PlaygroundRightPanelProps) {
  return (
    <div className="flex h-full min-h-0 flex-col">
      <div className="border-b border-[var(--border)] px-5 py-5">
        <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-[var(--muted-foreground)]">
          {badge}
        </p>
        <h2 className="mt-2 text-lg font-semibold tracking-tight text-[var(--foreground)]">
          {title}
        </h2>
        {description ? (
          <p className="mt-2 text-[13px] leading-6 text-[var(--muted-foreground)]">{description}</p>
        ) : null}
      </div>
      <div className="min-h-0 flex-1 overflow-y-auto px-5 py-5">{children}</div>
    </div>
  );
}
