export interface TeacherCockpitAction {
  title: string;
  description: string;
  href: string;
}

export function getTeacherCockpitPrimaryActions(): TeacherCockpitAction[] {
  return [
    {
      title: "Manage Knowledge Packs",
      description: "Create or refine the classroom source material before drafting practice.",
      href: "/knowledge",
    },
    {
      title: "Class tutor setup",
      description: "Set the teaching style, guardrails, and audience for the class tutor.",
      href: "/agents",
    },
    {
      title: "Teacher Dashboard",
      description: "Review diagnosis signals and choose the next classroom move.",
      href: "/dashboard",
    },
    {
      title: "Marketplace",
      description: "Browse reusable packs when you need a faster starting point.",
      href: "/marketplace",
    },
  ];
}

export function getTeacherCockpitSupportActions(): TeacherCockpitAction[] {
  return [
    {
      title: "Chat",
      description: "Open the broader workspace only when you need free-form tool exploration.",
      href: "/playground",
    },
  ];
}
