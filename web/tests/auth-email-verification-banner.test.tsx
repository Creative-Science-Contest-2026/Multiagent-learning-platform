import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

const refreshUser = vi.fn();
const sendVerificationEmail = vi.fn();
const useAuth = vi.fn();

vi.mock("../context/AuthContext", () => ({
  useAuth,
}));

vi.mock("../lib/auth-api", async () => {
  const actual = await vi.importActual("../lib/auth-api");
  return {
    ...actual,
    sendVerificationEmail,
  };
});

describe("EmailVerificationBanner", () => {
  beforeEach(() => {
    refreshUser.mockReset();
    sendVerificationEmail.mockReset();
    useAuth.mockReset();
  });

  it("stays hidden when the signed-in user is already verified", async () => {
    useAuth.mockReturnValue({
      user: {
        id: "teacher-1",
        email: "teacher@example.com",
        display_name: "Teacher One",
        role: "teacher",
        email_verified_at: "2026-05-03T00:00:00Z",
      },
      refreshUser,
    });

    const { default: EmailVerificationBanner } = await import("../components/auth/EmailVerificationBanner");
    const { container } = render(<EmailVerificationBanner />);

    expect(container).toBeEmptyDOMElement();
  });

  it("can resend verification email and expose the local debug link when available", async () => {
    useAuth.mockReturnValue({
      user: {
        id: "teacher-1",
        email: "teacher@example.com",
        display_name: "Teacher One",
        role: "teacher",
        email_verified_at: null,
      },
      refreshUser,
    });
    sendVerificationEmail.mockResolvedValue({
      ok: true,
      debug_url: "/verify-email?token=debug-token",
    });

    const { default: EmailVerificationBanner } = await import("../components/auth/EmailVerificationBanner");
    render(<EmailVerificationBanner />);

    fireEvent.click(screen.getByRole("button", { name: /gửi lại email xác minh/i }));

    await waitFor(() => {
      expect(sendVerificationEmail).toHaveBeenCalledTimes(1);
    });
    expect(screen.getByRole("link", { name: /mở liên kết xác minh cục bộ/i })).toHaveAttribute(
      "href",
      "/verify-email?token=debug-token",
    );
  });

  it("refreshes the auth user after the learner says verification is complete", async () => {
    useAuth.mockReturnValue({
      user: {
        id: "student-1",
        email: "student@example.com",
        display_name: "Student One",
        role: "student",
        email_verified_at: null,
      },
      refreshUser,
    });
    refreshUser.mockResolvedValue({
      id: "student-1",
      email: "student@example.com",
      display_name: "Student One",
      role: "student",
      email_verified_at: "2026-05-03T01:00:00Z",
    });

    const { default: EmailVerificationBanner } = await import("../components/auth/EmailVerificationBanner");
    render(<EmailVerificationBanner />);

    fireEvent.click(screen.getByRole("button", { name: /tôi đã xác minh xong, tải lại trạng thái/i }));

    await waitFor(() => {
      expect(refreshUser).toHaveBeenCalledTimes(1);
    });
    expect(screen.getByText(/trạng thái tài khoản đã được cập nhật/i)).toBeInTheDocument();
  });
});
