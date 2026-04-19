"""Dashboard API backed by the unified SQLite session store."""

from typing import Any

from fastapi import APIRouter, HTTPException

from deeptutor.services.session import extract_assessment_review, get_sqlite_session_store

router = APIRouter()


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
