from __future__ import annotations

from collections.abc import Callable

from fastapi import HTTPException
from fastapi import Request

from deeptutor.services.auth.schemas import AuthenticatedUser
from deeptutor.services.auth.service import AuthService


AUTH_COOKIE_NAME = "deeptutor_session"


def get_auth_service() -> AuthService:
    return AuthService()


def get_current_user(request: Request) -> AuthenticatedUser:
    session_secret = str(request.cookies.get(AUTH_COOKIE_NAME, "") or "").strip()
    if not session_secret:
        raise HTTPException(status_code=401, detail="Authentication required")
    user = get_auth_service().get_user_for_session_secret(session_secret)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid session")
    return AuthenticatedUser(**user)


def require_roles(*roles: str) -> Callable[[Request], AuthenticatedUser]:
    allowed = set(roles)

    def _resolver(request: Request) -> AuthenticatedUser:
        user = get_current_user(request)
        if user.role not in allowed:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user

    return _resolver
