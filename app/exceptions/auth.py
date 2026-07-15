from app.exceptions.base import BaseAppException

class UserAlreadyExistsError(BaseAppException):
    """Raised when attempting to create a user that already exists."""
    error_code = "USER_ALREADY_EXISTS"
    message = "User already exists"
    status_code = 409


class InvalidCredentialsError(BaseAppException):
    """Raised when Invalid credentials are provided"""
    error_code = "INVALID_CREDENTIALS"
    message = "Incorrect email or password"
    status_code = 401


class InactiveUserError(BaseAppException):
    """Raised when Invalid credentials are provided"""
    error_code = "INACTIVE_USER"
    message = "User account is inactive"
    status_code = 403


class InvalidTokenError(BaseAppException):
    """Raised when invalid token is passed"""
    error_code = "INVALID_TOKEN"
    message = "Invalid or expired token"
    status_code = 401
