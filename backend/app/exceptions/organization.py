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

class UserAlreadyInvitedException(BaseAppException):
    """Raise when user being invited already been invited"""
    error_code = "USER_ALREADY_INVITED"
    message = "User has been invited already"
    status_code = 409


class UserAlreadyMemberException(BaseAppException):
    """Raise when user being invited already a member"""

    error_code = "USER_ALREADY_MEMBER"
    message = "User is a member already"
    status_code = 409

class MembershipNotFoundException(BaseAppException):
    """Raise when user membership record not found"""
    
    error_code = "USER_MEMBERSHIP_NOT_FOUND"
    message = "User membership not found"
    status_code = 404


class UserInvitationNotPendingException:
    """Raised when user invitation is not pending"""
    error_code = "USER_INVITATION_NOT_PENDING"
    message = "User invitation not pending"
    status_code = 409