"""
@Time : 2025-04-06
@Auth : Adam Lyu
@Desc : Standard health check endpoints: /status, /status/db, /status/version
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from beanie import Document
from app.core.config import settings
from app.core.logger import log

router = APIRouter()


@router.get("/", summary="Basic service health check")
async def health_check():
    return {"status": "ok", "message": "Service is running."}


@router.get("/db", summary="Database connectivity check")
async def database_check():
    try:
        # Use a dummy Beanie Document to test database availability
        class Ping(Document):
            pass

        await Ping.find_one()
        return {"status": "ok", "message": "Database is connected."}
    except Exception as e:
        log.warning("MongoDB connectivity check failed", message=str(e))
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Database connection failed."}
        )


@router.get("/version", summary="Project version information")
async def version_info():
    return {
        "status": "ok",
        "version": settings.PROJECT_VERSION,
        "environment": settings.ENVIRONMENT,
    }
