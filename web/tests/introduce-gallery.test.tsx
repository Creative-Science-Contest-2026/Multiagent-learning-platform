import { fireEvent, render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { IntroduceGallery } from "../components/introduce/IntroduceGallery";
import { INTRODUCE_GALLERY_ITEMS } from "../components/introduce/introduce-content";

describe("IntroduceGallery", () => {
  it("renders the approved screenshots and opens a lightbox for the selected item", () => {
    render(<IntroduceGallery items={INTRODUCE_GALLERY_ITEMS} />);

    const primaryCard = screen.getByRole("button", { name: /^gói kiến thức \/ knowledge pack$/i });
    expect(
      screen.getByRole("button", {
        name: /^bảng điều khiển giáo viên \/ teacher dashboard$/i,
      }),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /^gia sư ai \/ ai tutor$/i })).toBeInTheDocument();

    fireEvent.click(primaryCard);

    const dialog = screen.getByRole("dialog", { name: /gói kiến thức/i });
    expect(dialog).toBeInTheDocument();
    expect(within(dialog).getByAltText(/^gói kiến thức$/i)).toHaveAttribute(
      "src",
      expect.stringContaining("anh1_goi_kien_thuc.jpg"),
    );

    fireEvent.click(screen.getByRole("button", { name: /đóng|close/i }));
    expect(screen.queryByRole("dialog", { name: /gói kiến thức/i })).not.toBeInTheDocument();
  });
});
