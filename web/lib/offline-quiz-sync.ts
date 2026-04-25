import type { QuizResultItem } from "@/lib/session-api";

const OFFLINE_QUIZ_RESULTS_KEY = "deeptutor:offline-quiz-results";

export interface PendingQuizResultRecord {
  sessionId: string;
  answers: QuizResultItem[];
  savedAt: string;
}

function canUseStorage(): boolean {
  return typeof window !== "undefined" && typeof window.localStorage !== "undefined";
}

function readQueue(): PendingQuizResultRecord[] {
  if (!canUseStorage()) return [];
  try {
    const raw = window.localStorage.getItem(OFFLINE_QUIZ_RESULTS_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as unknown;
    return Array.isArray(parsed)
      ? parsed.filter((item): item is PendingQuizResultRecord => Boolean(item && typeof item === "object"))
      : [];
  } catch {
    return [];
  }
}

function writeQueue(queue: PendingQuizResultRecord[]): void {
  if (!canUseStorage()) return;
  window.localStorage.setItem(OFFLINE_QUIZ_RESULTS_KEY, JSON.stringify(queue));
}

export function enqueueOfflineQuizResults(record: PendingQuizResultRecord): void {
  const queue = readQueue().filter((item) => item.sessionId !== record.sessionId);
  queue.push(record);
  writeQueue(queue);
}

export function getPendingOfflineQuizResults(): PendingQuizResultRecord[] {
  return readQueue();
}

export function removePendingOfflineQuizResults(sessionId: string): void {
  writeQueue(readQueue().filter((item) => item.sessionId !== sessionId));
}
