from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

from app.models.group import GroupRole


class GroupBase(BaseModel):
    """Base group schema"""
    name: str
    description: Optional[str] = None
    avatar_url: Optional[str] = None


class GroupCreate(GroupBase):
    """Group creation schema"""
    pass


class GroupUpdate(BaseModel):
    """Group update schema"""
    name: Optional[str] = None
    description: Optional[str] = None
    avatar_url: Optional[str] = None


class Group(GroupBase):
    """Group response schema"""
    id: int
    creator_id: int
    invite_code: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class GroupWithMembers(Group):
    """Group with member count"""
    member_count: int = 0


class GroupMemberBase(BaseModel):
    """Base group member schema"""
    user_id: int
    role: GroupRole = GroupRole.MEMBER


class GroupMember(GroupMemberBase):
    """Group member response schema"""
    id: int
    group_id: int
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)


class GroupMemberWithUser(GroupMember):
    """Group member with user info"""
    user_name: str
    user_avatar: Optional[str] = None
