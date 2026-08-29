from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends, status, Query

from app.models.auth import User

from app.schemas.organization import (
    OrganizationCreateRequestSchema,
    OrganizationResponseSchema,
    OrganizationUpdateRequestSchema,
    OrganizationMemberInviteRequestSchema,
    MembershipResponseSchema,
)

from app.schemas.common import PaginationResponse

from app.services.organization import OrganizationService

from app.dependencies.auth import get_current_user
from app.dependencies.organization import get_organization_service

router = APIRouter(prefix="/organization", tags=["Organization"])


@router.post(
    "/",
    response_model=OrganizationResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_organization(
    organization_data: OrganizationCreateRequestSchema,
    current_user: User = Depends(get_current_user),
    organization_service: OrganizationService = Depends(get_organization_service),
) -> OrganizationResponseSchema:
    return organization_service.create_organization(
        owner_id=current_user.id,
        name=organization_data.name,
        description=organization_data.description,
    )


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponseSchema,
    status_code=status.HTTP_200_OK,
)
def get_organization(
    organization_id: UUID,
    current_user: User = Depends(get_current_user),
    organization_service: OrganizationService = Depends(get_organization_service),
) -> OrganizationResponseSchema:
    return organization_service.get_organization(
        user_id=current_user.id, organization_id=organization_id
    )


@router.patch(
    "/{organization_id}",
    response_model=OrganizationResponseSchema,
    status_code=status.HTTP_200_OK,
)
def update_organization(
    organization_id: UUID,
    organization_data: OrganizationUpdateRequestSchema,
    current_user: User = Depends(get_current_user),
    organization_service: OrganizationService = Depends(get_organization_service),
) -> OrganizationResponseSchema:
    return organization_service.update_organization(
        organization_id=organization_id,
        user_id=current_user.id,
        organization_data=organization_data,
    )


@router.post(
    "/{organization_id}/members",
    response_model=MembershipResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def invite_member(
    organization_id: UUID,
    invite_member_data: OrganizationMemberInviteRequestSchema,
    current_user: User = Depends(get_current_user),
    organization_service: OrganizationService = Depends(get_organization_service),
) -> MembershipResponseSchema:
    return organization_service.invite_member(
        organization_id=organization_id,
        user_id=current_user.id,
        invite_member_data=invite_member_data,
    )


@router.post(
    "/{organization_id}/members/accept",
    response_model=MembershipResponseSchema,
    status_code=status.HTTP_200_OK,
)
def accept_membership(
    organization_id: UUID,
    current_user: User = Depends(get_current_user),
    organization_service: OrganizationService = Depends(get_organization_service),
) -> MembershipResponseSchema:
    return organization_service.accept_invitation(
        organization_id=organization_id, user_id=current_user.id
    )


@router.post(
    "/{organization_id}/members/reject",
    response_model=MembershipResponseSchema,
    status_code=status.HTTP_200_OK,
)
def reject_invitation(
    organization_id: UUID,
    current_user: User = Depends(get_current_user),
    organization_service: OrganizationService = Depends(get_organization_service),
) -> MembershipResponseSchema:
    return organization_service.reject_invitation(
        organization_id=organization_id, user_id=current_user.id
    )


@router.post(
    "/{organization_id}/members/{member_id}/remove",
    response_model=MembershipResponseSchema,
    status_code=status.HTTP_200_OK,
)
def remove_member(
    organization_id: UUID,
    member_id: UUID,
    current_user: User = Depends(get_current_user),
    organization_service: OrganizationService = Depends(get_organization_service),
) -> MembershipResponseSchema:
    return organization_service.remove_member(
        organization_id=organization_id, user_id=current_user.id, member_id=member_id
    )


@router.get(
    "/{organization_id}/members",
    response_model=PaginationResponse[MembershipResponseSchema],
    status_code=status.HTTP_200_OK,
)
def get_organization_members(
    organization_id: UUID,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,
    current_user: User = Depends(get_current_user),
    organization_service: OrganizationService = Depends(get_organization_service),
) -> PaginationResponse[MembershipResponseSchema]:
    return organization_service.get_organization_members(
        organization_id=organization_id, user_id=current_user.id, page=page, page_size=page_size
    )


@router.get(
    "/memberships/invitations",
    response_model=list[MembershipResponseSchema],
    status_code=status.HTTP_200_OK
)
def get_pending_invitations(
    current_user: User = Depends(get_current_user),
    organization_service: OrganizationService = Depends(get_organization_service)
) -> list[MembershipResponseSchema]:
    return organization_service.get_pending_invitations(user_id=current_user.id)
