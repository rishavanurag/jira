from uuid import UUID
from sqlalchemy.orm import Session

from app.models.organization import Membership, MembershipStatus

class MembershipRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, membership: Membership) -> None:
        """Create a membership"""
        self.db.add(membership)

    def get_membership(self, user_id: UUID, organization_id: UUID) -> Membership | None:
        """Get membership details if exists"""
        return (
            self.db.query(Membership)
            .filter(
                Membership.organization_id == organization_id,
                Membership.user_id == user_id,
            )
            .first()
        )

    def get_memberships_by_organization(self, organization_id: UUID, offset:int, limit: int) -> tuple[list[Membership], int]:
        return (
            self.db.query(Membership)
            .filter(
                Membership.organization_id == organization_id,
                Membership.status != MembershipStatus.REMOVED,
            )
            .order_by(Membership.created_at, Membership.id)
            .offset(offset)
            .limit(limit)
            .all(),
            self.db.query(Membership)
            .filter(
                Membership.organization_id == organization_id,
                Membership.status != MembershipStatus.REMOVED,
            )
            .count(),
        )

    def get_pending_memberships_by_user(self, user_id:UUID) -> list[Membership]:
        return (
            self.db.query(Membership)
            .filter(Membership.status == MembershipStatus.PENDING, Membership.user_id == user_id)
            .all()
        )
