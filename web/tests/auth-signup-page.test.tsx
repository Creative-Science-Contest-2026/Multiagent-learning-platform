import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

const push = vi.fn();
const signup = vi.fn();
const googleLoginUrl = vi.fn(
  (role: string, nextPath?: string | null) =>
    `/api/v1/auth/google/start?role=${role}${nextPath ? `&next=${encodeURIComponent(nextPath)}` : ""}`,
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
    signup,
    googleLoginUrl,
    postAuthRedirect,
  };
});

describe("signup page", () => {
  it("shows role selection and lets the user switch role before submit", async () => {
    signup.mockResolvedValue({
      user: {
        id: "user-1",
        email: "student@example.com",
        display_name: "Student One",
        role: "student",
      },
    });

    const { default: SignupPage } = await import("../app/signup/page");

    render(<SignupPage />);

    fireEvent.click(screen.getByRole("button", { name: /học sinh \/ student/i }));
    fireEvent.change(screen.getByLabelText(/họ và tên \/ full name/i), {
      target: { value: "Student One" },
    });
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "student@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/mật khẩu \/ password/i), {
      target: { value: "StrongPass123!" },
    });
    fireEvent.click(screen.getByRole("button", { name: /tạo tài khoản \/ create account/i }));

    await waitFor(() => {
      expect(signup).toHaveBeenCalledWith({
        display_name: "Student One",
        email: "student@example.com",
        password: "StrongPass123!",
        role: "student",
      });
    });
    expect(postAuthRedirect).toHaveBeenCalledWith("student", "/dashboard");
    expect(push).toHaveBeenCalledWith("/dashboard");
  }, 10000);
});
