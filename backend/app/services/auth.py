from app.repositories.user import UserRepository
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token, create_refresh_token, decode_token
from app.schemas.auth import UserCreateSchema, UserResponseSchema, LoginRequestSchema, LoginResponseSchema, RefreshTokenResponseSchema, TokenType
from app.exceptions.auth import UserAlreadyExistsError, InvalidCredentialsError, InactiveUserError, InvalidTokenError

class AuthService:
    def __init__(self, user_repo:UserRepository):
        self.user_repo = user_repo

    def register_user(self, user_data:UserCreateSchema) -> UserResponseSchema:
        """Register a new user with email, full name, and password."""
        # Check if the email is already registered
        existing_user = self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise UserAlreadyExistsError()
        # Hash the password before storing it
        password_hash = hash_password(user_data.password)
        # Create the new user in the database
        user = self.user_repo.create(email=user_data.email, full_name=user_data.full_name, password_hash=password_hash)
        return UserResponseSchema.model_validate(user)

    def login_user(self, login_data: LoginRequestSchema) -> LoginResponseSchema:
        """Login a user with email and password"""
        # check if email exists
        user = self.user_repo.get_by_email(login_data.email)
        if not user:
            raise InvalidCredentialsError()
        # check if the password is correct
        if not verify_password(login_data.password, user.password_hash):
            raise InvalidCredentialsError()
        if not user.is_active:
            raise InactiveUserError()
        return LoginResponseSchema(
            user=UserResponseSchema.model_validate(user),
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id)
        )

    def refresh_token(self, token:str) -> RefreshTokenResponseSchema:
        """Generate new token pair"""
        payload = decode_token(token)
        if payload.token_type != TokenType.REFRESH:
            raise InvalidTokenError()
        user = self.user_repo.get_by_id(payload.sub)
        if not user:
            raise InvalidTokenError()
        if not user.is_active:
            raise InactiveUserError()
        access_token=create_access_token(user.id)
        refresh_token=create_refresh_token(user.id)
        return RefreshTokenResponseSchema(
            access_token = access_token,
            refresh_token = refresh_token
        )
