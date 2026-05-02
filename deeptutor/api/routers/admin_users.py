from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from deeptutor.services.auth.deps import require_roles
from deeptutor.services.auth.schemas import AdminCreateUserRequest
from deeptutor.services.auth.schemas import AuthenticatedUser
from deeptutor.services.auth.service import AuthService

router = APIRouter()
require_admin = require_roles("admin")


def get_auth_service() -> AuthService:
    return AuthService()


@router.get("/users")
def list_users(
    current_user: AuthenticatedUser = Depends(require_admin),
    service: AuthService = Depends(get_auth_service),
):
    return {"users": service.list_users(), "viewer": current_user.model_dump()}


@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(
    payload: AdminCreateUserRequest,
    current_user: AuthenticatedUser = Depends(require_admin),
    service: AuthService = Depends(get_auth_service),
):
    try:
        user = service.create_user(
            email=payload.email,
            display_name=payload.display_name,
            role=payload.role,
            password=payload.password,
        )
    except ValueError as exc:
        if str(exc) == "email_exists":
            raise HTTPException(status_code=409, detail="Email already exists") from exc
        raise
    return {"user": user, "viewer": current_user.model_dump()}
