from sqlalchemy import (
    Column, BigInteger, Integer, String, Text, Numeric,
    DateTime, Boolean, ForeignKey, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class WishStatus(str, enum.Enum):
    """Wish status enum"""
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class WishPriority(int, enum.Enum):
    """Wish priority enum"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


class Wish(Base):
    """Wish model"""
    __tablename__ = "wishes"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    link = Column(String, nullable=True)

    price = Column(Numeric(10, 2), nullable=True)
    currency = Column(String(3), default="RUB")

    priority = Column(Integer, default=WishPriority.MEDIUM.value)
    status = Column(
        SQLEnum(WishStatus),
        default=WishStatus.ACTIVE,
        nullable=False,
        index=True
    )

    # Order for drag & drop
    order_index = Column(Integer, default=0)

    # Metadata
    is_public = Column(Boolean, default=True)
    notes = Column(Text, nullable=True)  # Private notes

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="wishes")
    category = relationship("Category", back_populates="wishes")
    reservations = relationship(
        "Reservation",
        back_populates="wish",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Wish {self.id} - {self.title}>"

    @property
    def is_reserved(self) -> bool:
        """Check if wish is reserved"""
        return len(self.reservations) > 0

    @property
    def formatted_price(self) -> str:
        """Get formatted price with currency"""
        if self.price:
            currency_symbols = {
                "RUB": "₽",
                "USD": "$",
                "EUR": "€",
            }
            symbol = currency_symbols.get(self.currency, self.currency)
            return f"{self.price} {symbol}"
        return "Не указана"
