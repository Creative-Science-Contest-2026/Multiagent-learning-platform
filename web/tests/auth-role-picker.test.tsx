import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import RolePicker from "../components/auth/RolePicker";

describe("RolePicker", () => {
  it("renders teacher and student options and reports the selected role", () => {
    const onSelect = vi.fn();

    render(<RolePicker selectedRole="teacher" onSelect={onSelect} />);

    fireEvent.click(screen.getByRole("button", { name: /học sinh \/ student/i }));

    expect(onSelect).toHaveBeenCalledWith("student");
  });
});
