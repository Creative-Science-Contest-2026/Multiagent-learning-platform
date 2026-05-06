import { readFileSync } from "node:fs";
import { resolve } from "node:path";

import { describe, expect, it } from "vitest";

const PROTECTED_FILES = [
  "app/(utility)/knowledge/page.tsx",
  "app/(utility)/memory/page.tsx",
  "app/(utility)/settings/page.tsx",
  "app/(workspace)/guide/hooks/useGuideHistory.ts",
  "app/(workspace)/guide/hooks/useGuideSession.ts",
  "app/(workspace)/agents/[botId]/chat/page.tsx",
  "app/(workspace)/agents/page.tsx",
  "app/(workspace)/co-writer/page.tsx",
  "app/(workspace)/playground/page.tsx",
  "components/notebook/SaveToNotebookModal.tsx",
  "components/sidebar/TutorBotRecent.tsx",
  "lib/knowledge-api.ts",
  "lib/dashboard-api.ts",
  "lib/marketplace-api.ts",
  "lib/notebook-api.ts",
  "lib/agent-spec-api.ts",
];

function readWebSource(relativePath: string): string {
  return readFileSync(resolve(process.cwd(), relativePath), "utf8");
}

describe("protected frontend API fetch hardening", () => {
  it("does not leave raw authenticated fetch(apiUrl(...)) calls in the protected surface", () => {
    for (const relativePath of PROTECTED_FILES) {
      const source = readWebSource(relativePath);
      expect(source, relativePath).not.toMatch(/fetch\s*\(\s*apiUrl\s*\(/);
    }
  });
});
