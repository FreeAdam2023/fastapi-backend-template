"""
@Time ： 2025-04-06
@Auth ： Adam Lyu
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from jose import JWTError, jwt
from app.core.config import settings
from app.models.user import User


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.user = None  # 默认无用户

        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[-1]
            try:
                payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
                user_id = payload.get("sub")
                if user_id:
                    user = await User.get(user_id)
                    if user and user.is_active:
                        request.state.user = user
            except JWTError:
                pass  # 无效 token，state.user 仍为 None

        response: Response = await call_next(request)
        return response
