"""
User-related API endpoints.

Includes:
- Get current user info (/me)
- User registration (/register)
- Logout (/logout)
- Email verification (/verify-email)

Author: Adam Lyu
Date: 2025-04-05
"""

from fastapi import APIRouter, Depends, Request, Query
from app.schemas.auth import UserCreate
from app.schemas.user import UserResponse
from app.services.user_service import (
    get_current_user,
    verify_email_by_token,
    logout_user,
    register_user
)
from app.models.user import User
from app.core.logger import log

router = APIRouter()


@router.get("/me", response_model=UserResponse, tags=["User"])
async def get_me(request: Request, current_user: User = Depends(get_current_user)):
    log.info("Fetching current user info", trace_id=request.state.trace_id, user_id=str(current_user.id))
    return UserResponse(
        id=str(current_user.id),
        username=current_user.username,
        email=current_user.email,
        is_verified=current_user.is_verified,
        role=current_user.role,
    )


@router.post("/register", response_model=UserResponse, status_code=201, tags=["User"])
async def register(user_in: UserCreate, request: Request):
    log.info(
        f"User registration requested | username={user_in.username}",
        trace_id=request.state.trace_id
    )
    return await register_user(user_in, request)


@router.post("/logout", tags=["User"])
async def logout(request: Request, current_user: User = Depends(get_current_user)):
    log.info("User logout requested", user_id=str(current_user.id), trace_id=request.state.trace_id)
    return await logout_user(request, current_user)


@router.get("/verify-email", tags=["User"])
async def verify_email(request: Request, token: str = Query(..., description="Email verification token")):
    log.info("Email verification requested", token=token, trace_id=request.state.trace_id)
    return await verify_email_by_token(token, request)
