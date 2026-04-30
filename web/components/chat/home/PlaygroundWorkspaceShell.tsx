"use client";

import type { ReactNode } from "react";

interface PlaygroundWorkspaceShellProps {
  leftCollapsed?: boolean;
  rightCollapsed: boolean;
  rightWidth?: "compact" | "comfortable" | "expanded";
  left?: ReactNode;
  center: ReactNode;
  right: ReactNode;
}

export function PlaygroundWorkspaceShell({
  leftCollapsed = false,
  rightCollapsed,
  rightWidth = "comfortable",
  left,
  center,
  right,
}: PlaygroundWorkspaceShellProps) {
  const rightWidthClass =
    rightWidth === "compact"
      ? "w-[296px]"
      : rightWidth === "expanded"
        ? "w-[404px]"
        : "w-[332px]";

  return (
    <div className="flex h-[calc(100vh-3rem)] min-h-0 w-full bg-[var(--background)] text-[var(--foreground)]">
      {left ? (
        <aside
          className={`min-h-0 shrink-0 border-r border-[var(--border)] bg-[var(--secondary)]/35 transition-[width] duration-200 ${
            leftCollapsed ? "w-[92px]" : "w-[320px]"
          }`}
        >
          {left}
        </aside>
      ) : null}
      <main className="min-h-0 min-w-0 flex-1">{center}</main>
      <aside
        className={`min-h-0 shrink-0 border-l border-[var(--border)] bg-[var(--secondary)]/25 transition-[width,opacity] duration-200 ${
          rightCollapsed ? "w-0 overflow-hidden border-l-0 opacity-0" : `${rightWidthClass} opacity-100`
        }`}
      >
        {right}
      </aside>
    </div>
  );
}
