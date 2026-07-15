from pydantic import BaseModel

class ErrorResponseSchema(BaseModel):
    code: str
    message: str