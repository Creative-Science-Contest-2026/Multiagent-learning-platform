import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

const push = vi.fn();
const login = vi.fn();
const googleLoginUrl = vi.fn(
  (role?: string, nextPath?: string | null) =>
    `/api/v1/auth/google/start?role=${role ?? "student"}${nextPath ? `&next=${encodeURIComponent(nextPath)}` : ""}`,
);
const postAuthRedirect = vi.fn((role: string, nextPath?: string | null) => nextPath || `/${role}`);
const searchParams = new URLSearchParams("next=/dashboard");

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push }),
  useSearchParams: () => searchParams,
}));

vi.mock("../lib/auth-api", async () => {
  const actual = await vi.importActual("../lib/auth-api");
  return {
    ...actual,
    login,
    googleLoginUrl,
    postAuthRedirect,
  };
});

describe("login page", () => {
  it("returns the user to the requested page and forwards Google role selection", async () => {
    login.mockResolvedValue({
      user: {
        id: "teacher-1",
        email: "teacher@example.com",
        display_name: "Teacher One",
        role: "teacher",
      },
    });

    const { default: LoginPage } = await import("../app/login/page");

    render(<LoginPage />);

    expect(screen.getByRole("button", { name: /tiếp tục với google \/ continue with google/i })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: /giáo viên \/ teacher/i }));

    fireEvent.change(screen.getByLabelText(/^email$/i), {
      target: { value: "teacher@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/mật khẩu \/ password/i), {
      target: { value: "StrongPass123!" },
    });
    fireEvent.click(screen.getByRole("button", { name: /đăng nhập \/ sign in/i }));

    await waitFor(() => {
      expect(login).toHaveBeenCalledWith({
        email: "teacher@example.com",
        password: "StrongPass123!",
      });
    });
    expect(postAuthRedirect).toHaveBeenCalledWith("teacher", "/dashboard");
    expect(push).toHaveBeenCalledWith("/dashboard");

    const originalLocation = window.location;
    const assignSpy = vi.fn();
    Object.defineProperty(window, "location", {
      configurable: true,
      value: { ...originalLocation, assign: assignSpy },
    });
    fireEvent.click(screen.getByRole("button", { name: /tiếp tục với google \/ continue with google/i }));
    expect(googleLoginUrl).toHaveBeenCalledWith("teacher", "/dashboard");
    expect(assignSpy).toHaveBeenCalledWith("/api/v1/auth/google/start?role=teacher&next=%2Fdashboard");
    Object.defineProperty(window, "location", {
      configurable: true,
      value: originalLocation,
    });
  }, 10000);
});
