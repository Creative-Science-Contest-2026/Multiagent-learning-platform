"""
TutorBot management API.
"""

from __future__ import annotations

import json
import logging

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from deeptutor.services.auth.deps import get_current_user
from deeptutor.services.auth.deps import get_current_user_from_websocket
from deeptutor.services.auth.schemas import AuthenticatedUser
from deeptutor.services.tutorbot import get_tutorbot_manager
from deeptutor.services.tutorbot.manager import BotConfig

logger = logging.getLogger(__name__)
router = APIRouter()
require_teacher_or_admin_roles = {"teacher", "admin"}


class CreateBotRequest(BaseModel):
    bot_id: str
    name: str | None = None
    description: str = ""
    persona: str = ""
    channels: dict = {}
    model: str | None = None


class UpdateBotRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    persona: str | None = None
    channels: dict | None = None
    model: str | None = None


class FileUpdateRequest(BaseModel):
    content: str


class SoulCreateRequest(BaseModel):
    id: str
    name: str
    content: str


class SoulUpdateRequest(BaseModel):
    name: str | None = None
    content: str | None = None


def _require_teacher_or_admin(user: AuthenticatedUser) -> None:
    if user.role not in require_teacher_or_admin_roles:
        raise HTTPException(status_code=403, detail="Forbidden")


def _can_access_bot(record: dict[str, object] | None, current_user: AuthenticatedUser) -> bool:
    if current_user.role == "admin":
        return True
    if not record:
        return False
    return str(record.get("owner_user_id") or "").strip() == current_user.id


def _resolve_bot_record(bot_id: str, current_user: AuthenticatedUser) -> dict[str, object] | None:
    manager = get_tutorbot_manager()
    for entry in manager.list_bots():
        if entry.get("bot_id") == bot_id and _can_access_bot(entry, current_user):
            return entry
    return None


# ── Soul template library (must be before /{bot_id} routes) ───

@router.get("/souls")
async def list_souls(current_user: AuthenticatedUser = Depends(get_current_user)):
    _require_teacher_or_admin(current_user)
    return get_tutorbot_manager().list_souls()


