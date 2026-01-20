from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.wish import Wish, WishStatus
from app.models.group import GroupMember
from app.schemas.user import User as UserSchema, UserUpdate, UserProfile

router = APIRouter()


@router.get("/profile", response_model=UserProfile)
async def get_profile(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get current user profile with statistics"""

    # Get wishes count
    wishes_result = await session.execute(
        select(func.count(Wish.id)).where(Wish.user_id == current_user.id)
    )
    wishes_count = wishes_result.scalar()

    # Get completed wishes count
    completed_result = await session.execute(
        select(func.count(Wish.id)).where(
            Wish.user_id == current_user.id,
            Wish.status == WishStatus.COMPLETED
        )
    )
    completed_wishes_count = completed_result.scalar()

    # Get groups count
    groups_result = await session.execute(
        select(func.count(GroupMember.id)).where(
            GroupMember.user_id == current_user.id
        )
    )
    groups_count = groups_result.scalar()

    return UserProfile(
        **current_user.__dict__,
        wishes_count=wishes_count,
        completed_wishes_count=completed_wishes_count,
        groups_count=groups_count
    )


@router.put("/profile", response_model=UserSchema)
async def update_profile(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Update user profile"""

    # Update fields
    update_data = user_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)

    await session.commit()
    await session.refresh(current_user)

    return current_user


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_db),
):
    """Get public user info"""
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.get("/{user_id}/wishes", response_model=list)
async def get_user_wishes(
    user_id: int,
    session: AsyncSession = Depends(get_db),
):
    """Get public wishes of a user"""
    result = await session.execute(
        select(Wish).where(
            Wish.user_id == user_id,
            Wish.status == WishStatus.ACTIVE,
            Wish.is_public == True
        ).order_by(Wish.priority.desc(), Wish.created_at.desc())
    )
    wishes = result.scalars().all()

    return wishes
