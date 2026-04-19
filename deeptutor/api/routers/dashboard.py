"""Dashboard API backed by the unified SQLite session store."""

import re
from typing import Any

from fastapi import APIRouter, HTTPException

from deeptutor.services.session import extract_assessment_review, get_sqlite_session_store

router = APIRouter()

_TOPIC_STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "to",
    "of",
    "in",
    "on",
    "for",
    "with",
    "is",
    "are",
    "what",
    "which",
    "solve",
    "find",
    "calculate",
    "determine",
}


def _infer_topic_from_question(question: str, fallback: str = "general") -> str:
    words = re.findall(r"[A-Za-z][A-Za-z0-9'-]{2,}", question.lower())
    filtered = [w for w in words if w not in _TOPIC_STOPWORDS]
    if not filtered:
        return fallback
    return " ".join(filtered[:2])


def _build_assessment_analysis(review: dict[str, Any]) -> dict[str, Any]:
    results = review.get("results", [])
    if not isinstance(results, list):
        results = []

    topic_buckets: dict[str, dict[str, int]] = {}
    for item in results:
        if not isinstance(item, dict):
            continue
        question = str(item.get("question") or "")
        topic = _infer_topic_from_question(question)
        bucket = topic_buckets.setdefault(topic, {"total": 0, "correct": 0, "incorrect": 0})
        bucket["total"] += 1
        if bool(item.get("is_correct")):
            bucket["correct"] += 1
        else:
            bucket["incorrect"] += 1

    performance_by_topic = []
    for topic, counts in sorted(topic_buckets.items(), key=lambda kv: (-kv[1]["incorrect"], kv[0])):
        total = counts["total"]
        accuracy = round((counts["correct"] / total) * 100) if total else 0
        performance_by_topic.append(
            {
                "topic": topic,
                "total_questions": total,
                "correct_count": counts["correct"],
                "incorrect_count": counts["incorrect"],
                "accuracy_percent": accuracy,
            }
        )

    weak_topics = [row["topic"] for row in performance_by_topic if row["incorrect_count"] > 0][:3]
    strong_topics = [row["topic"] for row in performance_by_topic if row["accuracy_percent"] >= 80][:3]

    score_percent = int(review.get("summary", {}).get("score_percent", 0))
    recommendations: list[str] = []
    if weak_topics:
        recommendations.append(
            f"Review these topics first: {', '.join(weak_topics)}."
        )
    if score_percent < 75:
        recommendations.append("Retry a focused quiz on weak topics before moving on.")
    elif score_percent < 90:
        recommendations.append("Practice mixed-difficulty questions to improve consistency.")
    else:
        recommendations.append("You are ready for advanced questions and extension material.")
    if strong_topics:
        recommendations.append(f"Strong areas: {', '.join(strong_topics)}.")

    return {
        "session_id": review.get("session_id"),
        "summary": review.get("summary", {}),
        "performance_by_topic": performance_by_topic,
        "weak_topics": weak_topics,
        "strong_topics": strong_topics,
        "recommendations": recommendations,
    }


def _activity_type(capability: str) -> str:
    if capability == "deep_question":
        return "assessment"
    if capability in {"chat", ""}:
        return "tutoring"
    return capability.replace("deep_", "")


def _session_knowledge_bases(session: dict[str, Any]) -> list[str]:
    preferences = session.get("preferences")
    if not isinstance(preferences, dict):
        return []
    raw_kbs = preferences.get("knowledge_bases", [])
    if not isinstance(raw_kbs, list):
        return []
    return [str(kb).strip() for kb in raw_kbs if str(kb).strip()]


