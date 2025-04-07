"""
@Time ： 2025-04-05
@Auth ： Adam Lyu
"""

# app/utils/pyobjectid.py

from bson import ObjectId
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from typing import Any


class PyObjectId(ObjectId):
    """Pydantic-compatible ObjectId with string representation"""

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            python_schema=core_schema.no_info_after_validator_function(cls.validate, core_schema.any_schema()),
            json_schema=core_schema.str_schema()
        )

    @classmethod
    def validate(cls, v: Any) -> "PyObjectId":
        if isinstance(v, ObjectId):
            return cls(str(v))  # 确保是 PyObjectId 类型
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return cls(v)  # 👈 返回 PyObjectId 而不是 ObjectId

    def __str__(self) -> str:
        return super().__str__()
