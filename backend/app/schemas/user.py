from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""
    username: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    language_code: str = "ru"
    birthday: Optional[datetime] = None


class UserCreate(UserBase):
    """User creation schema"""
    telegram_id: int


class UserUpdate(BaseModel):
    """User update schema"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    birthday: Optional[datetime] = None
    language_code: Optional[str] = None


class User(UserBase):
    """User response schema"""
    id: int
    telegram_id: int
    is_active: bool
    is_premium: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    @property
    def full_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name


class UserProfile(User):
    """Extended user profile with statistics"""
    wishes_count: int = 0
    completed_wishes_count: int = 0
    groups_count: int = 0
