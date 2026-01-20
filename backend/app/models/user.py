from sqlalchemy import Column, BigInteger, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String, nullable=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    language_code = Column(String(10), default="ru")
    birthday = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    wishes = relationship("Wish", back_populates="user", cascade="all, delete-orphan")
    created_groups = relationship(
        "Group",
        back_populates="creator",
        foreign_keys="Group.creator_id"
    )
    group_memberships = relationship(
        "GroupMember",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    reservations = relationship(
        "Reservation",
        back_populates="reserved_by_user",
        cascade="all, delete-orphan"
    )
    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.telegram_id} - {self.first_name}>"

    @property
    def full_name(self) -> str:
        """Get full name"""
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    @property
    def mention(self) -> str:
        """Get Telegram mention"""
        if self.username:
            return f"@{self.username}"
        return self.full_name
