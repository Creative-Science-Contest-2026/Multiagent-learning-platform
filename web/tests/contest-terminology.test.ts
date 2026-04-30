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
  assert.equal(en["Linked Knowledge Pack"], "Linked Knowledge Pack");
  assert.equal(en["Step 2 of classroom setup"], "Step 2 of classroom setup");
  assert.equal(en["Tutor identity section"], "Tutor identity section");
  assert.equal(en["Tutor teaching style section"], "Tutor teaching style section");
  assert.equal(en["Tutor rules section"], "Tutor rules section");
  assert.equal(en["Classroom flow"], "Classroom flow");
  assert.equal(en["Current pack"], "Current pack");
  assert.equal(en["Nhìn nhanh lớp học hôm nay"], "Quick view of the classroom today");
  assert.equal(en["Học sinh cần giáo viên xem trước"], "Students for the teacher to review first");
});

test("contest terminology keys exist in the Vietnamese locale", () => {
  const vi = readLocale("vi");

  assert.equal(vi["Knowledge Packs"], "Gói kiến thức");
  assert.equal(vi["Teacher dashboard"], "Bảng điều khiển giáo viên");
  assert.equal(vi["Class tutor"], "Gia sư lớp học");
  assert.equal(vi["Tutor setup"], "Thiết lập gia sư");
  assert.equal(vi["Teaching styles"], "Phong cách giảng dạy");
  assert.equal(vi["Linked Knowledge Pack"], "Gói kiến thức đang gắn");
  assert.equal(vi["Step 2 of classroom setup"], "Bước 2 của thiết lập lớp học");
  assert.equal(vi["Tutor identity section"], "Thông tin gia sư");
  assert.equal(vi["Tutor teaching style section"], "Phong cách giảng dạy");
  assert.equal(vi["Tutor rules section"], "Quy tắc và giới hạn");
  assert.equal(vi["Classroom flow"], "Luồng lớp học");
  assert.equal(vi["Current pack"], "Gói hiện tại");
  assert.equal(vi["Nhìn nhanh lớp học hôm nay"], "Nhìn nhanh lớp học hôm nay");
  assert.equal(vi["Học sinh cần giáo viên xem trước"], "Học sinh cần giáo viên xem trước");
});
