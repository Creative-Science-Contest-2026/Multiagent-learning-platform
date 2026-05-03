from __future__ import annotations

import os
import smtplib
import ssl
from email.message import EmailMessage

from pydantic import BaseModel
from pydantic import Field


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
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_use_tls: bool = True
    smtp_use_ssl: bool = False
    from_address: str = ""
    from_name: str = ""
    timeout_seconds: int = Field(default=30, ge=1, le=120)

    @classmethod
    def from_env(cls) -> "AuthEmailDeliverySettings":
        return cls(
            smtp_host=os.getenv("DEEPTUTOR_AUTH_SMTP_HOST", ""),
            smtp_port=int(os.getenv("DEEPTUTOR_AUTH_SMTP_PORT", "587")),
            smtp_username=os.getenv("DEEPTUTOR_AUTH_SMTP_USERNAME", ""),
            smtp_password=os.getenv("DEEPTUTOR_AUTH_SMTP_PASSWORD", ""),
            smtp_use_tls=_truthy(os.getenv("DEEPTUTOR_AUTH_SMTP_USE_TLS"), default=True),
            smtp_use_ssl=_truthy(os.getenv("DEEPTUTOR_AUTH_SMTP_USE_SSL"), default=False),
            from_address=os.getenv("DEEPTUTOR_AUTH_FROM_ADDRESS", ""),
            from_name=os.getenv("DEEPTUTOR_AUTH_FROM_NAME", ""),
            timeout_seconds=int(os.getenv("DEEPTUTOR_AUTH_SMTP_TIMEOUT_SECONDS", "30")),
        )

    def is_configured(self) -> bool:
        return bool(self.smtp_host.strip() and self.from_address.strip())


def build_password_reset_email(
    *,
    to_email: str,
    display_name: str,
    reset_url: str,
    from_address: str,
    from_name: str = "",
) -> EmailMessage:
    recipient_name = display_name.strip() or to_email.strip()
    message = EmailMessage()
    message["From"] = _from_header(from_address, from_name)
    message["To"] = to_email.strip()
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
) -> EmailMessage:
    recipient_name = display_name.strip() or to_email.strip()
    message = EmailMessage()
    message["From"] = _from_header(from_address, from_name)
    message["To"] = to_email.strip()
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
