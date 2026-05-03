from __future__ import annotations

import json
import os
from logging import getLogger
from urllib.parse import urlencode

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
from deeptutor.services.auth.mailer import AuthEmailDeliverySettings
from deeptutor.services.auth.mailer import AuthEmailDeliveryConfigError
from deeptutor.services.auth.mailer import AuthEmailDeliveryTransportError
from deeptutor.services.auth.mailer import build_password_reset_email
from deeptutor.services.auth.mailer import build_verification_email
from deeptutor.services.auth.mailer import deliver_auth_email
from deeptutor.services.auth.schemas import AuthenticatedUser
from deeptutor.services.auth.schemas import ForgotPasswordRequest
from deeptutor.services.auth.schemas import LoginRequest
from deeptutor.services.auth.schemas import ResetPasswordRequest
from deeptutor.services.auth.schemas import SignupRequest
from deeptutor.services.auth.schemas import VerifyEmailRequest
from deeptutor.services.auth.service import AuthService
from deeptutor.services.auth.session_tokens import mint_session_secret

router = APIRouter()
logger = getLogger(__name__)

_PUBLIC_SIGNUP_ROLES = {"teacher", "student"}
_GOOGLE_STATE_COOKIE_NAME = "deeptutor_google_oauth_state"
_GOOGLE_STATE_COOKIE_MAX_AGE_SECONDS = 10 * 60


def _bool_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _cookie_secure() -> bool:
    return _bool_env("DEEPTUTOR_AUTH_COOKIE_SECURE", default=False)


def _cookie_samesite() -> str:
    value = os.getenv("DEEPTUTOR_AUTH_COOKIE_SAMESITE", "lax").strip().lower()
    if value not in {"lax", "strict", "none"}:
        return "lax"
    return value


def _cookie_max_age_seconds() -> int:
    raw = os.getenv("DEEPTUTOR_AUTH_COOKIE_MAX_AGE_SECONDS", str(14 * 24 * 60 * 60)).strip()
    try:
        value = int(raw)
    except ValueError:
        return 14 * 24 * 60 * 60
    return value if value > 0 else 14 * 24 * 60 * 60


def _set_auth_cookie(response: Response, session_secret: str) -> None:
    response.set_cookie(
        key=AUTH_COOKIE_NAME,
        value=session_secret,
        httponly=True,
        samesite=_cookie_samesite(),
        secure=_cookie_secure(),
        max_age=_cookie_max_age_seconds(),
    )


def _debug_tokens_enabled() -> bool:
    return os.getenv("DEEPTUTOR_AUTH_DEBUG_TOKENS", "1").strip().lower() in {"1", "true", "yes", "on"}


def _public_app_url(request: Request) -> str:
    configured = os.getenv("DEEPTUTOR_PUBLIC_APP_URL", "").strip().rstrip("/")
    if configured:
        return configured
    return str(request.base_url).rstrip("/")


def _build_public_auth_url(request: Request, path: str, token: str) -> str:
    base_url = _public_app_url(request)
    query = urlencode({"token": token})
    return f"{base_url}{path}?{query}"


def _normalize_next_path(candidate: object, *, role: str) -> str | None:
    next_path = str(candidate or "").strip()
    if not next_path.startswith("/") or next_path.startswith("//"):
        return None
    if role == "student" and not next_path.startswith("/student"):
        return None
    return next_path


def _post_auth_redirect(role: str, next_path: object = "") -> str:
    normalized = _normalize_next_path(next_path, role=role)
    if normalized:
        return normalized
    return f"/{role}"


def _encode_google_state(role: str, next_path: str = "", nonce: str = "") -> str:
    payload: dict[str, str] = {"role": role}
    normalized = _normalize_next_path(next_path, role=role)
    if normalized:
        payload["next"] = normalized
    if nonce.strip():
        payload["nonce"] = nonce.strip()
    return json.dumps(payload, separators=(",", ":"))


def _decode_google_state(raw_state: str) -> tuple[str, str | None, str | None]:
    state = raw_state.strip()
    if not state:
        return "student", None, None
    try:
        payload = json.loads(state)
    except json.JSONDecodeError:
        role = state.lower()
        return (role if role in _PUBLIC_SIGNUP_ROLES else "student"), None, None
    role = str(payload.get("role", "student")).strip().lower()
    if role not in _PUBLIC_SIGNUP_ROLES:
        role = "student"
    nonce = str(payload.get("nonce", "") or "").strip() or None
    return role, _normalize_next_path(payload.get("next"), role=role), nonce


def _set_google_state_cookie(response: Response, nonce: str) -> None:
    response.set_cookie(
        key=_GOOGLE_STATE_COOKIE_NAME,
        value=nonce,
        httponly=True,
        samesite="lax",
        secure=_cookie_secure(),
        max_age=_GOOGLE_STATE_COOKIE_MAX_AGE_SECONDS,
    )


