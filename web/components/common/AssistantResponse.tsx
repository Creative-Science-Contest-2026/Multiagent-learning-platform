"use client";

import MarkdownRenderer from "@/components/common/MarkdownRenderer";
import { hasVisibleMarkdownContent } from "@/lib/markdown-display";

interface AssistantResponseProps {
  content: string;
  className?: string;
}

export default function AssistantResponse({
  content,
  className = "text-[15px] leading-[1.85]",
}: AssistantResponseProps) {
  if (!hasVisibleMarkdownContent(content)) return null;

  return (
    <div className={className}>
      <MarkdownRenderer
        content={content}
        variant="prose"
        className="text-[var(--foreground)] [&_p]:my-0 [&_p+*]:mt-3"
      />
    </div>
  );
}
