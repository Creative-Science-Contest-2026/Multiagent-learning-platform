"use client";

import type { PublicRole } from "@/lib/auth-api";

const ROLE_CARDS: Array<{
  role: PublicRole;
  title: string;
  subtitle: string;
  body: string;
}> = [
  {
    role: "teacher",
    title: "Giáo viên / Teacher",
    subtitle: "Tạo học liệu, đánh giá và can thiệp",
    body: "Dành cho người thiết kế gói kiến thức, giao bài, theo dõi tiến độ và đưa ra hành động sư phạm.",
  },
  {
    role: "student",
    title: "Học sinh / Student",
    subtitle: "Học với gia sư AI và theo dõi tiến bộ",
    body: "Dành cho người học cần hỏi đáp, làm bài đánh giá và xem tiến độ của riêng mình.",
  },
];

export default function RolePicker({
  selectedRole,
  onSelect,
}: {
  selectedRole: PublicRole;
  onSelect: (role: PublicRole) => void;
}) {
  return (
    <div className="grid gap-3 sm:grid-cols-2">
      {ROLE_CARDS.map((card) => {
        const active = selectedRole === card.role;
        return (
          <button
            key={card.role}
            type="button"
            aria-pressed={active}
            onClick={() => onSelect(card.role)}
            className={`rounded-[24px] border px-5 py-5 text-left transition-all ${
              active
                ? "border-[#0a1530] bg-[#0a1530] text-white shadow-[0_18px_40px_rgba(10,21,48,0.16)]"
                : "border-[rgba(10,21,48,0.1)] bg-[#f8f5ef] text-[#0a1530] hover:bg-white"
            }`}
          >
            <p className="text-base font-semibold tracking-[-0.03em]">{card.title}</p>
            <p className={`mt-2 text-sm font-medium ${active ? "text-white/78" : "text-[#50607d]"}`}>
              {card.subtitle}
            </p>
            <p className={`mt-3 text-sm leading-6 ${active ? "text-white/72" : "text-[#50607d]"}`}>
              {card.body}
            </p>
          </button>
        );
      })}
    </div>
  );
}
