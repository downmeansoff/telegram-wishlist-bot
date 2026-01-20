from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Category(Base):
    """Category model for wishes"""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    emoji = Column(String(10), nullable=True)
    color = Column(String(7), default="#3B82F6")  # Hex color
    description = Column(String(500), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    wishes = relationship("Wish", back_populates="category")

    def __repr__(self):
        return f"<Category {self.name}>"
