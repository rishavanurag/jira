from uuid import UUID
from sqlalchemy.orm import Session

from app.models.organization import Organization

class OrganizationRepository:
    
    def __init__(self, db:Session):
        self.db = db

    def create(
        self,
        organization: Organization,
    ) -> None:
        """Create an organization"""
        self.db.add(organization)

    def get_by_id(
        self,
        organization_id: UUID,
    ) -> Organization | None:
        """Get the organization details with the organization id"""
        return self.db.get(Organization, organization_id)

    def get_by_name(
        self,
        name: str,
    ) -> Organization | None:
        """Get the organization details with the organization name"""
        return self.db.query(Organization).filter(Organization.name == name).first()
