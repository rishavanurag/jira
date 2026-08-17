from uuid import UUID
from fastapi import APIRouter, Depends, status

from app.models.auth import User

from app.schemas.organization import (
    OrganizationCreateRequestSchema,
    OrganizationResponseSchema,
    OrganizationUpdateRequestSchema,
)

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
