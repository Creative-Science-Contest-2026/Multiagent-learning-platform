from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends

from deeptutor.services.auth.deps import require_roles
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
