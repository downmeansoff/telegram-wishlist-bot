from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class CategoryBase(BaseModel):
    """Base category schema"""
    name: str
    emoji: Optional[str] = None
    color: str = "#3B82F6"
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    """Category creation schema"""
    pass


class Category(CategoryBase):
    """Category response schema"""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
