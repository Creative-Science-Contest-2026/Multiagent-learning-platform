import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import test from "node:test";

const SPEC_PACK_AUTHORING_TAB_PATH = resolve(
  process.cwd(),
  "components/agents/SpecPackAuthoringTab.tsx",
);

function readSource(): string {
  return readFileSync(SPEC_PACK_AUTHORING_TAB_PATH, "utf8");
}

test("tutor rules boolean field stacks safely on narrow widths", () => {
  const source = readSource();
  const booleanFieldSource = source.match(/function BooleanField\([\s\S]*?function SummaryRow/)?.[0] ?? "";

  assert.ok(booleanFieldSource.length > 0, "BooleanField source should be present");
  assert.match(booleanFieldSource, /flex-col/);
  assert.match(booleanFieldSource, /sm:flex-row/);
  assert.match(booleanFieldSource, /min-w-0/);
  assert.match(booleanFieldSource, /break-words/);
});
