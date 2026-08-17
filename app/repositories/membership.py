from uuid import UUID
from sqlalchemy.orm import Session

from app.models.organization import Membership


class MembershipRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, membership:Membership) -> None:
        """Create a membership"""
        self.db.add(membership)
    
    def get_membership(self, user_id:UUID, organization_id:UUID) -> Membership|None:
        """Get membership details if exists"""
        return self.db.query(Membership).filter(Membership.organization_id==organization_id, Membership.user_id == user_id).first()