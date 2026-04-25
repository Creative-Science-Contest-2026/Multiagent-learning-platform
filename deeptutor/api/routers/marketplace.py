"""Marketplace API for discovering and browsing teacher-shared Knowledge Packs."""

from datetime import datetime
from pathlib import Path
import shutil
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from deeptutor.api.routers.knowledge import get_kb_manager

router = APIRouter()


class MarketplaceReviewRequest(BaseModel):
    reviewer: str = Field(min_length=1, max_length=80)
    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(default=None, max_length=400)


class MarketplaceBatchImportRequest(BaseModel):
    pack_names: list[str] = Field(min_length=1, max_length=20)


def _pack_reviews(source_cfg: dict[str, Any]) -> list[dict[str, Any]]:
    raw_reviews = source_cfg.get("marketplace_reviews", [])
    if not isinstance(raw_reviews, list):
        return []
    reviews = [review for review in raw_reviews if isinstance(review, dict)]
    return sorted(
        reviews,
        key=lambda review: str(review.get("created_at") or ""),
        reverse=True,
    )


def _rating_summary(source_cfg: dict[str, Any]) -> dict[str, float | int]:
    reviews = _pack_reviews(source_cfg)
    if not reviews:
        return {"average_rating": 0.0, "review_count": 0}
    average = round(sum(int(review.get("rating") or 0) for review in reviews) / len(reviews), 1)
    return {"average_rating": average, "review_count": len(reviews)}


def _list_marketplace_candidates() -> list[dict]:
    """Return shareable KB entries formatted for marketplace responses."""
    manager = get_kb_manager()
    kb_names = manager.list_knowledge_bases()
    items: list[dict] = []

    for name in kb_names:
        try:
            info = manager.get_info(name)
            metadata = info.get("metadata") or {}
            sharing_status = metadata.get("sharing_status")
            source_cfg = manager.config.get("knowledge_bases", {}).get(name, {})

            if sharing_status not in {"public", "team"}:
                continue

            items.append(
                {
                    "name": info.get("name", name),
                    "subject": metadata.get("subject"),
                    "grade": metadata.get("grade"),
                    "curriculum": metadata.get("curriculum"),
                    "learning_objectives": metadata.get("learning_objectives", []),
                    "owner": metadata.get("owner"),
                    "description": source_cfg.get("description"),
                    "sharing_status": sharing_status,
                    "session_count": info.get("statistics", {}).get("content_lists", 0),
                    "status": info.get("status", "ready"),
                    "statistics": info.get("statistics", {}),
                    "created_at": source_cfg.get("created_at"),
                    "updated_at": source_cfg.get("updated_at"),
                    "rating_summary": _rating_summary(source_cfg),
                }
            )
        except Exception:
            continue

    return items


def _matches_marketplace_search(pack: dict[str, Any], search: str | None) -> bool:
    needle = str(search or "").strip().lower()
    if not needle:
        return True

    haystack_parts = [
        str(pack.get("name") or ""),
        str(pack.get("subject") or ""),
        str(pack.get("grade") or ""),
        str(pack.get("curriculum") or ""),
        str(pack.get("owner") or ""),
        str(pack.get("description") or ""),
        " ".join(str(item or "") for item in pack.get("learning_objectives") or []),
    ]
    haystack = " ".join(part for part in haystack_parts if part).lower()
    return needle in haystack


def _sort_marketplace_candidates(items: list[dict], sort_by: str | None) -> list[dict]:
    if sort_by == "popularity":
        return sorted(
            items,
            key=lambda kb: (
                -(kb.get("rating_summary", {}).get("review_count") or 0),
                -(kb.get("session_count") or 0),
                str(kb.get("name") or ""),
            ),
        )

    if sort_by == "rating":
        return sorted(
            items,
            key=lambda kb: (
                -(kb.get("rating_summary", {}).get("average_rating") or 0.0),
                -(kb.get("rating_summary", {}).get("review_count") or 0),
                str(kb.get("name") or ""),
            ),
        )

    if sort_by == "most_objectives":
        return sorted(
            items,
            key=lambda kb: (
                -len(kb.get("learning_objectives") or []),
                str(kb.get("name") or ""),
            ),
        )

    if sort_by == "recent":
        return sorted(
            items,
            key=lambda kb: (
                str(kb.get("updated_at") or kb.get("created_at") or ""),
                str(kb.get("name") or ""),
            ),
            reverse=True,
        )

    return items


