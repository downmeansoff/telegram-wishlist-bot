from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime


class NotificationBase(BaseModel):
    """Base notification schema"""
    type: str
    title: str
    message: str
    data: Optional[dict[str, Any]] = None


class NotificationCreate(NotificationBase):
    """Notification creation schema"""
    user_id: int


class Notification(NotificationBase):
    """Notification response schema"""
    id: int
    user_id: int
    is_read: bool
    read_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
