"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { useTranslation } from "react-i18next";
import { SidebarShell } from "@/components/sidebar/SidebarShell";
import { useUnifiedChat } from "@/context/UnifiedChatContext";
import {
  deleteSession,
  listSessions,
  updateSessionTitle,
  type SessionSummary,
} from "@/lib/session-api";

export default function WorkspaceSidebar() {
  const { t } = useTranslation();
  const pathname = usePathname();
  const router = useRouter();
  const { newSession, loadSession, selectedSessionId, sessionStatuses, sidebarRefreshToken } =
    useUnifiedChat();
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [loadingSessions, setLoadingSessions] = useState(false);
  const hasLoadedSessionsRef = useRef(false);
  const shellMode = pathname.startsWith("/playground") ? "chat" : "business";
  const shouldShowChatHistory = shellMode === "chat";

  const refreshSessions = useCallback(async () => {
    if (!hasLoadedSessionsRef.current) {
      setLoadingSessions(true);
    }
    try {
      setSessions(await listSessions(50, 0, { force: true }));
      hasLoadedSessionsRef.current = true;
    } catch (error) {
      console.error("Failed to load sessions", error);
    } finally {
      setLoadingSessions(false);
    }
  }, []);

  useEffect(() => {
    if (!shouldShowChatHistory) {
      setLoadingSessions(false);
      return;
    }
    void refreshSessions();
  }, [refreshSessions, shouldShowChatHistory, sidebarRefreshToken]);

  const orderedSessions = sessions
    .map((session, index) => {
      const runtime = sessionStatuses[session.session_id];
      return {
        index,
        session: runtime
          ? {
              ...session,
              status: runtime.status,
              active_turn_id: runtime.activeTurnId || session.active_turn_id,
            }
          : session,
      };
    })
    .sort((a, b) => {
      const aPriority = a.session.status === "running" ? 0 : 1;
      const bPriority = b.session.status === "running" ? 0 : 1;
      if (aPriority !== bPriority) return aPriority - bPriority;
      return a.index - b.index;
    })
    .map(({ session }) => session);

  const handleNewChat = () => {
    newSession();
    if (pathname !== "/playground") router.push("/playground");
  };

  const handleSelectSession = useCallback(
    async (sessionId: string) => {
      await loadSession(sessionId);
      if (pathname !== "/playground") router.push("/playground");
    },
    [loadSession, pathname, router],
  );

  const handleRenameSession = useCallback(async (sessionId: string, title: string) => {
    const updated = await updateSessionTitle(sessionId, title);
    setSessions((prev) =>
      prev.map((session) =>
        session.session_id === sessionId
          ? { ...session, title: updated.title, updated_at: updated.updated_at }
          : session,
      ),
    );
  }, []);

  const handleDeleteSession = useCallback(
    async (sessionId: string) => {
      if (!window.confirm(t("Delete this chat history?"))) return;
      await deleteSession(sessionId);
      setSessions((prev) => prev.filter((session) => session.session_id !== sessionId));
      if (selectedSessionId === sessionId) {
        newSession();
        if (pathname !== "/playground") router.push("/playground");
      }
    },
    [newSession, pathname, router, selectedSessionId, t],
  );

  return (
    <SidebarShell
      shellMode={shellMode}
      sessions={shouldShowChatHistory ? orderedSessions : []}
      activeSessionId={selectedSessionId}
      loadingSessions={loadingSessions}
      onNewChat={shouldShowChatHistory ? handleNewChat : undefined}
      onSelectSession={shouldShowChatHistory ? handleSelectSession : undefined}
      onRenameSession={shouldShowChatHistory ? handleRenameSession : undefined}
      onDeleteSession={shouldShowChatHistory ? handleDeleteSession : undefined}
    />
  );
}