def _get_marketplace_match(pack_name: str) -> dict:
    match = next((kb for kb in _list_marketplace_candidates() if kb.get("name") == pack_name), None)
    if not match:
        raise HTTPException(status_code=404, detail=f"Knowledge pack '{pack_name}' not found")
    return match


def _preview_document_summary(pack_dir: Path) -> tuple[int, list[str]]:
    raw_dir = pack_dir / "raw"
    if not raw_dir.exists() or not raw_dir.is_dir():
        return 0, []

    documents = sorted(
        path.relative_to(raw_dir).as_posix()
        for path in raw_dir.rglob("*")
        if path.is_file()
    )
    return len(documents), documents[:3]


def _import_marketplace_pack_impl(pack_name: str) -> dict[str, Any]:
    manager = get_kb_manager()

    source_info = next(
        (kb for kb in _list_marketplace_candidates() if kb.get("name") == pack_name),
        None,
    )
    if not source_info:
        raise HTTPException(status_code=404, detail=f"Knowledge pack '{pack_name}' not found")

    source_path = manager.base_dir / pack_name
    if not source_path.exists() or not source_path.is_dir():
        raise HTTPException(status_code=404, detail=f"Knowledge pack directory '{pack_name}' not found")

    imported_name = f"{pack_name}__imported"
    dest_path = manager.base_dir / imported_name
    import_timestamp = datetime.utcnow().isoformat()

    if dest_path.exists():
        return {
            "success": True,
            "message": "Pack already available",
            "pack": {
                "name": imported_name,
                "subject": source_info.get("subject"),
                "grade": source_info.get("grade"),
                "owner": source_info.get("owner"),
                "import_date": import_timestamp,
                "session_count": source_info.get("session_count", 0),
            },
        }

    shutil.copytree(source_path, dest_path)

    manager.config = manager._load_config()
    source_cfg = manager.config.get("knowledge_bases", {}).get(pack_name, {})
    imported_cfg = dict(source_cfg)
    imported_cfg["path"] = imported_name
    imported_cfg["description"] = source_cfg.get("description") or f"Imported from {pack_name}"
    imported_cfg["owner"] = source_cfg.get("owner") or source_info.get("owner")
    imported_cfg["sharing_status"] = "private"
    imported_cfg["updated_at"] = import_timestamp
    imported_cfg["created_at"] = source_cfg.get("created_at") or import_timestamp
    imported_cfg["imported_from"] = pack_name
    imported_cfg["import_date"] = import_timestamp

    if "knowledge_bases" not in manager.config:
        manager.config["knowledge_bases"] = {}
    manager.config["knowledge_bases"][imported_name] = imported_cfg
    manager._save_config()

    return {
        "success": True,
        "message": f"Knowledge pack '{pack_name}' imported successfully as '{imported_name}'",
        "pack": {
            "name": imported_name,
            "subject": source_info.get("subject"),
            "grade": source_info.get("grade"),
            "owner": source_info.get("owner"),
            "import_date": import_timestamp,
            "session_count": source_info.get("session_count", 0),
        },
    }


