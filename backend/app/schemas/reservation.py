from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class ReservationBase(BaseModel):
    """Base reservation schema"""
    notes: Optional[str] = None


class ReservationCreate(ReservationBase):
    """Reservation creation schema"""
    wish_id: int
    group_id: int


class Reservation(ReservationBase):
    """Reservation response schema"""
    id: int
    wish_id: int
    group_id: int
    reserved_by: int
    reserved_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReservationWithDetails(Reservation):
    """Reservation with wish and user details"""
    wish_title: str
    wish_image_url: Optional[str] = None
    user_name: str
