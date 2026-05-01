import { describe, expect, it } from "vitest";
import {
  hasVisibleMarkdownContent,
  normalizeMarkdownForDisplay,
} from "../lib/markdown-display";

describe("markdown display normalization", () => {
  it("removes empty details blocks", () => {
    const input = "Before\n\n<details><summary></summary></details>\n\nAfter";
    expect(normalizeMarkdownForDisplay(input)).toBe("Before\n\nAfter");
  });

  it("removes raw html control placeholders", () => {
    const input =
      "Before\n\n<progress></progress>\n<input type=\"text\" />\n<textarea> </textarea>\n\nAfter";
    expect(normalizeMarkdownForDisplay(input)).toBe("Before\n\nAfter");
  });

  it("removes empty markdown tables", () => {
    const input = "Before\n\n| |\n|---|\n\nAfter";
    expect(normalizeMarkdownForDisplay(input)).toBe("Before\n\nAfter");
  });

  it("removes empty html tables", () => {
    const input = "Before\n\n<table><tr><td>&nbsp;</td></tr></table>\n\nAfter";
    expect(normalizeMarkdownForDisplay(input)).toBe("Before\n\nAfter");
  });

  it("keeps meaningful tables", () => {
    const input = "Before\n\n| Topic |\n|---|\n| Math |\n\nAfter";
    expect(normalizeMarkdownForDisplay(input)).toBe(input);
  });

  it("rejects empty raw-html placeholders", () => {
    expect(hasVisibleMarkdownContent("<details><summary></summary></details>")).toBe(
      false,
    );
  });

  it("rejects raw html control placeholders", () => {
    expect(
      hasVisibleMarkdownContent("<progress></progress>\n<input type=\"text\" />"),
    ).toBe(false);
  });

  it("rejects empty markdown tables", () => {
    expect(hasVisibleMarkdownContent("| |\n|---|")).toBe(false);
  });

  it("keeps meaningful markdown", () => {
    expect(hasVisibleMarkdownContent("这是一个正常回复。\n\n- 第一条")).toBe(true);
  });
});
