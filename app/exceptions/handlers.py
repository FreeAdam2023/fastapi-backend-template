"""
Global exception handler registration for FastAPI.

Author: Adam Lyu
Date: 2025-04-05
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import HTTPException as FastAPIHTTPException

from app.exceptions.base import BusinessException
from app.core.i18n import get_locale_gettext

import logging

logger = logging.getLogger(__name__)


def error_response(code: str, message: str, status_code: int = 400) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message
            }
        }
    )


async def business_exception_handler(request: Request, exc: BusinessException) -> JSONResponse:
    """
    Handle custom BusinessException with i18n message support.
    """
    _ = get_locale_gettext()
    return error_response(
        code=exc.code,
        message=_(exc.message),
        status_code=exc.status_code
    )


async def custom_http_exception_handler(request: Request, exc: FastAPIHTTPException) -> JSONResponse:
    """
    Delegate to FastAPI's built-in HTTPException handler.
    """
    return await http_exception_handler(request, exc)


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle uncaught exceptions as 500 errors with logging.
    """
    logger.exception(f"Unhandled exception: {repr(exc)}")

    _ = get_locale_gettext()
    return error_response(
        code="INTERNAL_ERROR",
        message=_("Internal server error, please try again later."),
        status_code=500
    )


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all global exception handlers to the FastAPI app.
    """
    app.add_exception_handler(BusinessException, business_exception_handler)
    app.add_exception_handler(FastAPIHTTPException, custom_http_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
