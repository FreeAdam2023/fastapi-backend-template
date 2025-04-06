"""
@Time ： 2025-04-05
@Auth ： Adam Lyu
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, user, status

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(user.router, prefix="/user", tags=["User"])
router.include_router(status.router, prefix="/status", tags=["Health"])