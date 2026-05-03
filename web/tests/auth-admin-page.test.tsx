import { fireEvent } from "@testing-library/react";
import { render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

const createAdminUser = vi.fn();
const listAdminUsers = vi.fn();
const updateAdminUser = vi.fn();

vi.mock("../lib/auth-api", async () => {
  const actual = await vi.importActual("../lib/auth-api");
  return {
    ...actual,
    createAdminUser,
    listAdminUsers,
    updateAdminUser,
  };
});

describe("admin page", () => {
  beforeEach(() => {
    createAdminUser.mockReset();
    listAdminUsers.mockReset();
    updateAdminUser.mockReset();
  });

  it("loads and renders the current account roster", async () => {
    listAdminUsers.mockResolvedValue({
      users: [
        {
          id: "admin-1",
          email: "admin@example.com",
          display_name: "System Admin",
          role: "admin",
          status: "active",
          email_verified_at: "2026-05-03T00:00:00Z",
        },
        {
          id: "teacher-1",
          email: "teacher@example.com",
          display_name: "Teacher One",
          role: "teacher",
          status: "active",
          email_verified_at: null,
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
        email_verified_at: null,
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

  it("updates account role and status from the admin roster", async () => {
    listAdminUsers.mockResolvedValue({
      users: [
        {
          id: "teacher-1",
          email: "teacher@example.com",
          display_name: "Teacher One",
          role: "teacher",
          status: "active",
          email_verified_at: null,
        },
      ],
    });
    updateAdminUser.mockResolvedValue({
      user: {
        id: "teacher-1",
        email: "teacher@example.com",
        display_name: "Teacher One",
        role: "student",
        status: "suspended",
        email_verified_at: null,
      },
    });

    const { default: AdminPage } = await import("../app/admin/page");
    render(<AdminPage />);

    await waitFor(() => {
      expect(listAdminUsers).toHaveBeenCalled();
    });

    const selects = screen.getAllByRole("combobox");
    fireEvent.change(selects[0], { target: { value: "student" } });
    fireEvent.change(selects[1], { target: { value: "suspended" } });
    fireEvent.click(screen.getByRole("button", { name: /^lưu$/i }));

    await waitFor(() => {
      expect(updateAdminUser).toHaveBeenCalledWith("teacher-1", {
        role: "student",
        status: "suspended",
      });
    });
    expect(screen.getByDisplayValue("student")).toBeInTheDocument();
    expect(screen.getByDisplayValue("suspended")).toBeInTheDocument();
  });

  it("reloads the roster after a failed lifecycle update so local edits do not linger", async () => {
    listAdminUsers
      .mockResolvedValueOnce({
        users: [
          {
            id: "teacher-1",
            email: "teacher@example.com",
            display_name: "Teacher One",
            role: "teacher",
            status: "active",
            email_verified_at: null,
          },
        ],
      })
      .mockResolvedValueOnce({
        users: [
          {
            id: "teacher-1",
            email: "teacher@example.com",
            display_name: "Teacher One",
            role: "teacher",
            status: "active",
            email_verified_at: null,
          },
        ],
      });
    updateAdminUser.mockRejectedValue(new Error("update failed"));

    const { default: AdminPage } = await import("../app/admin/page");
    render(<AdminPage />);

    await waitFor(() => {
      expect(listAdminUsers).toHaveBeenCalledTimes(1);
    });

    const selects = screen.getAllByRole("combobox");
    fireEvent.change(selects[0], { target: { value: "student" } });
    fireEvent.change(selects[1], { target: { value: "suspended" } });
    fireEvent.click(screen.getByRole("button", { name: /^lưu$/i }));

    await waitFor(() => {
      expect(updateAdminUser).toHaveBeenCalled();
      expect(listAdminUsers).toHaveBeenCalledTimes(2);
    });

    const refreshedSelects = screen.getAllByRole("combobox");
    expect(refreshedSelects[0]).toHaveDisplayValue("teacher");
    expect(refreshedSelects[1]).toHaveDisplayValue("active");
  });
});
