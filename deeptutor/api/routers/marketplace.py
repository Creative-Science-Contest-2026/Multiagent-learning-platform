"""Marketplace API for discovering and browsing teacher-shared Knowledge Packs."""

from fastapi import APIRouter, HTTPException, Query
from deeptutor.knowledge.manager import get_knowledge_manager

router = APIRouter()


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
        manager = get_knowledge_manager()
        
        # Get all knowledge bases with metadata
        all_kbs = await manager.list_knowledge_bases()
        
        # Filter by sharing_status
        if sharing_status:
            all_kbs = [
                kb for kb in all_kbs
                if kb.get("metadata", {}).get("sharing_status") == sharing_status
            ]
        else:
            # Default: show public and team packs
            all_kbs = [
                kb for kb in all_kbs
                if kb.get("metadata", {}).get("sharing_status") in ["public", "team"]
            ]
        
        # Filter by subject
        if subject:
            all_kbs = [
                kb for kb in all_kbs
                if kb.get("metadata", {}).get("subject", "").lower() == subject.lower()
            ]
        
        # Filter by owner
        if owner:
            all_kbs = [
                kb for kb in all_kbs
                if kb.get("metadata", {}).get("owner", "").lower() == owner.lower()
            ]
        
        # Apply pagination
        total = len(all_kbs)
        packs = all_kbs[offset : offset + limit]
        
        # Format response with metadata
        formatted_packs = []
        for kb in packs:
            metadata = kb.get("metadata", {})
            formatted_packs.append({
                "name": kb.get("name"),
                "subject": metadata.get("subject"),
                "grade": metadata.get("grade"),
                "curriculum": metadata.get("curriculum"),
                "learning_objectives": metadata.get("learning_objectives", []),
                "owner": metadata.get("owner"),
                "sharing_status": metadata.get("sharing_status"),
                "session_count": kb.get("session_count", 0),
                "status": kb.get("status", "ready"),
            })
        
        return {
            "total": total,
            "offset": offset,
            "limit": limit,
            "packs": formatted_packs,
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{pack_name}")
async def get_marketplace_pack(pack_name: str):
    """Get detailed information about a specific marketplace pack."""
    try:
        manager = get_knowledge_manager()
        kb = await manager.get_knowledge_base(pack_name)
        
        if not kb:
            raise HTTPException(status_code=404, detail=f"Knowledge pack '{pack_name}' not found")
        
        # Check if pack is shareable (public or team)
        sharing_status = kb.get("metadata", {}).get("sharing_status")
        if not sharing_status or sharing_status not in ["public", "team"]:
            raise HTTPException(
                status_code=403,
                detail=f"Knowledge pack '{pack_name}' is not publicly shared"
            )
        
        metadata = kb.get("metadata", {})
        return {
            "name": kb.get("name"),
            "subject": metadata.get("subject"),
            "grade": metadata.get("grade"),
            "curriculum": metadata.get("curriculum"),
            "learning_objectives": metadata.get("learning_objectives", []),
            "owner": metadata.get("owner"),
            "sharing_status": metadata.get("sharing_status"),
            "session_count": kb.get("session_count", 0),
            "status": kb.get("status", "ready"),
            "statistics": kb.get("statistics", {}),
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
