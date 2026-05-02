import type { Metadata } from "next";
import { IntroducePageShell } from "@/components/introduce/IntroducePageShell";

export const metadata: Metadata = {
  title: "Giới thiệu sản phẩm | Product introduction",
  description:
    "Trang giới thiệu song ngữ cho ban giám khảo, đối tác và đội vận hành để hiểu nhanh sản phẩm, xem ảnh thực tế và đi vào tài liệu sử dụng.",
};

export default function IntroducePage() {
  return <IntroducePageShell />;
}
