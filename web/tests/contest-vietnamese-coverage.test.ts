import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

function readLocale(locale: "en" | "vi"): Record<string, string> {
  return JSON.parse(
    readFileSync(resolve(import.meta.dirname, `../locales/${locale}/app.json`), "utf8"),
  ) as Record<string, string>;
}

test("teacher cockpit action descriptions exist in Vietnamese", () => {
  const vi = readLocale("vi");

  assert.equal(
    vi["Create or refine the classroom source material before drafting practice."],
    "Tạo mới hoặc tinh chỉnh học liệu nguồn của lớp học trước khi soạn phần luyện tập.",
  );
  assert.equal(
    vi["Open the broader workspace only when you need free-form tool exploration."],
    "Chỉ mở không gian làm việc rộng hơn khi bạn cần khám phá công cụ theo cách tự do.",
  );
});

test("spec-pack authoring Vietnamese fallbacks and templates exist", () => {
  const vi = readLocale("vi");

  assert.equal(vi["No subject yet"], "Chưa có môn học");
  assert.equal(vi["No language yet"], "Chưa có ngôn ngữ");
  assert.equal(vi["No direct-answer rule yet"], "Chưa có quy tắc cấm trả lời trực tiếp");
  assert.match(vi["Spec template CURRICULUM.md"], /Chương trình học/);
  assert.match(vi["Spec template WORKFLOW.md"], /Luồng buổi học/);
});
