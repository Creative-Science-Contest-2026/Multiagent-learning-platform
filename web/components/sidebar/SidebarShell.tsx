"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState, type ReactNode } from "react";
import {
  BookOpen,
  Bot,
  BarChart3,
  Brain,
  GraduationCap,
  MessageSquare,
  PanelLeftClose,
  PanelLeftOpen,
  PenLine,
  Plus,
  Settings,
  Store,
  type LucideIcon,
} from "lucide-react";
import { useTranslation } from "react-i18next";
import SessionList from "@/components/SessionList";
import { TutorBotRecent } from "@/components/sidebar/TutorBotRecent";
import {
  getCollapsedSidebarNav,
  getExpandedSidebarGroups,
  type SidebarNavItem,
} from "@/components/sidebar/nav-groups";
import type { SessionSummary } from "@/lib/session-api";

interface NavEntry {
  href: string;
  label: string;
  icon: LucideIcon;
}

const SECONDARY_NAV: NavEntry[] = [{ href: "/settings", label: "Settings", icon: Settings }];

function getContestLabel(label: string): string {
  switch (label) {
    case "Knowledge":
      return "Knowledge Packs";
    case "Dashboard":
      return "Teacher dashboard";
    case "TutorBot":
      return "Class tutor";
    case "Contest core":
      return "Classroom workflow";
    case "Secondary tools":
      return "Other tools";
    default:
      return label;
  }
}

function resolveNavIcon(icon: SidebarNavItem["icon"]): LucideIcon {
  switch (icon) {
    case "message-square":
      return MessageSquare;
    case "bot":
      return Bot;
    case "pen-line":
      return PenLine;
    case "graduation-cap":
      return GraduationCap;
    case "bar-chart-3":
      return BarChart3;
    case "book-open":
      return BookOpen;
    case "store":
      return Store;
    case "brain":
      return Brain;
  }
}

interface SidebarShellProps {
  shellMode?: "chat" | "business";
  sessions?: SessionSummary[];
  activeSessionId?: string | null;
  loadingSessions?: boolean;
  onNewChat?: () => void;
  onSelectSession?: (sessionId: string) => void | Promise<void>;
  onRenameSession?: (sessionId: string, title: string) => void | Promise<void>;
  onDeleteSession?: (sessionId: string) => void | Promise<void>;
  footerSlot?: ReactNode;
}

