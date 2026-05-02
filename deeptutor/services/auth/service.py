from __future__ import annotations

from datetime import UTC
from datetime import datetime
from datetime import timedelta

from deeptutor.services.auth.passwords import hash_password
from deeptutor.services.auth.session_tokens import hash_session_secret
from deeptutor.services.auth.session_tokens import mint_session_secret


class AuthService:
    def create_user(self, *, email: str, display_name: str, role: str, password: str) -> dict[str, str]:
        return {
            "email": email.strip().lower(),
            "display_name": display_name.strip(),
            "role": role,
            "password_hash": hash_password(password),
        }

    def create_auth_session(
        self,
        *,
        user_id: str,
        user_agent: str | None,
        ip_address: str | None,
    ) -> tuple[str, dict[str, str | None]]:
        secret = mint_session_secret()
        return secret, {
            "user_id": user_id,
            "session_secret_hash": hash_session_secret(secret),
            "user_agent": user_agent,
            "ip_address": ip_address,
            "expires_at": (datetime.now(UTC) + timedelta(days=14)).isoformat(),
        }
