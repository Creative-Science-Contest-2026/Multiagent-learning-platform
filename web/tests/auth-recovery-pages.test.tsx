import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

const push = vi.fn();
const requestPasswordReset = vi.fn();
const resetPassword = vi.fn();

let tokenValue = "";

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push }),
  useSearchParams: () => new URLSearchParams(tokenValue ? { token: tokenValue } : {}),
}));

vi.mock("../lib/auth-api", async () => {
  const actual = await vi.importActual("../lib/auth-api");
  return {
    ...actual,
    requestPasswordReset,
    resetPassword,
  };
});

describe("auth recovery pages", () => {
  it("submits forgot-password email and shows a recovery link when debug delivery is available", async () => {
    requestPasswordReset.mockResolvedValue({
      ok: true,
      debug_url: "/reset-password?token=debug-token",
    });

    const { default: ForgotPasswordPage } = await import("../app/forgot-password/page");

    render(<ForgotPasswordPage />);

    fireEvent.change(screen.getByLabelText(/^email$/i), {
      target: { value: "teacher@example.com" },
    });
    fireEvent.click(screen.getByRole("button", { name: /gửi liên kết/i }));

    await waitFor(() => {
      expect(requestPasswordReset).toHaveBeenCalledWith("teacher@example.com");
    });
    expect(screen.getByRole("link", { name: /mở liên kết khôi phục/i })).toHaveAttribute(
      "href",
      "/reset-password?token=debug-token",
    );
  });

  it("submits a new password with the reset token from the URL", async () => {
    tokenValue = "reset-token-123";
    resetPassword.mockResolvedValue({ ok: true });

    const { default: ResetPasswordPage } = await import("../app/reset-password/page");

    render(<ResetPasswordPage />);

    fireEvent.change(screen.getByLabelText(/mật khẩu mới \/ new password/i), {
      target: { value: "EvenStronger456!" },
    });
    fireEvent.click(screen.getByRole("button", { name: /đặt lại mật khẩu/i }));

    await waitFor(() => {
      expect(resetPassword).toHaveBeenCalledWith({
        token: "reset-token-123",
        password: "EvenStronger456!",
      });
    });
    expect(push).toHaveBeenCalledWith("/login");
    tokenValue = "";
  });
});
