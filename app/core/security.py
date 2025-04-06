"""
@Time  ：2025-04-04
@Auth  ：Adam Lyu
"""

import logging
from datetime import datetime, timedelta, UTC
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from app.constants.tokens import EmailVerificationPurpose
from app.core.config import settings

# 初始化日志
logger = logging.getLogger(__name__)

# 创建密码上下文（用于加密和校验）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    哈希密码（不记录日志，避免泄密）
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """
    验证密码（不记录日志，避免泄密）
    """
    return pwd_context.verify(password, hashed)


def create_access_token(data: dict, expires_minutes: Optional[int] = None) -> str:
    """
    创建访问令牌
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    logger.info(f"Issued access token for user_id={data.get('sub')}")
    return token


def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=30)) -> str:
    """
    创建刷新令牌
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({"exp": expire, "scope": "refresh_token"})
    token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    logger.info(f"Issued refresh token for user_id={data.get('sub')}")
    return token


def create_email_verification_token(
    user_id: str,
    purpose: EmailVerificationPurpose = EmailVerificationPurpose.REGISTER,
    expires_minutes: int = 60 * 24
) -> str:
    """
    创建邮箱验证令牌
    """
    payload = {
        "sub": user_id,
        "scope": "email_verification",
        "purpose": purpose.value,
        "exp": datetime.now(UTC) + timedelta(minutes=expires_minutes)
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    logger.info(f"Issued email verification token: user_id={user_id}, purpose={purpose.value}")
    return token
