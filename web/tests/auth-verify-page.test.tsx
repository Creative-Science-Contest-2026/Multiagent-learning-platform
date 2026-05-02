import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

const verifyEmailToken = vi.fn();
const sendVerificationEmail = vi.fn();
let tokenValue = "";

vi.mock("next/navigation", () => ({
  useSearchParams: () => new URLSearchParams(tokenValue ? { token: tokenValue } : {}),
}));

vi.mock("../lib/auth-api", async () => {
  const actual = await vi.importActual("../lib/auth-api");
  return {
    ...actual,
    sendVerificationEmail,
    verifyEmailToken,
  };
});

describe("verify email page", () => {
  it("verifies the token from the URL and shows a success state", async () => {
    tokenValue = "verify-token-123";
    verifyEmailToken.mockResolvedValue({ ok: true });

    const { default: VerifyEmailPage } = await import("../app/verify-email/page");

    render(<VerifyEmailPage />);

    fireEvent.click(screen.getByRole("button", { name: /xác minh email/i }));

    await waitFor(() => {
      expect(verifyEmailToken).toHaveBeenCalledWith("verify-token-123");
    });
    expect(screen.getByText(/email đã được xác minh/i)).toBeInTheDocument();
    tokenValue = "";
  });
});
