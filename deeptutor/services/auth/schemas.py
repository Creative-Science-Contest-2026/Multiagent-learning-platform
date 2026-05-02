from __future__ import annotations

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


class AuthenticatedUser(BaseModel):
    id: str
    email: EmailStr
    display_name: str
    role: Literal["teacher", "student", "admin"]
