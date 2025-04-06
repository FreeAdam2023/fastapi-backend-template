"""
@Time ： 2025-04-05
@Auth ： Adam Lyu
"""

from enum import Enum


class EmailVerificationPurpose(str, Enum):
    REGISTER = "register"
    UPDATE_EMAIL = "update_email"
