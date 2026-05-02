import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

const push = vi.fn();
const login = vi.fn();
const googleLoginUrl = vi.fn((role?: string) => `/api/v1/auth/google/start?role=${role ?? "student"}`);
const appHomeForRole = vi.fn((role: string) => `/${role}`);

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push }),
}));

vi.mock("../lib/auth-api", () => ({
  login,
  googleLoginUrl,
  appHomeForRole,
}));

describe("login page", () => {
  it("renders email/password login and a Google CTA", async () => {
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
    expect(push).toHaveBeenCalledWith("/teacher");
  });
});
