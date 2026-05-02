import { describe, expect, it } from "vitest";
import {
  INTRODUCE_GALLERY_ITEMS,
  INTRODUCE_QUICK_FACTS,
  INTRODUCE_SECTIONS,
} from "../components/introduce/introduce-content";

describe("introduce content", () => {
  it("keeps the seven approved screenshots in the expected order", () => {
    expect(INTRODUCE_GALLERY_ITEMS.map((item) => item.src)).toEqual([
      "/introduce/anh1_goi_kien_thuc.jpg",
      "/introduce/anh2_bang_dieu_khien_giao_vien.jpg",
      "/introduce/anh3_gia_su.jpg",
      "/introduce/anh4_thi_truong.jpg",
      "/introduce/anh5_tro_chuyen.jpg",
      "/introduce/anh6_bo_nho.jpg",
      "/introduce/anh7_cai_dat.jpg",
    ]);
  });

  it("keeps the page sections aligned with the approved docs sitemap", () => {
    expect(INTRODUCE_SECTIONS.map((section) => section.id)).toEqual([
      "overview",
      "core-loop",
      "evidence-gallery",
      "for-educators",
      "technical-documentation",
      "faq",
      "resources",
    ]);
  });

  it("keeps the quick facts bounded to honest prototype claims", () => {
    expect(INTRODUCE_QUICK_FACTS.some((fact) => /prototype/i.test(fact.vi))).toBe(true);
    expect(INTRODUCE_QUICK_FACTS.some((fact) => /Giáo dục/.test(fact.vi))).toBe(true);
  });
});
