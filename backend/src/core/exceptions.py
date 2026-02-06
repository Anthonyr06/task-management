from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
import logging

log = logging.getLogger("api")

def error_payload(code: str, message: str, details=None):
    return {"error": {"code": code, "message": message, "details": details}}

async def http_exception_handler(request: Request, exc: HTTPException):
    log.warning("http_error", extra={"status": exc.status_code, "detail": exc.detail})
    return JSONResponse(
        status_code=exc.status_code,
        content=error_payload("http_error", str(exc.detail)),
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=error_payload("validation_error", "Invalid request", exc.errors()),
    )

async def unhandled_exception_handler(request: Request, exc: Exception):
    log.exception("unhandled_error")
    return JSONResponse(
        status_code=500,
        content=error_payload("internal_error", "Unexpected error"),
    )