def _activity_from_session(
    session: dict[str, Any],
    assessment_review: dict[str, Any] | None = None,
) -> dict[str, Any]:
    capability = str(session.get("capability") or "chat")
    knowledge_bases = _session_knowledge_bases(session)
    return {
        "id": session.get("session_id"),
        "type": _activity_type(capability),
        "capability": capability,
        "title": session.get("title", "Untitled"),
        "timestamp": session.get("updated_at", session.get("created_at", 0)),
        "summary": (session.get("last_message") or "")[:160],
        "session_ref": f"sessions/{session.get('session_id')}",
        "message_count": session.get("message_count", 0),
        "status": session.get("status", "idle"),
        "active_turn_id": session.get("active_turn_id"),
        "knowledge_bases": knowledge_bases,
        "assessment_summary": assessment_review["summary"] if assessment_review else None,
        "review_ref": (
            f"dashboard/assessments/{session.get('session_id')}" if assessment_review else None
        ),
    }


async def _activity_with_review(
    store,
    session: dict[str, Any],
) -> dict[str, Any]:
    capability = str(session.get("capability") or "chat")
    if capability != "deep_question":
        return _activity_from_session(session)
    detail = await store.get_session_with_messages(str(session.get("session_id") or session.get("id")))
    review = extract_assessment_review(detail) if detail else None
    return _activity_from_session(session, review)


@router.get("/recent")
async def get_recent_activities(limit: int = 50, type: str | None = None):
    store = get_sqlite_session_store()
    sessions = await store.list_sessions(limit=limit, offset=0)
    activities: list[dict[str, Any]] = []

    for session in sessions:
        activity = await _activity_with_review(store, session)
        if type is not None and activity["type"] != type:
            continue
        activities.append(activity)

    return activities[:limit]


@router.get("/overview")
async def get_dashboard_overview(limit: int = 50):
    store = get_sqlite_session_store()
    sessions = await store.list_sessions(limit=limit, offset=0)
    activities = [await _activity_with_review(store, session) for session in sessions]

    knowledge_pack_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    for activity in activities:
        status = str(activity.get("status") or "idle")
        status_counts[status] = status_counts.get(status, 0) + 1
        for kb_name in activity["knowledge_bases"]:
            knowledge_pack_counts[kb_name] = knowledge_pack_counts.get(kb_name, 0) + 1

    return {
        "totals": {
            "total_sessions": len(activities),
            "assessments": sum(1 for activity in activities if activity["type"] == "assessment"),
            "tutoring_sessions": sum(1 for activity in activities if activity["type"] == "tutoring"),
            "running": status_counts.get("running", 0),
            "completed": status_counts.get("completed", 0),
            "failed": status_counts.get("failed", 0),
        },
        "knowledge_packs": [
            {"name": name, "session_count": count}
            for name, count in sorted(
                knowledge_pack_counts.items(),
                key=lambda item: (-item[1], item[0]),
            )
        ],
        "recent_activity": activities[:limit],
    }


@router.get("/{entry_id}")
async def get_activity_entry(entry_id: str):
    store = get_sqlite_session_store()
    session = await store.get_session_with_messages(entry_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Entry not found")

    capability = str(session.get("capability") or "chat")
    review = extract_assessment_review(session) if capability == "deep_question" else None
    return {
        "id": session.get("session_id"),
        "type": _activity_type(capability),
        "capability": capability,
        "title": session.get("title"),
        "timestamp": session.get("updated_at", session.get("created_at")),
        "knowledge_bases": _session_knowledge_bases(session),
        "assessment_summary": review["summary"] if review else None,
        "content": {
            "messages": session.get("messages", []),
            "active_turns": session.get("active_turns", []),
            "status": session.get("status", "idle"),
            "summary": session.get("compressed_summary", ""),
        },
    }


@router.get("/assessment-analysis/{session_id}")
async def get_assessment_analysis(session_id: str):
    store = get_sqlite_session_store()
    session = await store.get_session_with_messages(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Assessment session not found")

    review = extract_assessment_review(session)
    if review is None:
        raise HTTPException(status_code=404, detail="Assessment review data not found")

    return _build_assessment_analysis(review)
