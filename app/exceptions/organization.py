from app.exceptions.base import BaseAppException

class OrganizationAlreadyExistsException(BaseAppException):
    """Raise when organization name already exists"""
    error_code = "ORGANIZATION_ALREADY_EXISTS"
    message = "Organization already exists"
    status_code = 409


class OrganizationNotFoundException(BaseAppException):
    """Raise when organization does not exists"""
    error_code = "ORGANIZATION_NOT_FOUND"
    message = "Organization not found"
    status_code = 404