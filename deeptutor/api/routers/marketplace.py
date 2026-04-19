"""Marketplace API for discovering and browsing teacher-shared Knowledge Packs."""

from datetime import datetime
from pathlib import Path
import shutil

from fastapi import APIRouter, HTTPException, Query

from deeptutor.api.routers.knowledge import get_kb_manager

router = APIRouter()


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
                    "sharing_status": sharing_status,
                    "session_count": info.get("statistics", {}).get("content_lists", 0),
                    "status": info.get("status", "ready"),
                    "statistics": info.get("statistics", {}),
                }
            )
        except Exception:
            continue

    return items


@router.get("/list")
async def list_marketplace_packs(
    sharing_status: str | None = Query(None, description="Filter by sharing_status: public, team, or None for all"),
    subject: str | None = Query(None, description="Filter by subject"),
    owner: str | None = Query(None, description="Filter by owner"),
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
        match = next((kb for kb in _list_marketplace_candidates() if kb.get("name") == pack_name), None)

        if not match:
            raise HTTPException(status_code=404, detail=f"Knowledge pack '{pack_name}' not found")

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
        manager = get_kb_manager()

        source_info = None
        for kb in _list_marketplace_candidates():
            if kb.get("name") == pack_name:
                source_info = kb
                break

        if not source_info:
            raise HTTPException(status_code=404, detail=f"Knowledge pack '{pack_name}' not found")

        source_path = manager.base_dir / pack_name
        if not source_path.exists() or not source_path.is_dir():
            raise HTTPException(status_code=404, detail=f"Knowledge pack directory '{pack_name}' not found")

        imported_name = f"{pack_name}__imported"
        dest_path = manager.base_dir / imported_name

        if dest_path.exists():
            return {
                "success": True,
                "message": "Pack already available",
                "pack": {
                    "name": imported_name,
                    "subject": source_info.get("subject"),
                    "grade": source_info.get("grade"),
                    "owner": source_info.get("owner"),
                    "import_date": datetime.utcnow().isoformat(),
                },
            }

        shutil.copytree(source_path, dest_path)

        import_timestamp = datetime.utcnow().isoformat()

        manager.config = manager._load_config()  # keep manager in sync before updating registry
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
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")