def _clear_google_state_cookie(response: Response) -> None:
    response.delete_cookie(_GOOGLE_STATE_COOKIE_NAME)


def _debug_token_payload(flow: str, token: str | None) -> dict[str, str]:
    if not token:
        return {}
    if not _debug_tokens_enabled():
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


def _deliver_password_reset_email(request: Request, reset_info: dict[str, str] | None) -> None:
    if reset_info is None:
        return
    settings = AuthEmailDeliverySettings.from_env()
    message = build_password_reset_email(
        to_email=reset_info["email"],
        display_name=reset_info["display_name"],
        reset_url=_build_public_auth_url(request, "/reset-password", reset_info["token"]),
        from_address=settings.from_address,
        from_name=settings.from_name,
        reply_to_address=settings.reply_to_address,
        reply_to_name=settings.reply_to_name,
    )
    try:
        result = deliver_auth_email(settings, message)
    except (AuthEmailDeliveryConfigError, AuthEmailDeliveryTransportError):
        logger.exception("Password reset email delivery failed")
        return
    if result.status != "sent":
        logger.warning(
            "Password reset email was not sent",
            extra={
                "delivery_status": result.status,
                "delivery_transport": result.transport,
                "delivery_detail": result.detail,
            },
        )


def _deliver_verification_email(request: Request, verification_info: dict[str, str] | None) -> None:
    if verification_info is None:
        return
    settings = AuthEmailDeliverySettings.from_env()
    message = build_verification_email(
        to_email=verification_info["email"],
        display_name=verification_info["display_name"],
        verify_url=_build_public_auth_url(request, "/verify-email", verification_info["token"]),
        from_address=settings.from_address,
        from_name=settings.from_name,
        reply_to_address=settings.reply_to_address,
        reply_to_name=settings.reply_to_name,
    )
    try:
        result = deliver_auth_email(settings, message)
    except AuthEmailDeliveryConfigError as exc:
        logger.exception("Email verification delivery is misconfigured")
        raise HTTPException(status_code=503, detail="Email delivery is not configured") from exc
    except AuthEmailDeliveryTransportError as exc:
        logger.exception("Email verification delivery failed")
        raise HTTPException(status_code=503, detail="Email delivery failed") from exc
    if result.status != "sent":
        logger.warning(
            "Email verification was not sent",
            extra={
                "delivery_status": result.status,
                "delivery_transport": result.transport,
                "delivery_detail": result.detail,
            },
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


@router.post("/forgot-password")
def forgot_password(
    payload: ForgotPasswordRequest,
    request: Request,
    service: AuthService = Depends(get_auth_service),
):
    reset_info = service.request_password_reset(email=payload.email)
    _deliver_password_reset_email(request, reset_info)
    body: dict[str, object] = {"ok": True}
    body.update(_debug_token_payload("reset-password", reset_info["token"] if reset_info else None))
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
    request: Request,
    current_user: AuthenticatedUser = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service),
):
    verification_info = service.issue_email_verification(user_id=current_user.id)
    _deliver_verification_email(request, verification_info)
    body: dict[str, object] = {"ok": True}
    body.update(_debug_token_payload("verify-email", verification_info["token"] if verification_info else None))
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
def google_start(request: Request, role: str = "student", next: str = ""):
    normalized_role = role.strip().lower() or "student"
    if normalized_role not in _PUBLIC_SIGNUP_ROLES:
        raise HTTPException(status_code=400, detail="Unsupported signup role")
    settings = get_google_oauth_settings()
    nonce = mint_session_secret()
    authorize_url = build_google_authorize_url(
        settings,
        state=_encode_google_state(normalized_role, next, nonce),
    )
    redirect = RedirectResponse(authorize_url)
    _set_google_state_cookie(redirect, nonce)
    return redirect


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
    role, next_path, state_nonce = _decode_google_state(state)
    cookie_nonce = str(request.cookies.get(_GOOGLE_STATE_COOKIE_NAME, "") or "").strip() or None
    if not state_nonce or not cookie_nonce or state_nonce != cookie_nonce:
        raise HTTPException(status_code=400, detail="Invalid Google login state")
    settings = get_google_oauth_settings()
    try:
        identity = await exchange_google_code_for_identity(code.strip(), settings)
    except Exception as exc:  # pragma: no cover - external provider failures are integration-tested later
        raise HTTPException(status_code=502, detail="Google login failed") from exc
    try:
        user = service.upsert_google_user(
            email=identity.email,
            display_name=identity.name,
            provider_subject=identity.subject,
            desired_role=role,
        )
    except ValueError as exc:
        if str(exc) == "user_inactive":
            raise HTTPException(status_code=403, detail="Account is not active") from exc
        raise
    session_secret, _session = service.create_auth_session(
        user_id=user["id"],
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
    )
    redirect = RedirectResponse(url=_post_auth_redirect(str(user["role"]), next_path), status_code=302)
    _clear_google_state_cookie(redirect)
    _set_auth_cookie(redirect, session_secret)
    return redirect
