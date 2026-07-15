from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.base import BaseAppException
from app.schemas.common import ErrorResponseSchema


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(BaseAppException)
    async def handle_exception(
        request: Request,
        exc: BaseAppException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponseSchema(
                code=exc.error_code,
                message=exc.message,
            ).model_dump(),
        )