@router.get("/list")
async def list_marketplace_packs(
    sharing_status: str | None = Query(None, description="Filter by sharing_status: public, team, or None for all"),
    subject: str | None = Query(None, description="Filter by subject"),
    owner: str | None = Query(None, description="Filter by owner"),
    search: str | None = Query(None, description="Case-insensitive metadata search"),
    sort_by: str | None = Query(
        None,
        description="Sort packs by popularity, recent, rating, or most_objectives",
    ),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    """
    List marketplace knowledge packs (public or team sharing status).
    
    Returns knowledge packs with metadata, session counts, and owner info.
    """
    try:
        all_kbs = _list_marketplace_candidates()

        if sharing_status:
            all_kbs = [kb for kb in all_kbs if kb.get("sharing_status") == sharing_status]

        if subject:
            needle = subject.lower()
            all_kbs = [
                kb
                for kb in all_kbs
                if (kb.get("subject") or "").lower() == needle
            ]

        if owner:
            needle = owner.lower()
            all_kbs = [
                kb
                for kb in all_kbs
                if (kb.get("owner") or "").lower() == needle
            ]

        if search:
            all_kbs = [kb for kb in all_kbs if _matches_marketplace_search(kb, search)]

        all_kbs = _sort_marketplace_candidates(all_kbs, sort_by)

        total = len(all_kbs)
        packs = all_kbs[offset : offset + limit]

        return {
            "total": total,
            "offset": offset,
            "limit": limit,
            "packs": packs,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{pack_name}")
async def get_marketplace_pack(pack_name: str):
    """Get detailed information about a specific marketplace pack."""
    try:
        manager = get_kb_manager()
        match = _get_marketplace_match(pack_name)
        source_cfg = manager.config.get("knowledge_bases", {}).get(pack_name, {})

        return {
            "name": match.get("name"),
            "subject": match.get("subject"),
            "grade": match.get("grade"),
            "curriculum": match.get("curriculum"),
            "learning_objectives": match.get("learning_objectives", []),
            "owner": match.get("owner"),
            "sharing_status": match.get("sharing_status"),
            "session_count": match.get("session_count", 0),
            "status": match.get("status", "ready"),
            "statistics": match.get("statistics", {}),
            "rating_summary": _rating_summary(source_cfg),
            "recent_reviews": _pack_reviews(source_cfg)[:5],
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{pack_name}/preview")
async def preview_marketplace_pack(pack_name: str):
    """Return a compact preview payload for a marketplace knowledge pack."""
    try:
        manager = get_kb_manager()
        match = _get_marketplace_match(pack_name)
        pack_dir = manager.base_dir / pack_name
        if not pack_dir.exists() or not pack_dir.is_dir():
            raise HTTPException(status_code=404, detail=f"Knowledge pack directory '{pack_name}' not found")

        source_cfg = manager.config.get("knowledge_bases", {}).get(pack_name, {})
        document_count, sample_documents = _preview_document_summary(pack_dir)

        return {
            "name": match.get("name"),
            "description": source_cfg.get("description"),
            "subject": match.get("subject"),
            "grade": match.get("grade"),
            "curriculum": match.get("curriculum"),
            "learning_objectives": match.get("learning_objectives", []),
            "owner": match.get("owner"),
            "sharing_status": match.get("sharing_status"),
            "session_count": match.get("session_count", 0),
            "document_count": document_count,
            "sample_documents": sample_documents,
            "rating_summary": _rating_summary(source_cfg),
            "recent_reviews": _pack_reviews(source_cfg)[:5],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{pack_name}/reviews")
async def submit_marketplace_review(pack_name: str, payload: MarketplaceReviewRequest):
    try:
        manager = get_kb_manager()
        _get_marketplace_match(pack_name)

        source_cfg = manager.config.get("knowledge_bases", {}).get(pack_name)
        if not isinstance(source_cfg, dict):
            raise HTTPException(status_code=404, detail=f"Knowledge pack '{pack_name}' not found")

        review = {
            "reviewer": payload.reviewer.strip(),
            "rating": payload.rating,
            "comment": (payload.comment or "").strip(),
            "created_at": datetime.utcnow().isoformat(),
        }
        reviews = _pack_reviews(source_cfg)
        reviews.insert(0, review)
        source_cfg["marketplace_reviews"] = reviews[:50]
        source_cfg["updated_at"] = datetime.utcnow().isoformat()
        manager._save_config()

        return {
            "success": True,
            "review": review,
            "rating_summary": _rating_summary(source_cfg),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import/{pack_name}")
async def import_marketplace_pack(pack_name: str):
    """
    Import a marketplace knowledge pack to user's workspace.
    
    Copies the pack from the marketplace directory to the user's knowledge_bases.
    Updates metadata with import_date and imported_from fields.
    """
    try:
        return _import_marketplace_pack_impl(pack_name)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


@router.post("/import-batch")
async def import_marketplace_packs_batch(payload: MarketplaceBatchImportRequest):
    results: list[dict[str, Any]] = []

    for pack_name in payload.pack_names:
        normalized_name = pack_name.strip()
        if not normalized_name:
            continue
        try:
            result = _import_marketplace_pack_impl(normalized_name)
            results.append(
                {
                    "source_pack": normalized_name,
                    **result,
                }
            )
        except HTTPException as exc:
            results.append(
                {
                    "source_pack": normalized_name,
                    "success": False,
                    "message": str(exc.detail),
                    "pack": None,
                }
            )

    imported = sum(1 for row in results if row.get("success"))
    return {
        "success": imported == len(results),
        "requested": len(payload.pack_names),
        "imported": imported,
        "results": results,
    }
