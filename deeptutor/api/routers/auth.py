from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response

from deeptutor.services.auth.deps import AUTH_COOKIE_NAME
from deeptutor.services.auth.deps import get_auth_service
from deeptutor.services.auth.deps import get_current_user
from deeptutor.services.auth.schemas import AuthenticatedUser
from deeptutor.services.auth.schemas import LoginRequest
from deeptutor.services.auth.schemas import SignupRequest
from deeptutor.services.auth.service import AuthService

router = APIRouter()

_PUBLIC_SIGNUP_ROLES = {"teacher", "student"}


def _set_auth_cookie(response: Response, session_secret: str) -> None:
    response.set_cookie(
        key=AUTH_COOKIE_NAME,
        value=session_secret,
        httponly=True,
        samesite="lax",
        secure=False,
    )


@router.post("/signup")
def signup(
    payload: SignupRequest,
    request: Request,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    role = payload.role.strip().lower()
    if role == "admin":
        raise HTTPException(status_code=400, detail="Admin signup is not allowed")
    if role not in _PUBLIC_SIGNUP_ROLES:
        raise HTTPException(status_code=400, detail="Unsupported signup role")
    try:
        user = service.create_user(
            email=payload.email,
            display_name=payload.display_name,
            role=role,
            password=payload.password,
        )
    except ValueError as exc:
        if str(exc) == "email_exists":
            raise HTTPException(status_code=409, detail="Email already exists") from exc
        raise
    session_secret, _session = service.create_auth_session(
        user_id=user["id"],
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
    )
    _set_auth_cookie(response, session_secret)
    return {"user": user}


@router.post("/login")
def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    user = service.authenticate_user(email=payload.email, password=payload.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    session_secret, _session = service.create_auth_session(
        user_id=user["id"],
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
    )
    _set_auth_cookie(response, session_secret)
    return {"user": user}


@router.post("/logout")
def logout(request: Request, response: Response, service: AuthService = Depends(get_auth_service)):
    session_secret = str(request.cookies.get(AUTH_COOKIE_NAME, "") or "").strip()
    if session_secret:
        service.revoke_session(session_secret)
    response.delete_cookie(AUTH_COOKIE_NAME)
    return {"ok": True}


@router.get("/me")
def me(current_user: AuthenticatedUser = Depends(get_current_user)):
    return {"user": current_user.model_dump()}
