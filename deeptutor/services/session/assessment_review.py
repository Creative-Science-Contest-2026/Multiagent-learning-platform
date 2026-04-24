from __future__ import annotations

import re
from typing import Any

QUIZ_PREFIX = "[Quiz Performance]"
QUESTION_RE = re.compile(
    r"^\d+\.\s+(?:\[(?P<question_id>[^\]]*)\]\s+)?Q:\s+(?P<question>.+?)\s+->\s+Answered:\s+(?P<answer>.+?)\s+\((?P<status>Correct|Incorrect)(?:,\s+correct:\s+(?P<correct_answer>.+?))?(?:,\s+time:\s+(?P<duration_seconds>\d+)s)?\)$"
)
SCORE_RE = re.compile(r"^Score:\s+(?P<correct>\d+)/(?P<total>\d+)\s+\((?P<percent>\d+)%\)$")


def _session_knowledge_bases(session: dict[str, Any]) -> list[str]:
    preferences = session.get("preferences")
    if not isinstance(preferences, dict):
        return []
    raw_kbs = preferences.get("knowledge_bases", [])
    if not isinstance(raw_kbs, list):
        return []
    return [str(kb).strip() for kb in raw_kbs if str(kb).strip()]


def extract_assessment_review(session: dict[str, Any]) -> dict[str, Any] | None:
    messages = session.get("messages", [])
    review_message = None
    for message in reversed(messages):
        content = str(message.get("content") or "")
        if content.startswith(QUIZ_PREFIX):
            review_message = content
            break
    if review_message is None:
        return None

    results: list[dict[str, Any]] = []
    score_percent = 0
    correct_count = 0
    total_questions = 0

    for raw_line in review_message.splitlines()[1:]:
        line = raw_line.strip()
        if not line:
            continue
        score_match = SCORE_RE.match(line)
        if score_match:
            correct_count = int(score_match.group("correct"))
            total_questions = int(score_match.group("total"))
            score_percent = int(score_match.group("percent"))
            continue
        question_match = QUESTION_RE.match(line)
        if not question_match:
            continue
        results.append(
            {
                "question_id": (question_match.group("question_id") or "").strip(),
                "question": question_match.group("question").strip(),
                "user_answer": question_match.group("answer").strip(),
                "correct_answer": (question_match.group("correct_answer") or "").strip(),
                "is_correct": question_match.group("status") == "Correct",
                "duration_seconds": (
                    int(question_match.group("duration_seconds"))
                    if question_match.group("duration_seconds")
                    else None
                ),
            }
        )

    if total_questions == 0:
        total_questions = len(results)
        correct_count = sum(1 for item in results if item["is_correct"])
        score_percent = round((correct_count / total_questions) * 100) if total_questions else 0

    incorrect_count = max(total_questions - correct_count, 0)
    timed_results = [item["duration_seconds"] for item in results if item["duration_seconds"] is not None]
    summary = {
        "total_questions": total_questions,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "score_percent": score_percent,
    }
    if timed_results:
        estimated_time_spent = sum(timed_results)
        summary["estimated_time_spent"] = estimated_time_spent
        summary["average_time_per_question"] = round(estimated_time_spent / len(timed_results))

    return {
        "session_id": session.get("session_id") or session.get("id"),
        "title": session.get("title") or "Untitled session",
        "timestamp": session.get("updated_at", session.get("created_at", 0)),
        "status": session.get("status", "idle"),
        "knowledge_bases": _session_knowledge_bases(session),
        "summary": summary,
        "results": results,
    }
