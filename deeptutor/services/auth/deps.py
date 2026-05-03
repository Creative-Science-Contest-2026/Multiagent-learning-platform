from __future__ import annotations

from collections.abc import Callable

from fastapi import HTTPException
from fastapi import Request
from fastapi import WebSocket

from deeptutor.services.auth.schemas import AuthenticatedUser
from deeptutor.services.auth.service import AuthService


AUTH_COOKIE_NAME = "deeptutor_session"


def get_auth_service() -> AuthService:
    return AuthService()


def _resolve_user(session_secret: str) -> AuthenticatedUser:
    cleaned_secret = str(session_secret or "").strip()
    if not cleaned_secret:
        raise HTTPException(status_code=401, detail="Authentication required")
    user = get_auth_service().get_user_for_session_secret(cleaned_secret)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid session")
    return AuthenticatedUser(**user)


def get_current_user(request: Request) -> AuthenticatedUser:
    return _resolve_user(str(request.cookies.get(AUTH_COOKIE_NAME, "") or ""))


def get_current_user_from_websocket(websocket: WebSocket) -> AuthenticatedUser:
    return _resolve_user(str(websocket.cookies.get(AUTH_COOKIE_NAME, "") or ""))


def require_roles(*roles: str) -> Callable[[Request], AuthenticatedUser]:
    allowed = set(roles)

    def _resolver(request: Request) -> AuthenticatedUser:
        user = get_current_user(request)
        if user.role not in allowed:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user

    return _resolver


def require_roles_websocket(*roles: str) -> Callable[[WebSocket], AuthenticatedUser]:
    allowed = set(roles)

    def _resolver(websocket: WebSocket) -> AuthenticatedUser:
        user = get_current_user_from_websocket(websocket)
        if user.role not in allowed:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user

    return _resolver


def owner_scope_for_user(user: AuthenticatedUser) -> str | None:
    if user.role == "admin":
        return None
    return user.id
