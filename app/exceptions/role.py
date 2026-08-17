from app.exceptions.base import BaseAppException

class SystemRoleNotConfiguredException(BaseAppException):
    """Raised when system role not configured"""
    error_code = "SYSTEM_ROLE_NOT_CONFIGURED"
    message = "An unexpected error occurred"
    status_code = 500