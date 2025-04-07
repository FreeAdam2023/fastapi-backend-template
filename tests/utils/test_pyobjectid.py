"""
@Time ： 2025-04-06
@Auth ： Adam Lyu
"""

import pytest
from pydantic import BaseModel, Field
from app.utils.pyobjectid import PyObjectId


def test_pyobjectid_conversion():
    oid = PyObjectId()
    assert isinstance(str(oid), str)
    assert len(str(oid)) == 24


def test_invalid_objectid_raises():
    with pytest.raises(ValueError):
        PyObjectId.validate("not_a_valid_id")


class ExampleModel(BaseModel):
    id: PyObjectId = Field(alias="_id")

    model_config = {
        "populate_by_name": True
    }


def test_pyobjectid_in_model():
    raw_data = {"_id": "507f1f77bcf86cd799439011"}
    model = ExampleModel.model_validate(raw_data)
    assert isinstance(model.id, PyObjectId)
    assert str(model.id) == "507f1f77bcf86cd799439011"
