from __future__ import annotations

import os

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi.responses import RedirectResponse

from deeptutor.services.auth.deps import AUTH_COOKIE_NAME
from deeptutor.services.auth.deps import get_auth_service
from deeptutor.services.auth.deps import get_current_user
from deeptutor.services.auth.google_oauth import build_google_authorize_url
from deeptutor.services.auth.google_oauth import exchange_google_code_for_identity
from deeptutor.services.auth.google_oauth import get_google_oauth_settings
from deeptutor.services.auth.schemas import AuthenticatedUser
from deeptutor.services.auth.schemas import ForgotPasswordRequest
from deeptutor.services.auth.schemas import LoginRequest
from deeptutor.services.auth.schemas import ResetPasswordRequest
from deeptutor.services.auth.schemas import SignupRequest
from deeptutor.services.auth.schemas import VerifyEmailRequest
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


def _debug_token_payload(flow: str, token: str | None) -> dict[str, str]:
    if not token:
        return {}
    if os.getenv("DEEPTUTOR_AUTH_DEBUG_TOKENS", "1").strip().lower() not in {"1", "true", "yes", "on"}:
        return {}
    if flow == "verify-email":
        return {
            "debug_token": token,
            "debug_url": f"/verify-email?token={token}",
        }
    return {
        "debug_token": token,
        "debug_url": f"/reset-password?token={token}",
    }


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


@router.post("/forgot-password")
def forgot_password(
    payload: ForgotPasswordRequest,
    service: AuthService = Depends(get_auth_service),
):
    token = service.request_password_reset(email=payload.email)
    body: dict[str, object] = {"ok": True}
    body.update(_debug_token_payload("reset-password", token))
    return body


@router.post("/reset-password")
def reset_password(
    payload: ResetPasswordRequest,
    service: AuthService = Depends(get_auth_service),
):
    if not service.reset_password(token=payload.token, new_password=payload.password):
        raise HTTPException(status_code=400, detail="Invalid or expired password reset token")
    return {"ok": True}


@router.post("/send-verification")
def send_verification(
    current_user: AuthenticatedUser = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service),
):
    token = service.issue_email_verification(user_id=current_user.id)
    body: dict[str, object] = {"ok": True}
    body.update(_debug_token_payload("verify-email", token))
    return body


@router.post("/verify-email")
def verify_email(
    payload: VerifyEmailRequest,
    service: AuthService = Depends(get_auth_service),
):
    if not service.verify_email(token=payload.token):
        raise HTTPException(status_code=400, detail="Invalid or expired email verification token")
    return {"ok": True}


@router.get("/google/start")
def google_start(role: str = "student"):
    normalized_role = role.strip().lower() or "student"
    if normalized_role not in _PUBLIC_SIGNUP_ROLES:
        raise HTTPException(status_code=400, detail="Unsupported signup role")
    settings = get_google_oauth_settings()
    authorize_url = build_google_authorize_url(settings, state=normalized_role)
    return RedirectResponse(authorize_url)


@router.get("/google/callback")
async def google_callback(
    request: Request,
    response: Response,
    code: str = "",
    state: str = "student",
    service: AuthService = Depends(get_auth_service),
):
    if not code.strip():
        raise HTTPException(status_code=400, detail="Missing Google authorization code")
    role = state.strip().lower() or "student"
    if role not in _PUBLIC_SIGNUP_ROLES:
        role = "student"
    settings = get_google_oauth_settings()
    try:
        identity = await exchange_google_code_for_identity(code.strip(), settings)
    except Exception as exc:  # pragma: no cover - external provider failures are integration-tested later
        raise HTTPException(status_code=502, detail="Google login failed") from exc
    user = service.upsert_google_user(
        email=identity.email,
        display_name=identity.name,
        provider_subject=identity.subject,
        desired_role=role,
    )
    session_secret, _session = service.create_auth_session(
        user_id=user["id"],
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
    )
    redirect = RedirectResponse(url=f"/{user['role']}", status_code=302)
    _set_auth_cookie(redirect, session_secret)
    return redirect
