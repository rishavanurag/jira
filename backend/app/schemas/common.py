from typing import Generic, TypeVar

from pydantic import BaseModel


class ErrorResponseSchema(BaseModel):
    code: str
    message: str

T = TypeVar("T")
class PaginationResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int
