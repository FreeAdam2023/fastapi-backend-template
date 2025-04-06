"""
Authentication API endpoints.

Includes:
- User login (/login)
- Token refresh (/refresh)

Author: Adam Lyu
Date: 2025-04-04
"""

from fastapi import APIRouter, Request
from app.schemas.auth import UserLogin, LoginResponse, Token
from app.services.auth_service import refresh_token, login_user
from app.core.logger import log

router = APIRouter()


@router.post("/login", response_model=LoginResponse, tags=["Auth"])
async def login(user_in: UserLogin, request: Request):
    log.info("Login attempt", trace_id=request.state.trace_id, user_id=user_in.email, client_ip=request.client.host)
    response = await login_user(user_in, request)
    log.info("Login success", trace_id=request.state.trace_id, user_id=user_in.email)
    return response


@router.post("/refresh", response_model=Token, tags=["Auth"])
async def refresh(request: Request):
    log.info("Token refresh requested", trace_id=request.state.trace_id)
    response = await refresh_token(request)
    log.info("Token refresh successful", trace_id=request.state.trace_id)
    return response
