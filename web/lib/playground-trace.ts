import type { StreamEvent } from "./unified-ws";

export type PlaygroundTraceRow =
  | {
      type: "thinking";
      content: string;
    }
  | {
      type: "progress" | "tool_call" | "tool_result" | "error";
      content: string;
      event: StreamEvent;
    };

export function buildPlaygroundTraceRows(events: StreamEvent[]): PlaygroundTraceRow[] {
  const rows: PlaygroundTraceRow[] = [];
  let thinkingBuffer = "";

  function flushThinking() {
    if (!thinkingBuffer) return;
    rows.push({ type: "thinking", content: thinkingBuffer });
    thinkingBuffer = "";
  }

  for (const event of events) {
    if (event.type === "thinking") {
      thinkingBuffer += event.content;
      continue;
    }

    flushThinking();

    if (
      event.type === "progress" ||
      event.type === "tool_call" ||
      event.type === "tool_result" ||
      event.type === "error"
    ) {
      rows.push({
        type: event.type,
        content: event.content,
        event,
      });
    }
  }

  flushThinking();
  return rows;
}
