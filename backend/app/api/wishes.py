from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List
import logging

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.wish import Wish, WishStatus
from app.schemas.wish import (
    Wish as WishSchema,
    WishCreate,
    WishUpdate,
    WishListResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=WishListResponse)
async def get_wishes(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: WishStatus = Query(WishStatus.ACTIVE),
    category_id: int = Query(None),
    search: str = Query(None),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get user's wishes with pagination"""

    # Build query
    query = select(Wish).where(
        and_(
            Wish.user_id == current_user.id,
            Wish.status == status
        )
    )

    # Add filters
    if category_id:
        query = query.where(Wish.category_id == category_id)

    if search:
        query = query.where(
            Wish.title.ilike(f"%{search}%")
        )

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await session.execute(count_query)
    total = total_result.scalar()

    # Add pagination and ordering
    query = query.order_by(
        Wish.priority.desc(),
        Wish.order_index.asc(),
        Wish.created_at.desc()
    )
    query = query.offset((page - 1) * page_size).limit(page_size)

    # Execute query
    result = await session.execute(query)
    wishes = result.scalars().all()

    return WishListResponse(
        items=wishes,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get("/{wish_id}", response_model=WishSchema)
async def get_wish(
    wish_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Get single wish"""
    result = await session.execute(
        select(Wish).where(
            and_(
                Wish.id == wish_id,
                Wish.user_id == current_user.id
            )
        )
    )
    wish = result.scalar_one_or_none()

    if not wish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wish not found"
        )

    return wish


@router.post("/", response_model=WishSchema, status_code=status.HTTP_201_CREATED)
async def create_wish(
    wish_in: WishCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Create new wish"""
    logger.info(f"Creating wish for user {current_user.id}: {wish_in.title}")

    try:
        wish = Wish(
            **wish_in.model_dump(),
            user_id=current_user.id
        )

        session.add(wish)
        await session.commit()
        await session.refresh(wish)

        logger.info(f"Wish created successfully: {wish.id}")
        return wish
    except Exception as e:
        logger.error(f"Error creating wish: {e}", exc_info=True)
        raise


@router.put("/{wish_id}", response_model=WishSchema)
async def update_wish(
    wish_id: int,
    wish_in: WishUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Update wish"""
    result = await session.execute(
        select(Wish).where(
            and_(
                Wish.id == wish_id,
                Wish.user_id == current_user.id
            )
        )
    )
    wish = result.scalar_one_or_none()

    if not wish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wish not found"
        )

    # Update fields
    update_data = wish_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(wish, field, value)

    await session.commit()
    await session.refresh(wish)

    return wish


@router.delete("/{wish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wish(
    wish_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Delete wish"""
    result = await session.execute(
        select(Wish).where(
            and_(
                Wish.id == wish_id,
                Wish.user_id == current_user.id
            )
        )
    )
    wish = result.scalar_one_or_none()

    if not wish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wish not found"
        )

    await session.delete(wish)
    await session.commit()


@router.patch("/{wish_id}/complete", response_model=WishSchema)
async def complete_wish(
    wish_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Mark wish as completed"""
    result = await session.execute(
        select(Wish).where(
            and_(
                Wish.id == wish_id,
                Wish.user_id == current_user.id
            )
        )
    )
    wish = result.scalar_one_or_none()

    if not wish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wish not found"
        )

    wish.status = WishStatus.COMPLETED
    await session.commit()
    await session.refresh(wish)

    return wish
