from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.group import Group, GroupMember, GroupRole
from app.models.wish import Wish, WishStatus
from app.schemas.group import (
    Group as GroupSchema,
    GroupCreate,
    GroupUpdate,
    GroupWithMembers,
    GroupMember as GroupMemberSchema,
)

router = APIRouter()


@router.get("/", response_model=list[GroupWithMembers])
async def get_groups(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get user's groups"""
    result = await session.execute(
        select(Group)
        .join(GroupMember)
        .where(GroupMember.user_id == current_user.id)
        .order_by(Group.created_at.desc())
    )
    groups = result.scalars().all()

    # Add member count
    groups_with_members = []
    for group in groups:
        groups_with_members.append(
            GroupWithMembers(
                **group.__dict__,
                member_count=len(group.members)
            )
        )

    return groups_with_members


@router.get("/{group_id}", response_model=GroupSchema)
async def get_group(
    group_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get group details"""
    # Check if user is member
    result = await session.execute(
        select(GroupMember).where(
            and_(
                GroupMember.group_id == group_id,
                GroupMember.user_id == current_user.id
            )
        )
    )
    membership = result.scalar_one_or_none()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this group"
        )

    # Get group
    result = await session.execute(
        select(Group).where(Group.id == group_id)
    )
    group = result.scalar_one_or_none()

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )

    return group


@router.post("/", response_model=GroupSchema, status_code=status.HTTP_201_CREATED)
async def create_group(
    group_in: GroupCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Create new group"""
    group = Group(
        **group_in.model_dump(),
        creator_id=current_user.id
    )

    session.add(group)
    await session.flush()

    # Add creator as owner
    membership = GroupMember(
        group_id=group.id,
        user_id=current_user.id,
        role=GroupRole.OWNER
    )
    session.add(membership)

    await session.commit()
    await session.refresh(group)

    return group


@router.put("/{group_id}", response_model=GroupSchema)
async def update_group(
    group_id: int,
    group_in: GroupUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Update group (owner/admin only)"""
    # Check permissions
    result = await session.execute(
        select(GroupMember).where(
            and_(
                GroupMember.group_id == group_id,
                GroupMember.user_id == current_user.id,
                GroupMember.role.in_([GroupRole.OWNER, GroupRole.ADMIN])
            )
        )
    )
    membership = result.scalar_one_or_none()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this group"
        )

    # Get group
    result = await session.execute(
        select(Group).where(Group.id == group_id)
    )
    group = result.scalar_one_or_none()

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )

    # Update fields
    update_data = group_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(group, field, value)

    await session.commit()
    await session.refresh(group)

    return group


@router.post("/{group_id}/join", response_model=GroupMemberSchema)
async def join_group(
    group_id: int,
    invite_code: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Join group by invite code"""
    # Get group
    result = await session.execute(
        select(Group).where(
            and_(
                Group.id == group_id,
                Group.invite_code == invite_code
            )
        )
    )
    group = result.scalar_one_or_none()

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found or invalid invite code"
        )

    # Check if already member
    result = await session.execute(
        select(GroupMember).where(
            and_(
                GroupMember.group_id == group_id,
                GroupMember.user_id == current_user.id
            )
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already a member of this group"
        )

    # Add member
    membership = GroupMember(
        group_id=group_id,
        user_id=current_user.id,
        role=GroupRole.MEMBER
    )
    session.add(membership)
    await session.commit()
    await session.refresh(membership)

    return membership


@router.get("/{group_id}/members", response_model=list[GroupMemberSchema])
async def get_group_members(
    group_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get group members"""
    # Check if user is member
    result = await session.execute(
        select(GroupMember).where(
            and_(
                GroupMember.group_id == group_id,
                GroupMember.user_id == current_user.id
            )
        )
    )
    membership = result.scalar_one_or_none()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this group"
        )

    # Get all members
    result = await session.execute(
        select(GroupMember).where(GroupMember.group_id == group_id)
    )
    members = result.scalars().all()

    return members


@router.get("/{group_id}/wishes", response_model=list)
async def get_group_wishes(
    group_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get wishes of all group members"""
    # Check if user is member
    result = await session.execute(
        select(GroupMember).where(
            and_(
                GroupMember.group_id == group_id,
                GroupMember.user_id == current_user.id
            )
        )
    )
    membership = result.scalar_one_or_none()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this group"
        )

    # Get all member IDs
    result = await session.execute(
        select(GroupMember.user_id).where(GroupMember.group_id == group_id)
    )
    member_ids = result.scalars().all()

    # Get wishes
    result = await session.execute(
        select(Wish).where(
            and_(
                Wish.user_id.in_(member_ids),
                Wish.status == WishStatus.ACTIVE,
                Wish.is_public == True
            )
        ).order_by(Wish.priority.desc(), Wish.created_at.desc())
    )
    wishes = result.scalars().all()

    return wishes
