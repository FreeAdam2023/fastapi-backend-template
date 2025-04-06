"""
@Time ： 2025-04-05
@Auth ： Adam Lyu
"""
# app/exceptions/base.py

from fastapi import HTTPException
from typing import Optional


class BusinessException(HTTPException):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(
            status_code=status_code,
            detail={
                "code": code,
                "message": message
            }
        )
