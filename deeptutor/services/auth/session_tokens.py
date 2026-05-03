from __future__ import annotations

import hashlib
import secrets


def mint_session_secret() -> str:
    return secrets.token_urlsafe(48)


def hash_session_secret(secret: str) -> str:
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()
