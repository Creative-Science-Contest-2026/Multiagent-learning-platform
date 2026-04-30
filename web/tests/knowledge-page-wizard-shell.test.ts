import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const KNOWLEDGE_PAGE_PATH = resolve(
  process.cwd(),
  "app/(utility)/knowledge/page.tsx",
);

function readKnowledgePageSource(): string {
  return readFileSync(KNOWLEDGE_PAGE_PATH, "utf8");
}

test("knowledge page hides notebooks and provider selection from the main shell", () => {
  const source = readKnowledgePageSource();

  assert.doesNotMatch(source, /setTab\(<"knowledge" \| "notebooks">/);
  assert.doesNotMatch(source, /listRagProviders/);
  assert.doesNotMatch(source, /selectedProvider/);
});

test("knowledge page uses the wizard labels and difficulty choices", () => {
  const source = readKnowledgePageSource();

  assert.match(source, /Thông tin/);
  assert.match(source, /Tài liệu/);
  assert.match(source, /Hoàn tất/);
  assert.match(source, /Mức độ khó/);
  assert.match(source, /Cơ bản/);
  assert.match(source, /Trung bình/);
  assert.match(source, /Nâng cao/);
});
