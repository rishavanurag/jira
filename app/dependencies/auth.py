from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.auth import AuthService
from app.repositories.user import UserRepository
from app.core.jwt import decode_token
from app.models.auth import User
from app.schemas.auth import TokenType
from app.exceptions.auth import InvalidTokenError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_user_repo(db:Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_auth_service(user_repo: UserRepository = Depends(get_user_repo)) -> AuthService:
    return AuthService(user_repo)

def get_current_user(token: str = Depends(oauth2_scheme), user_repo:UserRepository = Depends(get_user_repo)) -> User:
    """Get the current user details by decoding the token"""
    payload = decode_token(token)
    if not payload.token_type == TokenType.ACCESS:
        raise InvalidTokenError()
    user = user_repo.get_by_id(payload.sub)
    if not user:
        raise InvalidTokenError()
    return user
