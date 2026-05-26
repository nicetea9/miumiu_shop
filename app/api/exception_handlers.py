"""
Роутеры просто вызывают сервис — не оборачивают в try/except.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import DomainError, InvalidStatusError, NotFoundError, OutOfStockError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def not_found(_: Request, exc: NotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(OutOfStockError)
    async def out_of_stock(_: Request, exc: OutOfStockError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(InvalidStatusError)
    async def invalid_status(_: Request, exc: InvalidStatusError):
        return JSONResponse(status_code=422, content={"detail": str(exc)})

    @app.exception_handler(DomainError)
    async def domain_error(_: Request, exc: DomainError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})
