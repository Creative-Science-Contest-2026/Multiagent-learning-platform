import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import IntroducePage, { metadata } from "../app/introduce/page";

describe("/introduce page", () => {
  it("exports route metadata and renders the approved docs navigation", () => {
    expect(typeof metadata.title).toBe("string");
    expect(metadata.title).toMatch(/introduce|giới thiệu/i);

    render(<IntroducePage />);

    expect(
      screen.getByRole("heading", { name: /giới thiệu sản phẩm|product introduction/i, level: 1 }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("link", { name: /tổng quan.*overview|overview.*tổng quan/i }),
    ).toHaveAttribute("href", "#overview");
    expect(
      screen.getByRole("link", {
        name: /hình ảnh thực tế.*evidence gallery|evidence gallery.*hình ảnh thực tế/i,
      }),
    ).toHaveAttribute("href", "#evidence-gallery");
    expect(
      screen.getByText(/knowledge pack\s*->\s*assessment\s*->\s*tutor\s*->\s*diagnosis\s*->\s*intervention/i),
    ).toBeInTheDocument();
  });
});
