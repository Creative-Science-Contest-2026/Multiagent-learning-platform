from __future__ import annotations

import os
import smtplib
import ssl
from email.message import EmailMessage
from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from pydantic import model_validator


def _truthy(value: str | None, *, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _from_header(from_address: str, from_name: str = "") -> str:
    name = from_name.strip()
    if not name:
        return from_address.strip()
    return f"{name} <{from_address.strip()}>"


class AuthEmailDeliverySettings(BaseModel):
    delivery_mode: Literal["auto", "disabled", "required"] = "auto"
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_use_tls: bool = True
    smtp_use_ssl: bool = False
    from_address: str = ""
    from_name: str = ""
    reply_to_address: str = ""
    reply_to_name: str = ""
    provider_name: str = ""
    timeout_seconds: int = Field(default=30, ge=1, le=120)

    @classmethod
    def from_env(cls) -> "AuthEmailDeliverySettings":
        return cls(
            delivery_mode=os.getenv("DEEPTUTOR_AUTH_MAIL_DELIVERY_MODE", "auto"),
            smtp_host=os.getenv("DEEPTUTOR_AUTH_SMTP_HOST", ""),
            smtp_port=int(os.getenv("DEEPTUTOR_AUTH_SMTP_PORT", "587")),
            smtp_username=os.getenv("DEEPTUTOR_AUTH_SMTP_USERNAME", ""),
            smtp_password=os.getenv("DEEPTUTOR_AUTH_SMTP_PASSWORD", ""),
            smtp_use_tls=_truthy(os.getenv("DEEPTUTOR_AUTH_SMTP_USE_TLS"), default=True),
            smtp_use_ssl=_truthy(os.getenv("DEEPTUTOR_AUTH_SMTP_USE_SSL"), default=False),
            from_address=os.getenv("DEEPTUTOR_AUTH_FROM_ADDRESS", ""),
            from_name=os.getenv("DEEPTUTOR_AUTH_FROM_NAME", ""),
            reply_to_address=os.getenv("DEEPTUTOR_AUTH_REPLY_TO_ADDRESS", ""),
            reply_to_name=os.getenv("DEEPTUTOR_AUTH_REPLY_TO_NAME", ""),
            provider_name=os.getenv("DEEPTUTOR_AUTH_MAIL_PROVIDER", ""),
            timeout_seconds=int(os.getenv("DEEPTUTOR_AUTH_SMTP_TIMEOUT_SECONDS", "30")),
        )

    @model_validator(mode="after")
    def _validate_transport(self) -> "AuthEmailDeliverySettings":
        if self.smtp_use_tls and self.smtp_use_ssl:
            raise ValueError("SMTP TLS and SSL modes are mutually exclusive")
        return self

    def is_configured(self) -> bool:
        return bool(self.smtp_host.strip() and self.from_address.strip())

    def is_disabled(self) -> bool:
        return self.delivery_mode == "disabled"

    def is_required(self) -> bool:
        return self.delivery_mode == "required"

    def transport_name(self) -> str:
        return self.provider_name.strip() or "smtp"


class AuthEmailDeliveryConfigError(ValueError):
    """Raised when auth email delivery is required but not configured correctly."""


class AuthEmailDeliveryTransportError(RuntimeError):
    """Raised when auth email delivery fails while running in required mode."""


class AuthEmailDeliveryResult(BaseModel):
    status: Literal["sent", "skipped", "failed"]
    transport: str
    detail: str = ""


def _apply_reply_to(message: EmailMessage, reply_to_address: str = "", reply_to_name: str = "") -> None:
    if not reply_to_address.strip():
        return
    message["Reply-To"] = _from_header(reply_to_address, reply_to_name)


def build_password_reset_email(
    *,
    to_email: str,
    display_name: str,
    reset_url: str,
    from_address: str,
    from_name: str = "",
    reply_to_address: str = "",
    reply_to_name: str = "",
) -> EmailMessage:
    recipient_name = display_name.strip() or to_email.strip()
    message = EmailMessage()
    message["From"] = _from_header(from_address, from_name)
    message["To"] = to_email.strip()
    _apply_reply_to(message, reply_to_address, reply_to_name)
    message["Subject"] = "Dat lai mat khau DeepTutor"
    message.set_content(
        "\n".join(
            [
                f"Xin chao {recipient_name},",
                "",
                "Chung toi da nhan duoc yeu cau dat lai mat khau cho tai khoan DeepTutor cua ban.",
                "Truy cap lien ket ben duoi de tao mat khau moi:",
                reset_url.strip(),
                "",
                "Neu ban khong thuc hien yeu cau nay, ban co the bo qua email nay.",
            ]
        )
    )
    return message


def build_verification_email(
    *,
    to_email: str,
    display_name: str,
    verify_url: str,
    from_address: str,
    from_name: str = "",
    reply_to_address: str = "",
    reply_to_name: str = "",
) -> EmailMessage:
    recipient_name = display_name.strip() or to_email.strip()
    message = EmailMessage()
    message["From"] = _from_header(from_address, from_name)
    message["To"] = to_email.strip()
    _apply_reply_to(message, reply_to_address, reply_to_name)
    message["Subject"] = "Xac minh email DeepTutor"
    message.set_content(
        "\n".join(
            [
                f"Xin chao {recipient_name},",
                "",
                "Hay xac minh dia chi email cua ban de kich hoat day du tai khoan DeepTutor.",
                "Truy cap lien ket ben duoi de hoan tat xac minh:",
                verify_url.strip(),
                "",
                "Neu ban khong tao tai khoan nay, ban co the bo qua email nay.",
            ]
        )
    )
    return message


def send_auth_email(settings: AuthEmailDeliverySettings, message: EmailMessage) -> None:
    timeout = settings.timeout_seconds
    if settings.smtp_use_ssl:
        with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port, timeout=timeout) as smtp:
            if settings.smtp_username.strip():
                smtp.login(settings.smtp_username, settings.smtp_password)
            smtp.send_message(message)
        return

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=timeout) as smtp:
        if settings.smtp_use_tls:
            smtp.starttls(context=ssl.create_default_context())
        if settings.smtp_username.strip():
            smtp.login(settings.smtp_username, settings.smtp_password)
        smtp.send_message(message)


def deliver_auth_email(
    settings: AuthEmailDeliverySettings,
    message: EmailMessage,
) -> AuthEmailDeliveryResult:
    transport = settings.transport_name()
    if settings.is_disabled():
        return AuthEmailDeliveryResult(status="skipped", transport=transport, detail="delivery-disabled")
    if not settings.is_configured():
        if settings.is_required():
            raise AuthEmailDeliveryConfigError(
                "Auth email delivery is required but SMTP transport is not fully configured"
            )
        return AuthEmailDeliveryResult(status="skipped", transport=transport, detail="smtp-not-configured")
    try:
        send_auth_email(settings, message)
    except Exception as exc:
        if settings.is_required():
            raise AuthEmailDeliveryTransportError("Auth email delivery failed") from exc
        return AuthEmailDeliveryResult(status="failed", transport=transport, detail=exc.__class__.__name__)
    return AuthEmailDeliveryResult(status="sent", transport=transport, detail="smtp-sent")
