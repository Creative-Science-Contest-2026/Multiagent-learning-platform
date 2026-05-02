import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import ProtectedRoute from "../components/auth/ProtectedRoute";

describe("ProtectedRoute", () => {
  it("blocks a student from a teacher-only surface", () => {
    render(
      <ProtectedRoute
        allow={["teacher"]}
        user={{
          id: "student-1",
          email: "student@example.com",
          display_name: "Student One",
          role: "student",
        }}
      >
        <div>Teacher shell</div>
      </ProtectedRoute>,
    );

    expect(screen.queryByText("Teacher shell")).toBeNull();
  });

  it("allows the matching role to see the surface", () => {
    render(
      <ProtectedRoute
        allow={["teacher"]}
        user={{
          id: "teacher-1",
          email: "teacher@example.com",
          display_name: "Teacher One",
          role: "teacher",
        }}
      >
        <div>Teacher shell</div>
      </ProtectedRoute>,
    );

    expect(screen.getByText("Teacher shell")).toBeInTheDocument();
  });
});
