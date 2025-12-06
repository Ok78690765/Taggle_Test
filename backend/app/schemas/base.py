"""Base schema for Pydantic models"""
from datetime import datetime

from pydantic import BaseModel as PydanticBaseModel, ConfigDict


class BaseSchema(PydanticBaseModel):
    """Base schema with common fields"""

    model_config = ConfigDict(from_attributes=True)


class ItemSchema(BaseSchema):
    """Item schema"""

    id: int | None = None
    name: str
    description: str = ""
    created_at: datetime | None = None
    updated_at: datetime | None = None
