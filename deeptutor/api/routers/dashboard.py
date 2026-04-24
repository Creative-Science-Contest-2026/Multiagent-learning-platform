"""Dashboard API backed by the unified SQLite session store."""

from datetime import datetime, timezone
from typing import Any

import fitz
from fastapi import APIRouter, HTTPException, Response

from deeptutor.services.assessment import build_assessment_analysis
from deeptutor.services.learning_path import build_suggested_learning_path
from deeptutor.services.session import extract_assessment_review, get_sqlite_session_store

router = APIRouter()


def _activity_type(capability: str) -> str:
    if capability == "deep_question":
        return "assessment"
    if capability in {"chat", ""}:
        return "tutoring"
    return capability.replace("deep_", "")


def _timestamp_to_day(value: float | int | None) -> int | None:
    if not value:
        return None
    timestamp = float(value)
    if timestamp > 10_000_000_000:
        timestamp /= 1000
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).date().toordinal()


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
    activity_type = _activity_type(capability)
    return {
        "id": session.get("session_id"),
        "type": activity_type,
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
        "replay_ref": (
            f"dashboard/sessions/{session.get('session_id')}" if activity_type == "tutoring" else None
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


def _summarize_topic_mastery(
    assessment_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    topic_totals: dict[str, dict[str, int]] = {}

    for activity in assessment_rows:
        for row in build_assessment_analysis(
            {
                "session_id": activity.get("session_id"),
                "summary": activity.get("summary") or {},
                "results": activity.get("assessment_results") or [],
            }
        )["performance_by_topic"]:
            bucket = topic_totals.setdefault(
                row["topic"],
                {"topic": row["topic"], "total_questions": 0, "correct_count": 0, "incorrect_count": 0},
            )
            bucket["total_questions"] += row["total_questions"]
            bucket["correct_count"] += row["correct_count"]
            bucket["incorrect_count"] += row["incorrect_count"]

    topic_rows = []
    for row in topic_totals.values():
        total = row["total_questions"]
        row["accuracy_percent"] = round((row["correct_count"] / total) * 100) if total else 0
        topic_rows.append(row)

    focus_topics = sorted(
        [row for row in topic_rows if row["incorrect_count"] > 0],
        key=lambda row: (-row["incorrect_count"], row["accuracy_percent"], row["topic"]),
    )[:5]
    mastered_topics = sorted(
        [row for row in topic_rows if row["accuracy_percent"] >= 80],
        key=lambda row: (-row["accuracy_percent"], row["topic"]),
    )[:5]
    return focus_topics, mastered_topics


def _build_dashboard_analytics(
    activities: list[dict[str, Any]],
    assessment_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    focus_topics, mastered_topics = _summarize_topic_mastery(assessment_rows)
    unique_knowledge_packs = sorted(
        {
            kb_name
            for activity in activities
            for kb_name in activity.get("knowledge_bases", [])
        }
    )
    average_score_percent = round(
        sum(int(row["summary"]["score_percent"]) for row in assessment_rows) / len(assessment_rows)
    ) if assessment_rows else 0
    ordered_assessments = sorted(assessment_rows, key=lambda row: row["timestamp"])
    latest_score_percent = (
        int(ordered_assessments[-1]["summary"]["score_percent"]) if ordered_assessments else 0
    )
    previous_score_percent = (
        int(ordered_assessments[-2]["summary"]["score_percent"])
        if len(ordered_assessments) > 1
        else latest_score_percent
    )

    return {
        "engagement": {
            "active_days": len(
                {
                    day
                    for activity in activities
                    if (day := _timestamp_to_day(activity.get("timestamp"))) is not None
                }
            ),
            "streak_days": _learning_streak_days(activities),
            "knowledge_packs_used": len(unique_knowledge_packs),
        },
        "assessment_trend": {
            "assessments_completed": len(assessment_rows),
            "average_score_percent": average_score_percent,
            "latest_score_percent": latest_score_percent,
            "score_delta": latest_score_percent - previous_score_percent,
        },
        "learning_signals": {
            "focus_topics": focus_topics,
            "mastered_topics": mastered_topics,
        },
    }


def _learning_streak_days(activities: list[dict[str, Any]]) -> int:
    days = []
    seen_days: set[int] = set()
    for activity in sorted(activities, key=lambda row: row.get("timestamp", 0), reverse=True):
        day = _timestamp_to_day(activity.get("timestamp"))
        if day is None or day in seen_days:
            continue
        seen_days.add(day)
        days.append(day)

    if not days:
        return 0

    streak = 1
    for previous, current in zip(days, days[1:]):
        if previous - current == 1:
            streak += 1
            continue
        break
    return streak


def _matches_dashboard_filters(
    activity: dict[str, Any],
    *,
    type: str | None = None,
    knowledge_base: str | None = None,
    search: str | None = None,
    min_score: int | None = None,
) -> bool:
    if type is not None and activity.get("type") != type:
        return False

    if knowledge_base is not None:
        available = [str(kb).lower() for kb in activity.get("knowledge_bases", [])]
        if knowledge_base.lower() not in available:
            return False

    if search:
        haystack = " ".join(
            [
                str(activity.get("title") or ""),
                str(activity.get("summary") or ""),
                " ".join(str(kb) for kb in activity.get("knowledge_bases", [])),
            ]
        ).lower()
        if search.lower() not in haystack:
            return False

    if min_score is not None:
        summary = activity.get("assessment_summary")
        if not summary or int(summary.get("score_percent", 0)) < min_score:
            return False

    return True


def _build_assessment_export_pdf(
    review: dict[str, Any],
    analysis: dict[str, Any],
) -> bytes:
    document = fitz.open()
    page = document.new_page()

    lines = [
        "Assessment Report",
        "",
        f"Title: {review.get('title') or 'Untitled session'}",
        f"Status: {review.get('status') or 'completed'}",
        f"Score: {review.get('summary', {}).get('score_percent', 0)}%",
        (
            "Knowledge Packs: "
            + ", ".join(review.get("knowledge_bases") or [])
            if review.get("knowledge_bases")
            else "Knowledge Packs: None"
        ),
        "",
        "Recommendations:",
    ]

    recommendations = analysis.get("recommendations") or []
    if recommendations:
        lines.extend(f"- {item}" for item in recommendations)
    else:
        lines.append("- No recommendations recorded")

    lines.extend(["", "Question Breakdown:"])
    for index, result in enumerate(review.get("results") or [], start=1):
        lines.extend(
            [
                f"{index}. {result.get('question') or ''}",
                f"Student Answer: {result.get('user_answer') or '(blank)'}",
                f"Correct Answer: {result.get('correct_answer') or '(not recorded)'}",
                f"Result: {'Correct' if result.get('is_correct') else 'Incorrect'}",
                "",
            ]
        )

    y = 48
    for line in lines:
        if y > 780:
            page = document.new_page()
            y = 48
        page.insert_text((48, y), line, fontsize=11)
        y += 18

    pdf_bytes = document.tobytes()
    document.close()
    return pdf_bytes


@router.get("/recent")
async def get_recent_activities(
    limit: int = 50,
    type: str | None = None,
    knowledge_base: str | None = None,
    search: str | None = None,
    min_score: int | None = None,
):
    store = get_sqlite_session_store()
    sessions = await store.list_sessions(limit=limit, offset=0)
    activities: list[dict[str, Any]] = []

    for session in sessions:
        activity = await _activity_with_review(store, session)
        if not _matches_dashboard_filters(
            activity,
            type=type,
            knowledge_base=knowledge_base,
            search=search,
            min_score=min_score,
        ):
            continue
        activities.append(activity)

    return activities[:limit]


@router.get("/overview")
async def get_dashboard_overview(
    limit: int = 50,
    type: str | None = None,
    knowledge_base: str | None = None,
    search: str | None = None,
    min_score: int | None = None,
):
    store = get_sqlite_session_store()
    sessions = await store.list_sessions(limit=limit, offset=0)
    activities = [
        activity
        for session in sessions
        if _matches_dashboard_filters(
            activity := await _activity_with_review(store, session),
            type=type,
            knowledge_base=knowledge_base,
            search=search,
            min_score=min_score,
        )
    ]

    knowledge_pack_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    for activity in activities:
        status = str(activity.get("status") or "idle")
        status_counts[status] = status_counts.get(status, 0) + 1
        for kb_name in activity["knowledge_bases"]:
            knowledge_pack_counts[kb_name] = knowledge_pack_counts.get(kb_name, 0) + 1

    assessment_rows = [
        {
            "session_id": activity["id"],
            "title": activity["title"],
            "timestamp": activity["timestamp"],
            "knowledge_bases": activity["knowledge_bases"],
            "summary": activity["assessment_summary"],
            "review_ref": activity["review_ref"],
            "assessment_results": activity.get("assessment_summary") and (
                extract_assessment_review(await store.get_session_with_messages(activity["id"])) or {}
            ).get("results", []),
        }
        for activity in activities
        if activity["type"] == "assessment" and activity.get("assessment_summary")
    ]

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
        "analytics": _build_dashboard_analytics(activities, assessment_rows),
        "recent_activity": activities[:limit],
    }


@router.get("/student-progress")
async def get_student_progress(limit: int = 50):
    store = get_sqlite_session_store()
    sessions = await store.list_sessions(limit=limit, offset=0)
    activities = [await _activity_with_review(store, session) for session in sessions]

    assessment_rows = [
        {
            "session_id": activity["id"],
            "title": activity["title"],
            "timestamp": activity["timestamp"],
            "knowledge_bases": activity["knowledge_bases"],
            "summary": activity["assessment_summary"],
            "review_ref": activity["review_ref"],
            "assessment_results": activity.get("assessment_summary") and (
                extract_assessment_review(await store.get_session_with_messages(activity["id"])) or {}
            ).get("results", []),
        }
        for activity in activities
        if activity["type"] == "assessment" and activity.get("assessment_summary")
    ]

    focus_topics, mastered_topics = _summarize_topic_mastery(assessment_rows)
    unique_knowledge_packs = sorted(
        {
            kb_name
            for activity in activities
            for kb_name in activity.get("knowledge_bases", [])
        }
    )
    average_score_percent = round(
        sum(int(row["summary"]["score_percent"]) for row in assessment_rows) / len(assessment_rows)
    ) if assessment_rows else 0

    score_trend = [
        {
            "session_id": row["session_id"],
            "score_percent": int(row["summary"]["score_percent"]),
            "timestamp": row["timestamp"],
        }
        for row in sorted(assessment_rows, key=lambda row: row["timestamp"])
    ]
    recent_assessments = [
        {
            "session_id": row["session_id"],
            "title": row["title"],
            "timestamp": row["timestamp"],
            "score_percent": int(row["summary"]["score_percent"]),
            "correct_count": int(row["summary"]["correct_count"]),
            "total_questions": int(row["summary"]["total_questions"]),
            "knowledge_bases": row["knowledge_bases"],
            "review_ref": row["review_ref"],
        }
        for row in sorted(assessment_rows, key=lambda row: row["timestamp"], reverse=True)[:5]
    ]
    suggested_learning_path = build_suggested_learning_path(
        focus_topics=focus_topics,
        mastered_topics=mastered_topics,
        knowledge_bases=unique_knowledge_packs,
    )

    return {
        "totals": {
            "assessments_completed": len(assessment_rows),
            "tutoring_sessions": sum(1 for activity in activities if activity["type"] == "tutoring"),
            "knowledge_packs_used": len(unique_knowledge_packs),
            "average_score_percent": average_score_percent,
            "streak_days": _learning_streak_days(activities),
        },
        "focus_topics": focus_topics,
        "mastered_topics": mastered_topics,
        "score_trend": score_trend,
        "recent_assessments": recent_assessments,
        "suggested_learning_path": suggested_learning_path,
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

    return build_assessment_analysis(review)


@router.get("/assessment-export/{session_id}")
async def export_assessment_report(session_id: str):
    store = get_sqlite_session_store()
    session = await store.get_session_with_messages(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Assessment session not found")

    review = extract_assessment_review(session)
    if review is None:
        raise HTTPException(status_code=404, detail="Assessment review data not found")

    analysis = build_assessment_analysis(review)
    pdf_bytes = _build_assessment_export_pdf(review, analysis)
    filename = f"{session_id}-assessment-report.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
