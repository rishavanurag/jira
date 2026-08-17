from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.constants.role import SystemRoleCode

from app.repositories.organization import OrganizationRepository
from app.repositories.membership import MembershipRepository
from app.repositories.role import RoleRepository

from app.models.organization import Role, Organization, Membership, MembershipStatus

from app.schemas.organization import (
    OrganizationResponseSchema,
    OrganizationUpdateRequestSchema,
)

from app.exceptions.organization import (
    OrganizationAlreadyExistsException,
    OrganizationNotFoundException,
)
from app.exceptions.role import SystemRoleNotConfiguredException
from app.exceptions.auth import UserNotAuthorizedError


class OrganizationService:
    def __init__(
        self,
        db: Session,
        organization_repo: OrganizationRepository,
        membership_repo: MembershipRepository,
        role_repo: RoleRepository,
    ):
        self.db = db
        self.organization_repo = organization_repo
        self.membership_repo = membership_repo
        self.role_repo = role_repo

    def create_organization(
        self, *, owner_id: UUID, name: str, description: str | None
    ) -> OrganizationResponseSchema:
        try:
            self._validate_unique_name(name)

            role = self._get_system_owner_role()

            organization = self._persist_organization(
                name=name, description=description
            )

            self._persist_owner_membership(
                owner_id=owner_id, organization_id=organization.id, role_id=role.id
            )

            self.db.commit()
            self.db.refresh(organization)
            return OrganizationResponseSchema.model_validate(organization)
        except Exception:
            self.db.rollback()
            raise

    def get_organization(
        self, user_id: UUID, organization_id: UUID
    ) -> OrganizationResponseSchema:
        organization = self.organization_repo.get_by_id(organization_id=organization_id)
        if not organization:
            raise OrganizationNotFoundException()
        membership = self.membership_repo.get_membership(
            user_id=user_id, organization_id=organization_id
        )
        if not (membership and membership.status == MembershipStatus.ACTIVE):
            raise UserNotAuthorizedError()
        return OrganizationResponseSchema.model_validate(organization)

    def update_organization(
        self,
        organization_id: UUID,
        user_id: UUID,
        organization_data: OrganizationUpdateRequestSchema,
    ) -> OrganizationResponseSchema:
        organization = self.organization_repo.get_by_id(organization_id=organization_id)
        if not organization:
            raise OrganizationNotFoundException()
        self._validate_organization_owner(user_id=user_id, organization_id=organization_id)
        if "description" in organization_data.model_fields_set:
            organization.description = organization_data.description
        try:
            self.db.commit()
            self.db.refresh(organization)
            return OrganizationResponseSchema.model_validate(organization)
        except Exception:
            self.db.rollback()
            raise

    # ----------------------------
    # Private Helpers
    # ----------------------------

    def _validate_unique_name(self, name: str) -> None:
        organization = self.organization_repo.get_by_name(name)

        if organization is not None:
            raise OrganizationAlreadyExistsException()

    def _get_system_owner_role(self) -> Role:
        role = self.role_repo.get_system_owner_role(SystemRoleCode.OWNER)

        if role is None:
            raise SystemRoleNotConfiguredException()

        return role

    def _persist_organization(
        self, *, name: str, description: str | None
    ) -> Organization:
        organization = Organization(name=name, description=description)
        self.organization_repo.create(organization=organization)
        self.db.flush()
        return organization

    def _persist_owner_membership(
        self, owner_id: UUID, organization_id: UUID, role_id: UUID
    ) -> None:
        membership = Membership(
            user_id=owner_id,
            organization_id=organization_id,
            role_id=role_id,
            status=MembershipStatus.ACTIVE,
            joined_at=datetime.now(timezone.utc),
        )
        self.membership_repo.create(membership=membership)

    def _validate_organization_owner(
        self, user_id: UUID, organization_id: UUID
    ) -> Membership:
        membership = self.membership_repo.get_membership(user_id, organization_id)
        if not (
            membership
            and membership.status == MembershipStatus.ACTIVE
            and membership.role.code == SystemRoleCode.OWNER
        ):
            raise UserNotAuthorizedError()
        return membership
