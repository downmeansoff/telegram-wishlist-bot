from pydantic import BaseModel, ConfigDict, HttpUrl
from typing import Optional
from datetime import datetime
from decimal import Decimal

from app.models.wish import WishStatus, WishPriority


class WishBase(BaseModel):
    """Base wish schema"""
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    link: Optional[str] = None
    price: Optional[Decimal] = None
    currency: str = "RUB"
    priority: int = WishPriority.MEDIUM.value
    category_id: Optional[int] = None
    is_public: bool = True
    notes: Optional[str] = None


class WishCreate(WishBase):
    """Wish creation schema"""
    pass


class WishUpdate(BaseModel):
    """Wish update schema"""
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    link: Optional[str] = None
    price: Optional[Decimal] = None
    currency: Optional[str] = None
    priority: Optional[int] = None
    category_id: Optional[int] = None
    status: Optional[WishStatus] = None
    is_public: Optional[bool] = None
    notes: Optional[str] = None
    order_index: Optional[int] = None


class Wish(WishBase):
    """Wish response schema"""
    id: int
    user_id: int
    status: WishStatus
    order_index: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class WishWithReservation(Wish):
    """Wish with reservation info"""
    is_reserved: bool = False
    reserved_by: Optional[int] = None
    reservation_notes: Optional[str] = None


class WishListResponse(BaseModel):
    """Wish list response with pagination"""
    items: list[Wish]
    total: int
    page: int
    page_size: int
    total_pages: int