@router.post("/souls")
async def create_soul(
    payload: SoulCreateRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    _require_teacher_or_admin(current_user)
    mgr = get_tutorbot_manager()
    if mgr.get_soul(payload.id):
        raise HTTPException(status_code=409, detail=f"Soul '{payload.id}' already exists")
    return mgr.create_soul(payload.id, payload.name, payload.content)


@router.get("/souls/{soul_id}")
async def get_soul(soul_id: str, current_user: AuthenticatedUser = Depends(get_current_user)):
    _require_teacher_or_admin(current_user)
    soul = get_tutorbot_manager().get_soul(soul_id)
    if not soul:
        raise HTTPException(status_code=404, detail="Soul not found")
    return soul


@router.put("/souls/{soul_id}")
async def update_soul(
    soul_id: str,
    payload: SoulUpdateRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    _require_teacher_or_admin(current_user)
    result = get_tutorbot_manager().update_soul(soul_id, payload.name, payload.content)
    if not result:
        raise HTTPException(status_code=404, detail="Soul not found")
    return result


@router.delete("/souls/{soul_id}")
async def delete_soul(soul_id: str, current_user: AuthenticatedUser = Depends(get_current_user)):
    _require_teacher_or_admin(current_user)
    if not get_tutorbot_manager().delete_soul(soul_id):
        raise HTTPException(status_code=404, detail="Soul not found")
    return {"id": soul_id, "deleted": True}


# ── Bot management (static paths before /{bot_id} parameterized routes) ──

@router.get("")
async def list_bots(current_user: AuthenticatedUser = Depends(get_current_user)):
    _require_teacher_or_admin(current_user)
    bots = get_tutorbot_manager().list_bots()
    if current_user.role == "admin":
        return bots
    return [entry for entry in bots if _can_access_bot(entry, current_user)]


@router.get("/recent")
async def recent_bots(
    limit: int = 3,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    """Return the most recently active bots with their last message preview."""
    _require_teacher_or_admin(current_user)
    bots = get_tutorbot_manager().get_recent_active_bots(limit=limit * 4)
    if current_user.role != "admin":
        bots = [entry for entry in bots if _can_access_bot(entry, current_user)]
    return bots[:limit]


@router.post("")
async def create_and_start_bot(
    payload: CreateBotRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    _require_teacher_or_admin(current_user)
    mgr = get_tutorbot_manager()
    config = BotConfig(
        name=payload.name or payload.bot_id,
        description=payload.description,
        persona=payload.persona,
        channels=payload.channels,
        model=payload.model,
        owner_user_id=current_user.id,
        owner_email=current_user.email,
        owner_display_name=current_user.display_name,
    )
    try:
        instance = await mgr.start_bot(payload.bot_id, config)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return instance.to_dict()


@router.get("/{bot_id}")
async def get_bot(bot_id: str, current_user: AuthenticatedUser = Depends(get_current_user)):
    _require_teacher_or_admin(current_user)
    record = _resolve_bot_record(bot_id, current_user)
    if record:
        return record
    raise HTTPException(status_code=404, detail="Bot not found")


@router.delete("/{bot_id}")
async def stop_bot(bot_id: str, current_user: AuthenticatedUser = Depends(get_current_user)):
    _require_teacher_or_admin(current_user)
    if not _resolve_bot_record(bot_id, current_user):
        raise HTTPException(status_code=404, detail="Bot not found or not running")
    stopped = await get_tutorbot_manager().stop_bot(bot_id)
    if not stopped:
        raise HTTPException(status_code=404, detail="Bot not found or not running")
    return {"bot_id": bot_id, "stopped": True}


@router.delete("/{bot_id}/destroy")
async def destroy_bot(bot_id: str, current_user: AuthenticatedUser = Depends(get_current_user)):
    _require_teacher_or_admin(current_user)
    if not _resolve_bot_record(bot_id, current_user):
        raise HTTPException(status_code=404, detail="Bot not found")
    destroyed = await get_tutorbot_manager().destroy_bot(bot_id)
    if not destroyed:
        raise HTTPException(status_code=404, detail="Bot not found")
    return {"bot_id": bot_id, "destroyed": True}


@router.patch("/{bot_id}")
async def update_bot(
    bot_id: str,
    payload: UpdateBotRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    _require_teacher_or_admin(current_user)
    mgr = get_tutorbot_manager()
    if not _resolve_bot_record(bot_id, current_user):
        raise HTTPException(status_code=404, detail="Bot not found")
    instance = mgr.get_bot(bot_id)
    if not instance:
        raise HTTPException(status_code=404, detail="Bot not found")

    if payload.name is not None:
        instance.config.name = payload.name
    if payload.description is not None:
        instance.config.description = payload.description
    if payload.persona is not None:
        instance.config.persona = payload.persona
    if payload.channels is not None:
        instance.config.channels = payload.channels
    if payload.model is not None:
        instance.config.model = payload.model

    mgr._save_bot_config(bot_id, instance.config)
    return instance.to_dict()


# ── Workspace file endpoints ──────────────────────────────────

@router.get("/{bot_id}/files")
async def list_bot_files(bot_id: str, current_user: AuthenticatedUser = Depends(get_current_user)):
    _require_teacher_or_admin(current_user)
    if not _resolve_bot_record(bot_id, current_user):
        raise HTTPException(status_code=404, detail="Bot not found")
    return get_tutorbot_manager().read_all_bot_files(bot_id)


@router.get("/{bot_id}/files/{filename}")
async def read_bot_file(
    bot_id: str,
    filename: str,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    _require_teacher_or_admin(current_user)
    if not _resolve_bot_record(bot_id, current_user):
        raise HTTPException(status_code=404, detail="Bot not found")
    content = get_tutorbot_manager().read_bot_file(bot_id, filename)
    if content is None:
        raise HTTPException(status_code=400, detail=f"Not an editable file: {filename}")
    return {"filename": filename, "content": content}


@router.put("/{bot_id}/files/{filename}")
async def write_bot_file(
    bot_id: str,
    filename: str,
    payload: FileUpdateRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    _require_teacher_or_admin(current_user)
    if not _resolve_bot_record(bot_id, current_user):
        raise HTTPException(status_code=404, detail="Bot not found")
    ok = get_tutorbot_manager().write_bot_file(bot_id, filename, payload.content)
    if not ok:
        raise HTTPException(status_code=400, detail=f"Not an editable file: {filename}")
    return {"filename": filename, "saved": True}


# ── Chat history & WebSocket ──────────────────────────────────

@router.get("/{bot_id}/history")
async def get_bot_history(
    bot_id: str,
    limit: int = 100,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    """Read chat history from the bot's per-bot JSONL session files."""
    _require_teacher_or_admin(current_user)
    if not _resolve_bot_record(bot_id, current_user):
        raise HTTPException(status_code=404, detail="Bot not found")
    return get_tutorbot_manager().get_bot_history(bot_id, limit=limit)


@router.websocket("/{bot_id}/ws")
async def bot_chat_ws(ws: WebSocket, bot_id: str):
    import asyncio

    try:
        current_user = get_current_user_from_websocket(ws)
    except Exception:
        await ws.close(code=4401)
        return
    if current_user.role not in require_teacher_or_admin_roles:
        await ws.close(code=4403)
        return
    if not _resolve_bot_record(bot_id, current_user):
        await ws.close(code=4404, reason="Bot not found")
        return

    mgr = get_tutorbot_manager()
    instance = mgr.get_bot(bot_id)
    if not instance or not instance.running:
        await ws.close(code=4004, reason="Bot not found or not running")
        return

    await ws.accept()
    logger.info("WebSocket connected for bot '%s'", bot_id)

    async def _handle_user_messages():
        while True:
            raw = await ws.receive_text()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                await ws.send_json({"type": "error", "content": "Invalid JSON"})
                continue

            content = data.get("content", "").strip()
            if not content:
                continue

            async def on_progress(text: str) -> None:
                await ws.send_json({"type": "thinking", "content": text})

            try:
                response = await mgr.send_message(
                    bot_id, content, chat_id=data.get("chat_id", "web"),
                    on_progress=on_progress,
                )
                await ws.send_json({"type": "content", "content": response})
                await ws.send_json({"type": "done"})
            except RuntimeError as exc:
                await ws.send_json({"type": "error", "content": str(exc)})
            except Exception:
                logger.exception("Error processing message for bot '%s'", bot_id)
                await ws.send_json({"type": "error", "content": "Internal error"})

    async def _handle_notifications():
        while True:
            content = await instance.notify_queue.get()
            try:
                await ws.send_json({"type": "proactive", "content": content})
            except Exception:
                break

    user_task = asyncio.create_task(_handle_user_messages())
    notify_task = asyncio.create_task(_handle_notifications())
    try:
        done, pending = await asyncio.wait(
            [user_task, notify_task], return_when=asyncio.FIRST_COMPLETED,
        )
        for t in pending:
            t.cancel()
        for t in done:
            if t.exception() and not isinstance(t.exception(), WebSocketDisconnect):
                logger.exception("WebSocket task error for bot '%s'", bot_id, exc_info=t.exception())
    except Exception:
        user_task.cancel()
        notify_task.cancel()
    logger.info("WebSocket closed for bot '%s'", bot_id)
