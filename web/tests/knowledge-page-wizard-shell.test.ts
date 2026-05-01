import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const KNOWLEDGE_PAGE_PATH = resolve(
  process.cwd(),
  "app/(utility)/knowledge/page.tsx",
);

function readKnowledgePageSource(): string {
  return readFileSync(KNOWLEDGE_PAGE_PATH, "utf8");
}

describe("knowledge page wizard shell", () => {
  it("hides notebooks and provider selection from the main shell", () => {
    const source = readKnowledgePageSource();

    expect(source).not.toMatch(/setTab\(<"knowledge" \| "notebooks">/);
    expect(source).not.toMatch(/listRagProviders/);
    expect(source).not.toMatch(/selectedProvider/);
  });

  it("uses the wizard labels and difficulty choices", () => {
    const source = readKnowledgePageSource();

    expect(source).toMatch(/Thông tin/);
    expect(source).toMatch(/Tài liệu/);
    expect(source).toMatch(/Hoàn tất/);
    expect(source).toMatch(/Mức độ khó/);
    expect(source).toMatch(/Cơ bản/);
    expect(source).toMatch(/Trung bình/);
    expect(source).toMatch(/Nâng cao/);
  });
});
