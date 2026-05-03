from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class SignupRequest(BaseModel):
    display_name: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    role: str = Field(..., min_length=1, max_length=32)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=16, max_length=256)
    password: str = Field(..., min_length=8, max_length=128)


class VerifyEmailRequest(BaseModel):
    token: str = Field(..., min_length=16, max_length=256)


class AdminCreateUserRequest(BaseModel):
    display_name: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    role: Literal["teacher", "student", "admin"]


class AdminUpdateUserRequest(BaseModel):
    role: Literal["teacher", "student", "admin"] | None = None
    status: Literal["active", "suspended"] | None = None


class AuthenticatedUser(BaseModel):
    id: str
    email: EmailStr
    display_name: str
    role: Literal["teacher", "student", "admin"]
    email_verified_at: datetime | None = None
