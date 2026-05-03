import { render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

const replace = vi.fn();
const useAuth = vi.fn();

vi.mock("next/navigation", () => ({
  useRouter: () => ({ replace }),
  usePathname: () => "/dashboard",
}));

vi.mock("../context/AuthContext", () => ({
  useAuth,
}));

describe("TeacherSurfaceGate", () => {
  beforeEach(() => {
    replace.mockReset();
    useAuth.mockReset();
  });

  it("redirects unauthenticated users to login with next", async () => {
    useAuth.mockReturnValue({
      user: null,
      loading: false,
    });

    const { default: TeacherSurfaceGate } = await import("../components/auth/TeacherSurfaceGate");

    render(
      <TeacherSurfaceGate>
        <div>Teacher surface</div>
      </TeacherSurfaceGate>,
    );

    await waitFor(() => {
      expect(replace).toHaveBeenCalledWith("/login?next=%2Fdashboard");
    });
  });

  it("redirects students back to the student home", async () => {
    useAuth.mockReturnValue({
      user: {
        id: "student-1",
        email: "student@example.com",
        display_name: "Student One",
        role: "student",
      },
      loading: false,
    });

    const { default: TeacherSurfaceGate } = await import("../components/auth/TeacherSurfaceGate");

    render(
      <TeacherSurfaceGate>
        <div>Teacher surface</div>
      </TeacherSurfaceGate>,
    );

    await waitFor(() => {
      expect(replace).toHaveBeenCalledWith("/student");
    });
  });

  it("renders the surface for teacher users", async () => {
    useAuth.mockReturnValue({
      user: {
        id: "teacher-1",
        email: "teacher@example.com",
        display_name: "Teacher One",
        role: "teacher",
        email_verified_at: null,
      },
      loading: false,
      refreshUser: vi.fn(),
    });

    const { default: TeacherSurfaceGate } = await import("../components/auth/TeacherSurfaceGate");

    render(
      <TeacherSurfaceGate>
        <div>Teacher surface</div>
      </TeacherSurfaceGate>,
    );

    expect(await screen.findByText("Teacher surface")).toBeInTheDocument();
    expect(screen.getByText(/xác minh email để tăng độ tin cậy/i)).toBeInTheDocument();
    expect(replace).not.toHaveBeenCalled();
  });
});