export function SidebarShell({
  shellMode = "business",
  sessions = [],
  activeSessionId = null,
  loadingSessions = false,
  onNewChat,
  onSelectSession,
  onRenameSession,
  onDeleteSession,
  footerSlot,
}: SidebarShellProps) {
  const pathname = usePathname();
  const router = useRouter();
  const { t } = useTranslation();
  const [collapsed, setCollapsed] = useState(false);
  const collapsedNav = getCollapsedSidebarNav();
  const expandedNavGroups = getExpandedSidebarGroups();
  const isChatWorkspace = shellMode === "chat";
  const sessionControls =
    isChatWorkspace && onSelectSession && onRenameSession && onDeleteSession
      ? {
          onSelectSession,
          onRenameSession,
          onDeleteSession,
        }
      : null;

  const handleNewChat = () => {
    if (onNewChat) {
      onNewChat();
      return;
    }
    router.push("/");
  };

  /* ---- Collapsed state ---- */
  if (collapsed) {
    return (
      <aside className="flex w-[56px] h-screen shrink-0 flex-col items-center bg-[var(--secondary)] py-3 transition-all duration-200">
        <button
          onClick={() => setCollapsed(false)}
          className="mb-4 rounded-md p-1.5 text-[var(--muted-foreground)] transition-colors hover:text-[var(--foreground)]"
          aria-label={t("Expand sidebar")}
        >
          <PanelLeftOpen size={15} />
        </button>

        {isChatWorkspace ? (
          <button
            onClick={handleNewChat}
            className="mb-3 rounded-lg p-2 text-[var(--muted-foreground)] transition-colors hover:bg-[var(--background)]/60 hover:text-[var(--foreground)]"
            aria-label={t("New Chat")}
          >
            <Plus size={16} strokeWidth={2} />
          </button>
        ) : null}

        <nav className="flex flex-col items-center gap-px pt-1">
          {collapsedNav.map((item) => {
            const Icon = resolveNavIcon(item.icon);
            const active = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
            return (
              <div key={item.href} className="flex flex-col items-center">
                <Link
                  href={item.href}
                  title={t(getContestLabel(item.label))}
                  aria-label={t(getContestLabel(item.label))}
                  className={`rounded-lg p-2 transition-colors ${
                    active
                      ? "bg-[var(--background)]/70 text-[var(--foreground)]"
                      : "text-[var(--muted-foreground)] hover:bg-[var(--background)]/50 hover:text-[var(--foreground)]"
                  }`}
                >
                  <Icon size={16} strokeWidth={active ? 1.9 : 1.5} />
                </Link>
                {item.href === "/agents" && <TutorBotRecent collapsed />}
              </div>
            );
          })}
        </nav>

        <div className="flex-1" />

        <div className="flex flex-col items-center gap-px pb-1">
          {SECONDARY_NAV.map((item) => {
            const active = pathname.startsWith(item.href);
            return (
              <Link
                key={item.href}
                href={item.href}
                title={t(item.label)}
                aria-label={t(item.label)}
                className={`rounded-lg p-2 transition-colors ${
                  active
                    ? "bg-[var(--background)]/70 text-[var(--foreground)]"
                    : "text-[var(--muted-foreground)] hover:bg-[var(--background)]/50 hover:text-[var(--foreground)]"
                }`}
              >
                <item.icon size={16} strokeWidth={active ? 1.9 : 1.5} />
              </Link>
            );
          })}
          {footerSlot}
        </div>
      </aside>
    );
  }

  /* ---- Expanded state ---- */
  return (
    <aside className="flex h-screen w-[264px] shrink-0 flex-col bg-[var(--secondary)] transition-all duration-200">
      {/* Header: logo + collapse toggle */}
      <div className="flex h-12 items-center justify-between px-4">
        <Link href="/" className="flex items-center gap-2">
          <Image src="/logo-ver2.png" alt={t("DeepTutor")} width={20} height={20} />
          <span className="text-[15px] font-semibold tracking-tight text-[var(--foreground)]">
            {t("DeepTutor")}
          </span>
        </Link>
        <button
          onClick={() => setCollapsed(true)}
          className="rounded-md p-1 text-[var(--muted-foreground)] transition-colors hover:text-[var(--foreground)]"
          aria-label={t("Collapse sidebar")}
        >
          <PanelLeftClose size={15} />
        </button>
      </div>

      {/* Primary nav */}
      <nav className="px-2 pt-1">
        <div className="space-y-px">
          {expandedNavGroups.map((group, index) => (
            <div key={group.id} className={index > 0 ? "pt-3" : ""}>
              <div className="px-3 pb-1 text-[11px] font-semibold uppercase tracking-[0.12em] text-[var(--muted-foreground)]/80">
                {t(getContestLabel(group.label))}
              </div>
              {group.items.map((item) => {
                const Icon = resolveNavIcon(item.icon);
                const active = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
                const hasBots = item.href === "/agents";
                return (
                  <div key={item.href}>
                    <Link
                      href={item.href}
                      className={`flex items-center gap-2.5 rounded-lg px-3 py-1.5 text-[13.5px] transition-colors ${
                        active
                          ? "bg-[var(--background)]/70 font-medium text-[var(--foreground)]"
                          : "text-[var(--muted-foreground)] hover:bg-[var(--background)]/50 hover:text-[var(--foreground)]"
                      }`}
                    >
                      <Icon size={16} strokeWidth={active ? 1.9 : 1.5} />
                      <span>{t(getContestLabel(item.label))}</span>
                    </Link>
                    {hasBots && <TutorBotRecent />}
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      </nav>

      {sessionControls ? (
        <div className="min-h-0 flex-1 px-2 pb-2 pt-3">
          <div className="flex items-center justify-between px-3 pb-2">
            <div className="text-[11px] font-semibold uppercase tracking-[0.12em] text-[var(--muted-foreground)]/80">
              {t("Chat")}
            </div>
            <button
              onClick={handleNewChat}
              className="rounded-md p-1 text-[var(--muted-foreground)] transition-colors hover:bg-[var(--background)]/60 hover:text-[var(--foreground)]"
              aria-label={t("New Chat")}
            >
              <Plus size={15} strokeWidth={2} />
            </button>
          </div>
          <div className="min-h-0 overflow-y-auto rounded-2xl bg-[var(--background)]/35 p-1">
            <SessionList
              sessions={sessions}
              activeSessionId={activeSessionId}
              loading={loadingSessions}
              onSelect={sessionControls.onSelectSession}
              onRename={sessionControls.onRenameSession}
              onDelete={sessionControls.onDeleteSession}
            />
          </div>
        </div>
      ) : (
        <div className="flex-1" />
      )}

      {/* Secondary nav + footer */}
      <div className="border-t border-[var(--border)]/40 px-2 py-2">
        {SECONDARY_NAV.map((item) => {
          const active = pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-2.5 rounded-lg px-3 py-1.5 text-[13.5px] transition-colors ${
                active
                  ? "bg-[var(--background)]/70 font-medium text-[var(--foreground)]"
                  : "text-[var(--muted-foreground)] hover:bg-[var(--background)]/50 hover:text-[var(--foreground)]"
              }`}
            >
              <item.icon size={16} strokeWidth={active ? 1.9 : 1.5} />
              <span>{t(item.label)}</span>
            </Link>
          );
        })}
        {footerSlot}
      </div>
    </aside>
  );
}
