export interface SidebarNavItem {
  href: string;
  label: string;
  icon: "message-square" | "bot" | "pen-line" | "graduation-cap" | "bar-chart-3" | "book-open" | "store" | "brain";
}

export interface SidebarNavGroup {
  id: "contest-core" | "secondary-tools";
  label: string;
  items: SidebarNavItem[];
}

const CONTEST_CORE_ITEMS: SidebarNavItem[] = [
  { href: "/knowledge", label: "Knowledge", icon: "book-open" },
  { href: "/dashboard", label: "Dashboard", icon: "bar-chart-3" },
  { href: "/agents", label: "TutorBot", icon: "bot" },
  { href: "/marketplace", label: "Marketplace", icon: "store" },
];

const SECONDARY_TOOL_ITEMS: SidebarNavItem[] = [
  { href: "/", label: "Chat", icon: "message-square" },
  { href: "/guide", label: "Guided Learning", icon: "graduation-cap" },
  { href: "/co-writer", label: "Co-Writer", icon: "pen-line" },
  { href: "/memory", label: "Memory", icon: "brain" },
];

export function getExpandedSidebarGroups(): SidebarNavGroup[] {
  return [
    { id: "contest-core", label: "Contest core", items: CONTEST_CORE_ITEMS },
    { id: "secondary-tools", label: "Secondary tools", items: SECONDARY_TOOL_ITEMS },
  ];
}

export function getCollapsedSidebarNav(): SidebarNavItem[] {
  return CONTEST_CORE_ITEMS;
}
