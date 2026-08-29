from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from typing import List

from app.constants.role import SystemRoleCode

from app.repositories.organization import OrganizationRepository
from app.repositories.membership import MembershipRepository
from app.repositories.role import RoleRepository
from app.repositories.user import UserRepository

from app.models.organization import Role, Organization, Membership, MembershipStatus

from app.schemas.organization import (
    OrganizationResponseSchema,
    OrganizationUpdateRequestSchema,
    OrganizationMemberInviteRequestSchema,
    MembershipResponseSchema,
)

from app.schemas.common import PaginationResponse

from app.exceptions.organization import (
    OrganizationAlreadyExistsException,
    OrganizationNotFoundException,
    UserAlreadyInvitedException,
    UserAlreadyMemberException,
    MembershipNotFoundException,
    UserInvitationNotPendingException,
)
from app.exceptions.role import SystemRoleNotConfiguredException
from app.exceptions.auth import UserNotAuthorizedError, UserNotFoundException


class OrganizationService:

    def __init__(
        self,
        db: Session,
        organization_repo: OrganizationRepository,
        membership_repo: MembershipRepository,
        role_repo: RoleRepository,
        user_repo: UserRepository,
    ):
        self.db = db
        self.organization_repo = organization_repo
        self.membership_repo = membership_repo
        self.role_repo = role_repo
        self.user_repo = user_repo

    def create_organization(
        self, *, owner_id: UUID, name: str, description: str | None
    ) -> OrganizationResponseSchema:
        try:
            self._validate_unique_name(name)

            owner_role = self._get_system_role(SystemRoleCode.OWNER)

            organization = self._persist_organization(
                name=name, description=description
            )

            self._persist_owner_membership(
                owner_id=owner_id,
                organization_id=organization.id,
                role_id=owner_role.id,
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
        organization = self._get_organization_or_raise(organization_id=organization_id)
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
        organization = self._get_organization_or_raise(organization_id)
        self._validate_organization_owner(
            user_id=user_id, organization_id=organization_id
        )
        if "description" in organization_data.model_fields_set:
            organization.description = organization_data.description
        try:
            self.db.commit()
            self.db.refresh(organization)
            return OrganizationResponseSchema.model_validate(organization)
        except Exception:
            self.db.rollback()
            raise

    def invite_member(
        self,
        organization_id: UUID,
        user_id: UUID,
        invite_member_data: OrganizationMemberInviteRequestSchema,
    ) -> MembershipResponseSchema:
        self._get_organization_or_raise(organization_id=organization_id)
        self._validate_organization_owner(
            user_id=user_id, organization_id=organization_id
        )

        user = self.user_repo.get_by_email(invite_member_data.email)
        if not user:
            raise UserNotFoundException()

        existing_membership = self.membership_repo.get_membership(
            user_id=user.id, organization_id=organization_id
        )
        system_member_role = self._get_system_role(SystemRoleCode.MEMBER)
        try:
            if (
                not existing_membership
                or existing_membership.status == MembershipStatus.REMOVED
            ):
                membership = Membership(
                    user_id=user.id,
                    organization_id=organization_id,
                    role_id=system_member_role.id,
                    status=MembershipStatus.PENDING,
                    joined_at=None,
                    accepted_at=None,
                    invited_by=user_id,
                )
                self.membership_repo.create(membership=membership)
                self.db.commit()
                self.db.refresh(membership)
                return MembershipResponseSchema(
                    email=membership.user.email,
                    organization_id=membership.organization_id,
                    role_code=membership.role.code,
                    status=membership.status,
                )
            if existing_membership.status == MembershipStatus.REJECTED:
                existing_membership.status = MembershipStatus.PENDING
                existing_membership.invited_by = user_id
                existing_membership.joined_at = None
                existing_membership.accepted_at = None
                self.db.commit()
                self.db.refresh(existing_membership)
                return MembershipResponseSchema(
                    email=existing_membership.user.email,
                    organization_id=existing_membership.organization_id,
                    role_code=existing_membership.role.code,
                    status=existing_membership.status,
                )

            if existing_membership.status == MembershipStatus.PENDING:
                raise UserAlreadyInvitedException()

            if existing_membership.status == MembershipStatus.ACTIVE:
                raise UserAlreadyMemberException()
        except Exception:
            self.db.rollback()
            raise

    def accept_invitation(
        self, organization_id: UUID, user_id: UUID
    ) -> MembershipResponseSchema:
        self._get_organization_or_raise(organization_id=organization_id)
        existing_membership = self.membership_repo.get_membership(
            user_id=user_id, organization_id=organization_id
        )
        if not existing_membership:
            raise MembershipNotFoundException()

        if existing_membership.status == MembershipStatus.ACTIVE:
            raise UserAlreadyMemberException()

        if existing_membership.status != MembershipStatus.PENDING:
            raise UserInvitationNotPendingException()

        try:
            time_now = datetime.now(timezone.utc)
            existing_membership.status = MembershipStatus.ACTIVE
            existing_membership.joined_at = time_now
            existing_membership.accepted_at = time_now
            self.db.commit()
            self.db.refresh(existing_membership)
            return MembershipResponseSchema(
                email=existing_membership.user.email,
                organization_id=existing_membership.organization_id,
                role_code=existing_membership.role.code,
                status=existing_membership.status,
            )
        except Exception:
            self.db.rollback()
            raise

    def reject_invitation(
        self,
        organization_id: UUID,
        user_id: UUID,
    ) -> MembershipResponseSchema:
        self._get_organization_or_raise(organization_id=organization_id)
        existing_membership = self.membership_repo.get_membership(
            user_id=user_id, organization_id=organization_id
        )
        if not existing_membership:
            raise MembershipNotFoundException()

        if existing_membership.status != MembershipStatus.PENDING:
            raise UserInvitationNotPendingException()
        try:
            existing_membership.status = MembershipStatus.REJECTED
            self.db.commit()
            self.db.refresh(existing_membership)
            return MembershipResponseSchema(
                email=existing_membership.user.email,
                organization_id=existing_membership.organization_id,
                role_code=existing_membership.role.code,
                status=existing_membership.status,
            )
        except Exception:
            self.db.rollback()
            raise

    def remove_member(
        self, organization_id: UUID, user_id: UUID, member_id: UUID
    ) -> MembershipResponseSchema:
        self._get_organization_or_raise(organization_id=organization_id)
        self._validate_organization_owner(
            user_id=user_id, organization_id=organization_id
        )

        member = self.user_repo.get_by_id(member_id)
        if not member:
            raise UserNotFoundException()

        membership = self.membership_repo.get_membership(
            user_id=member_id, organization_id=organization_id
        )
        if not membership:
            raise MembershipNotFoundException()

        if membership.role.code == SystemRoleCode.OWNER:
            raise UserNotAuthorizedError()

        if membership.status != MembershipStatus.ACTIVE:
            raise UserNotAuthorizedError()

        try:
            membership.status = MembershipStatus.REMOVED
            self.db.commit()
            self.db.refresh(membership)
            return MembershipResponseSchema(
                email=membership.user.email,
                organization_id=membership.organization_id,
                role_code=membership.role.code,
                status=membership.status,
            )
        except Exception:
            self.db.rollback()
            raise

    # def get_organization_members(
    #     self, organization_id: UUID, user_id: UUID
    # ) -> List[MembershipResponseSchema]:
    #     self._get_organization_or_raise(organization_id=organization_id)
    #     membership = self.membership_repo.get_membership(user_id, organization_id)
    #     if not (membership and membership.status == MembershipStatus.ACTIVE):
    #         raise UserNotAuthorizedError()
    #     members = self.membership_repo.get_memberships_by_organization(
    #         organization_id=organization_id
    #     )
    #     return [
    #         MembershipResponseSchema(
    #             email=member.user.email,
    #             organization_id=member.organization_id,
    #             role_code=member.role.code,
    #             status=member.status,
    #         )
    #         for member in members
    #         if member.status != MembershipStatus.REMOVED
    #     ]
    def get_organization_members(
        self, organization_id: UUID, user_id: UUID, page: int, page_size: int
    ) -> PaginationResponse[MembershipResponseSchema]:
        self._get_organization_or_raise(organization_id=organization_id)
        membership = self.membership_repo.get_membership(user_id, organization_id)
        if not (membership and membership.status == MembershipStatus.ACTIVE):
            raise UserNotAuthorizedError()
        members, total = self.membership_repo.get_memberships_by_organization(
            organization_id=organization_id,
            offset=(page - 1) * page_size,
            limit=page_size,
        )
        return PaginationResponse(
            items=[
                MembershipResponseSchema(
                    email=member.user.email,
                    organization_id=member.organization_id,
                    role_code=member.role.code,
                    status=member.status,
                )
                for member in members
            ],
            total=total,
            page=page,
            page_size=page_size,
            pages=(total + page_size - 1) // page_size,
        )

    def get_pending_invitations(self, user_id: UUID) -> list[MembershipResponseSchema]:
        memberships = self.membership_repo.get_pending_memberships_by_user(
            user_id=user_id
        )
        return [
            MembershipResponseSchema(
                email=member.user.email,
                organization_id=member.organization_id,
                role_code=member.role.code,
                status=member.status,
            )
            for member in memberships
        ]

    # ----------------------------
    # Private Helpers
    # ----------------------------

    def _get_organization_or_raise(self, organization_id: UUID) -> Organization:
        organization = self.organization_repo.get_by_id(organization_id=organization_id)
        if not organization:
            raise OrganizationNotFoundException()
        return organization

    def _validate_unique_name(self, name: str) -> None:
        organization = self.organization_repo.get_by_name(name)

        if organization is not None:
            raise OrganizationAlreadyExistsException()

    def _get_system_role(self, role_code: SystemRoleCode) -> Role:
        role = self.role_repo.get_system_role(role_code)

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
