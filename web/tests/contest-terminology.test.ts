import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

function readLocale(locale: "en" | "vi"): Record<string, string> {
  return JSON.parse(
    readFileSync(resolve(import.meta.dirname, `../locales/${locale}/app.json`), "utf8"),
  ) as Record<string, string>;
}

test("contest terminology keys exist in the English locale", () => {
  const en = readLocale("en");

  assert.equal(en["Knowledge Packs"], "Knowledge Packs");
  assert.equal(en["Teacher dashboard"], "Teacher dashboard");
  assert.equal(en["Class tutor"], "Class tutor");
  assert.equal(en["Tutor setup"], "Tutor setup");
  assert.equal(en["Teaching styles"], "Teaching styles");
});

test("contest terminology keys exist in the Vietnamese locale", () => {
  const vi = readLocale("vi");

  assert.equal(vi["Knowledge Packs"], "Gói kiến thức");
  assert.equal(vi["Teacher dashboard"], "Bảng điều khiển giáo viên");
  assert.equal(vi["Class tutor"], "Gia sư lớp học");
  assert.equal(vi["Tutor setup"], "Thiết lập gia sư");
  assert.equal(vi["Teaching styles"], "Phong cách giảng dạy");
});
