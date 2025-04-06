"""
Authentication service functions.

Includes:
- User login logic
- Refresh token handling

Author: Adam Lyu
Date: 2025-04-05
"""

from uuid import uuid4
from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi import Request
from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.core.logger import log
from app.exceptions.auth import InvalidCredentials, InvalidToken
from app.schemas.auth import UserLogin, LoginResponse
from app.schemas.user import UserResponse
from app.models.user import User
from app.models.user_token import UserToken


def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=7)) -> str:
    """生成 refresh token，用于长期登录续期"""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "scope": "refresh_token"})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def extract_refresh_token(request: Request) -> str:
    """从请求头中提取 refresh token"""
    refresh_token = request.headers.get("x-refresh-token")
    if not refresh_token:
        raise InvalidToken()
    return refresh_token


async def refresh_token(request: Request) -> dict[str, str]:
    trace_id = request.state.trace_id
    token = extract_refresh_token(request)

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("scope") != "refresh_token":
            log.warning("Invalid refresh token scope", trace_id=trace_id)
            raise InvalidToken()
    except JWTError:
        log.warning("Invalid refresh token", trace_id=trace_id)
        raise InvalidToken()

    user_id = payload.get("sub")
    if not user_id:
        log.warning("Refresh token missing subject", trace_id=trace_id)
        raise InvalidToken()

    new_access_token = create_access_token(data={"sub": user_id})
    log.info("Access token refreshed successfully", trace_id=trace_id)

    return {"access_token": new_access_token, "token_type": "bearer"}


async def login_user(user_in: UserLogin, request: Request) -> LoginResponse:
    trace_id = request.state.trace_id
    log.info("Login attempt", email=user_in.email, trace_id=trace_id)

    user = await User.find_one(User.email == user_in.email)
    if not user or not verify_password(user_in.password, user.hashed_password):
        log.warning("Login failed: invalid credentials", trace_id=trace_id)
        raise InvalidCredentials()

    token_id = str(uuid4())
    access_token = create_access_token(data={"sub": str(user.id), "jti": token_id})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    user_agent = request.headers.get("user-agent", "Unknown Device")
    await UserToken(
        user_id=user.id,
        token=access_token,
        device_name=user_agent,
        is_active=True
    ).insert()

    log.info("Login successful, access & refresh tokens generated", user_id=str(user.id), trace_id=trace_id)

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            is_verified=user.is_verified,
            role=user.role
        )
    )
