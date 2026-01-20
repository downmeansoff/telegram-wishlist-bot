from sqlalchemy import Column, BigInteger, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Reservation(Base):
    """Reservation model - when someone reserves a gift"""
    __tablename__ = "reservations"

    id = Column(BigInteger, primary_key=True, index=True)
    wish_id = Column(BigInteger, ForeignKey("wishes.id"), nullable=False, index=True)
    group_id = Column(BigInteger, ForeignKey("groups.id"), nullable=False, index=True)
    reserved_by = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)

    notes = Column(Text, nullable=True)  # Private notes for the person reserving

    reserved_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    wish = relationship("Wish", back_populates="reservations")
    group = relationship("Group", back_populates="reservations")
    reserved_by_user = relationship("User", back_populates="reservations")

    def __repr__(self):
        return f"<Reservation wish={self.wish_id} by={self.reserved_by}>"
