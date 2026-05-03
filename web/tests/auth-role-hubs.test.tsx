import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

describe("role hubs", () => {
  it("teacher hub links into the core teacher workflow", async () => {
    const { default: TeacherPage } = await import("../app/teacher/page");

    render(<TeacherPage />);

    expect(screen.getByRole("link", { name: /gói kiến thức/i })).toHaveAttribute("href", "/knowledge");
    expect(screen.getByRole("link", { name: /dashboard lớp học/i })).toHaveAttribute("href", "/dashboard");
    expect(screen.getByRole("link", { name: /gia sư lớp học/i })).toHaveAttribute("href", "/agents");
  });

  it("student hub links into the core student workflow", async () => {
    const { default: StudentPage } = await import("../app/student/page");

    render(<StudentPage />);

    expect(screen.getByRole("link", { name: /vào gia sư ai/i })).toHaveAttribute("href", "/playground");
    expect(screen.getByRole("link", { name: /xem tiến độ học/i })).toHaveAttribute("href", "/dashboard/student");
    expect(screen.getByRole("link", { name: /mở tài liệu hướng dẫn/i })).toHaveAttribute("href", "/introduce");
  });
});
