"""
User-related business exceptions.

Author: Adam Lyu
Date: 2025-04-05
"""

from app.exceptions.base import BusinessException
from app.core.i18n import get_locale_gettext


class UserAlreadyExists(BusinessException):
    def __init__(self):
        _ = get_locale_gettext()
        super().__init__(
            code="USER_EXISTS",
            message=_("User already exists"),
            status_code=400
        )


class InvalidUsername(BusinessException):
    def __init__(self):
        _ = get_locale_gettext()
        super().__init__(
            code="INVALID_USERNAME",
            message=_("Invalid username"),
            status_code=422
        )


class UsernameTaken(BusinessException):
    def __init__(self):
        _ = get_locale_gettext()
        super().__init__(
            code="USERNAME_TAKEN",
            message=_("Username is already taken"),
            status_code=400
        )


class UserNotFound(BusinessException):
    def __init__(self):
        _ = get_locale_gettext()
        super().__init__(
            code="USER_NOT_FOUND",
            message=_("User not found or deactivated"),
            status_code=404
        )


class EmailFormatInvalid(BusinessException):
    def __init__(self):
        _ = get_locale_gettext()
        super().__init__(
            code="INVALID_EMAIL",
            message=_("Invalid email format"),
            status_code=422
        )
