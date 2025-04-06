"""
User service functions.

Includes:
- User registration
- Current user retrieval
- Email verification
- Logout

Author: Adam Lyu
Date: 2025-04-04
"""

from fastapi import Request, Depends
from jose import JWTError, jwt
from bson import ObjectId
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta

from app.constants.tokens import EmailVerificationPurpose
from app.core.security import hash_password
from app.core.config import settings
from app.core.logger import log

from app.schemas.auth import UserCreate
from app.schemas.user import UserResponse

from app.models.user import User
from app.models.user_token import UserToken

from app.exceptions.user import UserAlreadyExists, UsernameTaken, UserNotFound
from app.exceptions.auth import InvalidToken
from app.services.email.sender import send_welcome_email, send_verification_email


# Generate email verification token
def create_email_verification_token(user_id: str, expires_minutes: int = 60 * 24) -> str:
    payload = {
        "sub": user_id,
        "scope": "email_verification",
        "exp": datetime.utcnow() + timedelta(minutes=expires_minutes)
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


# Register user and send verification email
async def register_user(user_in: UserCreate, request: Request) -> UserResponse:
    trace_id = request.state.trace_id
    log.info("Received registration request", trace_id=trace_id)

    existing = await User.find_one({"email": user_in.email})

    if existing:
        log.warning("Email already exists", trace_id=trace_id)
        raise UserAlreadyExists()

    username_taken = await User.find_one({"username": user_in.username})
    if username_taken:
        log.warning("Username already taken", trace_id=trace_id)
        raise UsernameTaken()

    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hash_password(user_in.password)
    )
    await user.insert()

    log.info("User registered successfully", trace_id=trace_id)

    token = create_email_verification_token(str(user.id))
    verify_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    await send_verification_email(user.email, verify_url, lang=request.state.lang)

    log.info("Verification email sent", trace_id=trace_id, user_id=str(user.id))

    return UserResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        is_verified=user.is_verified,
        role=user.role,
    )


# Get current authenticated user
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        token_id: str = payload.get("jti")
        if user_id is None or token_id is None:
            raise InvalidToken()
    except JWTError:
        raise InvalidToken()

    token_record = await UserToken.find_one({
        "token": token,
        "is_active": True
    })
    if not token_record:
        raise InvalidToken()

    user = await User.get(ObjectId(user_id))
    if user is None or not user.is_active:
        raise UserNotFound()

    return user


# Verify email from token
async def verify_email_by_token(token: str, request: Request) -> dict[str, str]:
    trace_id = request.state.trace_id

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("scope") != "email_verification":
            raise InvalidToken()
    except JWTError:
        log.warning("Email verification failed: token decoding error", trace_id=trace_id)
        raise InvalidToken()

    user_id = payload.get("sub")
    purpose = payload.get("purpose", EmailVerificationPurpose.REGISTER.value)

    user = await User.get(ObjectId(user_id))
    if not user:
        log.warning("Email verification failed: user not found", trace_id=trace_id)
        raise UserNotFound()

    if user.is_verified:
        log.info("Email already verified, skipping", trace_id=trace_id, user_id=str(user.id))
        return {"message": "Email already verified"}

    user.is_verified = True
    await user.save()

    log.info("Email verification succeeded", trace_id=trace_id, user_id=str(user.id))

    if purpose == EmailVerificationPurpose.REGISTER.value:
        await send_welcome_email(user.email, user.username, lang=request.state.lang)

    return {"message": "Email verified successfully"}


# Logout current device
async def logout_user(request: Request, current_user: User):
    token = request.headers.get("authorization", "").replace("Bearer ", "")
    trace_id = request.state.trace_id

    if not token:
        log.warning("Logout failed: missing token", trace_id=trace_id, user_id=str(current_user.id))
        raise InvalidToken()

    token_doc = await UserToken.find_one({"token": token})
    if token_doc:
        token_doc.is_active = False
        await token_doc.save()
        log.info("Logout successful", trace_id=trace_id, user_id=str(current_user.id))
    else:
        log.warning("Token invalid or already revoked", trace_id=trace_id, user_id=str(current_user.id))

    return {"message": "Logout successful"}
