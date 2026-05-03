import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

const push = vi.fn();
const logout = vi.fn();
const useAuth = vi.fn();

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push }),
}));

vi.mock("../context/AuthContext", () => ({
  useAuth,
}));

describe("SignedInAccountBar", () => {
  beforeEach(() => {
    push.mockReset();
    logout.mockReset();
    useAuth.mockReset();
  });

  it("renders the current identity, verification state, and logout action", async () => {
    logout.mockResolvedValue(undefined);
    useAuth.mockReturnValue({
      user: {
        id: "teacher-1",
        email: "teacher@example.com",
        display_name: "Teacher One",
        role: "teacher",
        email_verified_at: null,
      },
      logout,
    });

    const { default: SignedInAccountBar } = await import("../components/auth/SignedInAccountBar");
    render(<SignedInAccountBar />);

    expect(screen.getByText("Teacher One")).toBeInTheDocument();
    expect(screen.getByText("teacher@example.com")).toBeInTheDocument();
    expect(screen.getByText(/chưa xác minh email/i)).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: /đăng xuất/i }));

    await waitFor(() => {
      expect(logout).toHaveBeenCalledTimes(1);
    });
    expect(push).toHaveBeenCalledWith("/login");
  });

  it("routes the user to the verification page from the account bar", async () => {
    useAuth.mockReturnValue({
      user: {
        id: "student-1",
        email: "student@example.com",
        display_name: "Student One",
        role: "student",
        email_verified_at: "2026-05-03T10:00:00Z",
      },
      logout,
    });

    const { default: SignedInAccountBar } = await import("../components/auth/SignedInAccountBar");
    render(<SignedInAccountBar />);

    fireEvent.click(screen.getByRole("button", { name: /quản lý xác minh email/i }));

    expect(push).toHaveBeenCalledWith("/verify-email");
    expect(screen.getByText(/email đã xác minh/i)).toBeInTheDocument();
  });
});
