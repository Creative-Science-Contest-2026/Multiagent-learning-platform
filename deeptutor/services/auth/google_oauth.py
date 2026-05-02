from __future__ import annotations

import os
from urllib.parse import urlencode

import httpx
from pydantic import BaseModel, Field


class GoogleOAuthSettings(BaseModel):
    client_id: str = Field(..., min_length=1)
    client_secret: str = Field(..., min_length=1)
    redirect_uri: str = Field(..., min_length=1)


class GoogleIdentity(BaseModel):
    subject: str
    email: str
    name: str


def get_google_oauth_settings() -> GoogleOAuthSettings:
    return GoogleOAuthSettings(
        client_id=os.getenv("DEEPTUTOR_GOOGLE_CLIENT_ID", "").strip(),
        client_secret=os.getenv("DEEPTUTOR_GOOGLE_CLIENT_SECRET", "").strip(),
        redirect_uri=os.getenv("DEEPTUTOR_GOOGLE_REDIRECT_URI", "").strip(),
    )


def build_google_authorize_url(settings: GoogleOAuthSettings, state: str) -> str:
    query = urlencode(
        {
            "client_id": settings.client_id,
            "redirect_uri": settings.redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "access_type": "online",
            "prompt": "select_account",
        }
    )
    return f"https://accounts.google.com/o/oauth2/v2/auth?{query}"


async def exchange_google_code_for_identity(code: str, settings: GoogleOAuthSettings) -> GoogleIdentity:
    async with httpx.AsyncClient(timeout=20.0) as client:
        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.client_id,
                "client_secret": settings.client_secret,
                "redirect_uri": settings.redirect_uri,
                "grant_type": "authorization_code",
            },
        )
        token_response.raise_for_status()
        token_payload = token_response.json()
        access_token = str(token_payload.get("access_token", "")).strip()
        if not access_token:
            raise ValueError("google_access_token_missing")

        profile_response = await client.get(
            "https://openidconnect.googleapis.com/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_response.raise_for_status()
        profile = profile_response.json()
        return GoogleIdentity(
            subject=str(profile.get("sub", "")).strip(),
            email=str(profile.get("email", "")).strip().lower(),
            name=str(profile.get("name", "")).strip() or str(profile.get("email", "")).strip(),
        )
