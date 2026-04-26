from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

from deeptutor.services.agent_spec import get_agent_spec_service

router = APIRouter()


class IdentityPayload(BaseModel):
    agent_name: str = ""
    subject: str = ""
    grade_band: str = ""
    tone: str = ""
    primary_language: str = ""
    persona_summary: str = ""


class SoulPayload(BaseModel):
    teaching_philosophy: str = ""
    when_student_wrong: str = ""
    when_student_stuck: str = ""
    encouragement_style: str = ""


class RulesPayload(BaseModel):
    do_not_solve_directly: str = "yes"
    max_session_minutes: str = ""
    hint_policy: str = ""
    escalation_rule: str = ""
    guardrails: str = ""


class StructuredPayload(BaseModel):
    identity: IdentityPayload = Field(default_factory=IdentityPayload)
    soul: SoulPayload = Field(default_factory=SoulPayload)
    rules: RulesPayload = Field(default_factory=RulesPayload)


class AgentSpecUpsertRequest(BaseModel):
    agent_id: str
    display_name: str
    description: str = ""
    structured: StructuredPayload = Field(default_factory=StructuredPayload)
    files: dict[str, str] = Field(default_factory=dict)


@router.get("")
async def list_agent_specs():
    return {"items": get_agent_spec_service().list_packs()}


@router.post("")
async def create_agent_spec(payload: AgentSpecUpsertRequest):
    service = get_agent_spec_service()
    try:
        return service.create_pack(
            agent_id=payload.agent_id,
            display_name=payload.display_name,
            description=payload.description,
            structured=payload.structured.model_dump(),
            files=payload.files,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{agent_id}")
async def get_agent_spec(agent_id: str):
    service = get_agent_spec_service()
    try:
        return service.get_pack(agent_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Agent spec not found") from exc


@router.put("/{agent_id}")
async def update_agent_spec(agent_id: str, payload: AgentSpecUpsertRequest):
    service = get_agent_spec_service()
    try:
        return service.save_pack(
            agent_id=agent_id,
            display_name=payload.display_name,
            description=payload.description,
            structured=payload.structured.model_dump(),
            files=payload.files,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Agent spec not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{agent_id}/export")
async def export_agent_spec(agent_id: str):
    service = get_agent_spec_service()
    try:
        content = service.export_pack_archive(agent_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Agent spec not found") from exc
    return Response(
        content=content,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{agent_id}-spec-pack.zip"'},
    )
