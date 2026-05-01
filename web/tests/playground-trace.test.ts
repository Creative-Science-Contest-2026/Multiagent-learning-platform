import { describe, expect, it } from "vitest";

import { buildPlaygroundTraceRows } from "../lib/playground-trace";
import type { StreamEvent } from "../lib/unified-ws";

function event(type: StreamEvent["type"], content: string): StreamEvent {
  return {
    type,
    source: "chat",
    stage: "thinking",
    content,
    metadata: {},
    timestamp: 0,
  };
}

describe("playground trace rows", () => {
  it("merges consecutive thinking chunks into one readable row", () => {
    const rows = buildPlaygroundTraceRows([
      event("thinking", "Hello"),
      event("thinking", " "),
      event("thinking", "world"),
      event("thinking", "!"),
    ]);

    expect(rows).toEqual([
      {
        type: "thinking",
        content: "Hello world!",
      },
    ]);
  });

  it("preserves tool rows around merged thinking text", () => {
    const rows = buildPlaygroundTraceRows([
      event("thinking", "Need"),
      event("thinking", " tools"),
      event("tool_call", "web_search"),
      event("tool_result", "Found result"),
      event("thinking", "Done"),
    ]);

    expect(rows).toEqual([
      { type: "thinking", content: "Need tools" },
      { type: "tool_call", content: "web_search", event: event("tool_call", "web_search") },
      {
        type: "tool_result",
        content: "Found result",
        event: event("tool_result", "Found result"),
      },
      { type: "thinking", content: "Done" },
    ]);
  });
});
