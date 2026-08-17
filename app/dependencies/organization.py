from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.membership import MembershipRepository
from app.repositories.organization import OrganizationRepository
from app.repositories.role import RoleRepository

from app.services.organization import OrganizationService


def get_organization_repository(db: Session = Depends(get_db)) -> OrganizationRepository:
    return OrganizationRepository(db)


def get_membership_repository(db: Session = Depends(get_db)) -> MembershipRepository:
    return MembershipRepository(db)


def get_role_repository(db: Session = Depends(get_db)) -> RoleRepository:
    return RoleRepository(db)


def get_organization_service(
    db: Session = Depends(get_db),
    organization_repo: OrganizationRepository = Depends(get_organization_repository),
    membership_repo: MembershipRepository = Depends(get_membership_repository),
    role_repo: RoleRepository = Depends(get_role_repository),
) -> OrganizationService:
    return OrganizationService(
        db=db,
        organization_repo=organization_repo,
        membership_repo=membership_repo,
        role_repo=role_repo,
    )
