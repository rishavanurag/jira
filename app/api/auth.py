from fastapi import APIRouter, Depends, status

from app.schemas.auth import (
    UserCreateSchema,
    UserResponseSchema,
    LoginRequestSchema,
    LoginResponseSchema,
    RefreshTokenRequestSchema,
    RefreshTokenResponseSchema,
)
from app.dependencies.auth import get_auth_service, get_current_user
from app.services.auth import AuthService
from app.models.auth import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED
)
def register_user(
    user_data: UserCreateSchema, auth_service: AuthService = Depends(get_auth_service)
) -> UserResponseSchema:
    """Register user and return user details"""
    return auth_service.register_user(user_data)


@router.post(
    "/login", response_model=LoginResponseSchema, status_code=status.HTTP_200_OK
)
def login_user(
    login_data: LoginRequestSchema,
    auth_service: AuthService = Depends(get_auth_service),
) -> LoginResponseSchema:
    """Authenticate a user and return access and refresh tokens"""
    return auth_service.login_user(login_data)


@router.get("/me", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def get_me(current_user: User = Depends(get_current_user)) -> UserResponseSchema:
    return UserResponseSchema.model_validate(current_user)


@router.post("/refresh", response_model=RefreshTokenResponseSchema, status_code=status.HTTP_200_OK)
def refresh_token(
    refresh_data: RefreshTokenRequestSchema,
    auth_service: AuthService = Depends(get_auth_service),
) -> RefreshTokenResponseSchema:
    return auth_service.refresh_token(refresh_data.refresh_token)