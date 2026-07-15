import uuid
from enum import StrEnum
from pydantic import BaseModel, EmailStr, field_validator


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: str

    @field_validator("full_name")
    def validate_full_name(cls, full_name: str) -> str:
        """validate full name should be a proper string."""
        if full_name.strip() == "":
            raise ValueError("Full name cannot be empty.")
        return full_name.strip()

    @field_validator("password")
    def validate_password(cls, password: str) -> str:
        """validate password should be a proper string amd at least 6 characters long."""
        if not password or password.strip() == "":
            raise ValueError("Password cannot be empty.")
        elif len(password.strip()) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        return password


class UserResponseSchema(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str

    model_config = {"from_attributes": True}


class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: str


class LoginResponseSchema(BaseModel):
    user: UserResponseSchema
    access_token: str
    refresh_token: str


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenPayloadSchema(BaseModel):
    sub: uuid.UUID
    token_type: TokenType
    exp: int


class RefreshTokenRequestSchema(BaseModel):
    refresh_token: str


class RefreshTokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
