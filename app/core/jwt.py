import uuid
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError
from datetime import timedelta, datetime, timezone

from app.core.settings import settings
from app.schemas.auth import TokenType, TokenPayloadSchema
from app.exceptions.auth import InvalidTokenError


def create_token(user_id: uuid.UUID, token_type: TokenType, expires_delta: timedelta):
    now = datetime.now(timezone.utc)
    exp_time = now + expires_delta
    payload = {
        "sub": str(user_id),
        "token_type": token_type.value,
        "exp": int(exp_time.timestamp()),
    }
    return jwt.encode(
        payload, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


def create_access_token(user_id: uuid.UUID) -> str:
    return create_token(
        user_id=user_id,
        token_type=TokenType.ACCESS,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(user_id: uuid.UUID) -> str:
    return create_token(
        user_id=user_id,
        token_type=TokenType.REFRESH,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def decode_token(token: str) -> TokenPayloadSchema:
    try:
        decoded_payload = jwt.decode(
            token=token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return TokenPayloadSchema.model_validate(decoded_payload)
    except (JWTError, ValidationError):
        raise InvalidTokenError()
