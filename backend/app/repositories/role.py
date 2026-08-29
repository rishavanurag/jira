from sqlalchemy.orm import Session

from app.models.organization import Role
from app.constants.role import SystemRoleCode

class RoleRepository:
    def __init__(self, db:Session):
        self.db = db

    def get_system_role(self, role_code:SystemRoleCode) -> Role|None:
        return (
            self.db.query(Role)
            .filter(
                Role.code == role_code, Role.is_system == True, Role.is_active == True
            )
            .first()
        )