"""
Authentication and authorization related exceptions.

Author: Adam Lyu
Date: 2025-04-05
"""

from app.exceptions.base import BusinessException
from app.core.i18n import get_locale_gettext


class InvalidToken(BusinessException):
    def __init__(self):
        _ = get_locale_gettext()
        super().__init__(
            code="INVALID_TOKEN",
            message=_("Invalid token"),
            status_code=401
        )


class ExpiredToken(BusinessException):
    def __init__(self):
        _ = get_locale_gettext()
        super().__init__(
            code="TOKEN_EXPIRED",
            message=_("Access token has expired"),
            status_code=401
        )


class NotAuthenticated(BusinessException):
    def __init__(self):
        _ = get_locale_gettext()
        super().__init__(
            code="NOT_AUTHENTICATED",
            message=_("User not authenticated"),
            status_code=401
        )


class PermissionDenied(BusinessException):
    def __init__(self):
        _ = get_locale_gettext()
        super().__init__(
            code="PERMISSION_DENIED",
            message=_("Permission denied"),
            status_code=403
        )


class InvalidCredentials(BusinessException):
    def __init__(self):
        _ = get_locale_gettext()
        super().__init__(
            code="INVALID_CREDENTIALS",
            message=_("Invalid email or password"),
            status_code=401
        )


class TooManyLoginAttempts(BusinessException):
    def __init__(self):
        _ = get_locale_gettext()
        super().__init__(
            code="TOO_MANY_ATTEMPTS",
            message=_("Too many login attempts, please try again later"),
            status_code=429
        )
