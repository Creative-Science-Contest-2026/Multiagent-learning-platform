import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const TEST_DIR = dirname(fileURLToPath(import.meta.url));

function readLocale(locale: "en" | "vi"): Record<string, string> {
  return JSON.parse(
    readFileSync(resolve(TEST_DIR, `../locales/${locale}/app.json`), "utf8"),
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

test("playground workspace Vietnamese labels exist", () => {
  const vi = readLocale("vi");

  assert.equal(vi["Conversation workspace"], "Không gian hội thoại");
  assert.equal(vi["Conversation history"], "Lịch sử cuộc trò chuyện");
  assert.equal(vi["Today"], "Hôm nay");
  assert.equal(vi["Yesterday"], "Hôm qua");
  assert.equal(vi["Untitled chat"], "Cuộc trò chuyện chưa có tiêu đề");
});
