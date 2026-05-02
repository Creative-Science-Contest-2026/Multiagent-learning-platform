import { fireEvent } from "@testing-library/react";
import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

const createAdminUser = vi.fn();
const listAdminUsers = vi.fn();

vi.mock("../lib/auth-api", async () => {
  const actual = await vi.importActual("../lib/auth-api");
  return {
    ...actual,
    createAdminUser,
    listAdminUsers,
  };
});

describe("admin page", () => {
  it("loads and renders the current account roster", async () => {
    listAdminUsers.mockResolvedValue({
      users: [
        {
          id: "admin-1",
          email: "admin@example.com",
          display_name: "System Admin",
          role: "admin",
          status: "active",
        },
        {
          id: "teacher-1",
          email: "teacher@example.com",
          display_name: "Teacher One",
          role: "teacher",
          status: "active",
        },
      ],
    });

    const { default: AdminPage } = await import("../app/admin/page");

    render(<AdminPage />);

    await waitFor(() => {
      expect(listAdminUsers).toHaveBeenCalled();
    });
    expect(screen.getByText("teacher@example.com")).toBeInTheDocument();
    expect(screen.getByText("System Admin")).toBeInTheDocument();
  });

  it("creates a new account from the admin panel and appends it to the roster", async () => {
    listAdminUsers.mockResolvedValue({ users: [] });
    createAdminUser.mockResolvedValue({
      user: {
        id: "student-2",
        email: "student2@example.com",
        display_name: "Student Two",
        role: "student",
        status: "active",
      },
    });

    const { default: AdminPage } = await import("../app/admin/page");

    render(<AdminPage />);

    await waitFor(() => {
      expect(listAdminUsers).toHaveBeenCalled();
    });

    fireEvent.change(screen.getByLabelText(/họ và tên/i), {
      target: { value: "Student Two" },
    });
    fireEvent.change(screen.getByLabelText(/^email$/i), {
      target: { value: "student2@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/mật khẩu tạm thời/i), {
      target: { value: "StrongPass123!" },
    });
    fireEvent.change(screen.getByLabelText(/vai trò/i), {
      target: { value: "student" },
    });
    fireEvent.click(screen.getByRole("button", { name: /tạo tài khoản/i }));

    await waitFor(() => {
      expect(createAdminUser).toHaveBeenCalledWith({
        display_name: "Student Two",
        email: "student2@example.com",
        password: "StrongPass123!",
        role: "student",
      });
    });
    expect(screen.getByText("student2@example.com")).toBeInTheDocument();
  });
});
