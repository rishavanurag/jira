from uuid import UUID
from typing import Annotated
from pydantic import BaseModel, StringConstraints, ConfigDict, Field


class OrganizationCreateRequestSchema(BaseModel):
    name: Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=100,
            strip_whitespace=True,
        ),
    ]
    description: Annotated[
        str | None, StringConstraints(max_length=255, strip_whitespace=True)
    ] = None


class OrganizationResponseSchema(BaseModel):
    id: UUID
    name: str
    description: str | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class OrganizationUpdateRequestSchema(BaseModel):
    description: str | None = Field(default=None)
