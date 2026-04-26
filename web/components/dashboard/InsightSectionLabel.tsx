import type { ReactNode } from "react";

export function InsightSectionLabel({
  eyebrow,
  title,
  toneClassName = "text-[var(--muted-foreground)]",
  children,
}: {
  eyebrow: string;
  title: string;
  toneClassName?: string;
  children?: ReactNode;
}) {
  return (
    <div className="space-y-1">
      <div className={`text-[11px] font-semibold uppercase tracking-[0.12em] ${toneClassName}`}>
        {eyebrow}
      </div>
      <div className="text-[14px] font-medium text-[var(--foreground)]">{title}</div>
      {children ? <div className="text-[12px] text-[var(--muted-foreground)]">{children}</div> : null}
    </div>
  );
}
