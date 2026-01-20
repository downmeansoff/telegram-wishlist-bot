from sqlalchemy import (
    Column, BigInteger, Integer, String, Text,
    DateTime, Boolean, ForeignKey, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import secrets

from app.core.database import Base


class GroupRole(str, enum.Enum):
    """Group member role enum"""
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class Group(Base):
    """Group model"""
    __tablename__ = "groups"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    avatar_url = Column(String, nullable=True)

    creator_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    invite_code = Column(
        String(16),
        unique=True,
        nullable=False,
        index=True,
        default=lambda: secrets.token_urlsafe(12)
    )

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    creator = relationship(
        "User",
        back_populates="created_groups",
        foreign_keys=[creator_id]
    )
    members = relationship(
        "GroupMember",
        back_populates="group",
        cascade="all, delete-orphan"
    )
    reservations = relationship(
        "Reservation",
        back_populates="group",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Group {self.id} - {self.name}>"

    @property
    def member_count(self) -> int:
        """Get member count"""
        return len(self.members)


class GroupMember(Base):
    """Group member model"""
    __tablename__ = "group_members"

    id = Column(BigInteger, primary_key=True, index=True)
    group_id = Column(BigInteger, ForeignKey("groups.id"), nullable=False, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)

    role = Column(
        SQLEnum(GroupRole),
        default=GroupRole.MEMBER,
        nullable=False
    )

    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    group = relationship("Group", back_populates="members")
    user = relationship("User", back_populates="group_memberships")

    def __repr__(self):
        return f"<GroupMember group={self.group_id} user={self.user_id}>"
