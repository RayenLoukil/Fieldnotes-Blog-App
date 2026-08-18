from fastapi import HTTPException, status, APIRouter, Query
from typing import Annotated

## models + schemas + database
from schemas import PostCreate, PostResponse, PostUpdate, PaginatedPostResponse
import models
from database import get_db

## Dependency injection for database session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

#Authorization
from auth import CurrentUser

#---------------

router = APIRouter()


# ---------------------------------------------------------
# GET all posts
# Public — no authentication required
# Anyone can read the feed
# ---------------------------------------------------------

@router.get("", response_model=PaginatedPostResponse)
async def get_posts(db: Annotated[AsyncSession, Depends(get_db)],
                skip: Annotated[int, Query(ge=0)] = 0,
                limit: Annotated[int, Query(ge=1, le=100)] = 10,):
    
    total_result = await db.execute(
        select(func.count()).select_from(models.Post)
    )
    total = total_result.scalar() or 0
    
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.user))
        .order_by(models.Post.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    posts = result.scalars().all()
    
    has_more = (skip + len(posts)) < total
    
    return PaginatedPostResponse(
        posts=[PostResponse.model_validate(post) for post in posts],
        total=total,
        skip=skip,
        limit=limit,
        has_more=has_more,
    )


# ---------------------------------------------------------
# GET /{id} — get a single post
# Public — no authentication required
# ---------------------------------------------------------
@router.get("/{id}", response_model=PostResponse)
async def get_post(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.user))
        .where(models.Post.id == id)
    )
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


# ---------------------------------------------------------
# POST — create a post
# Protected — requires valid JWT
# id_user comes from the token, NOT the request body
# ---------------------------------------------------------
@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    new_post = models.Post(
        title=post.title,
        content=post.content,
        id_user=current_user.id,
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post


# ---------------------------------------------------------
# PATCH /{id} — update a post
# Protected — requires valid JWT
# Ownership check — you can only edit your own posts
# ---------------------------------------------------------
@router.patch("/{id}", response_model=PostResponse)
async def update_post(
    id: int,
    updated_post: PostUpdate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(models.Post).where(models.Post.id == id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if post.id_user != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post"
        )

    update_data = updated_post.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)

    await db.commit()
    await db.refresh(post)
    return post


# ---------------------------------------------------------
# DELETE /{id} — delete a post
# Protected — requires valid JWT
# Ownership check — you can only delete your own posts
# ---------------------------------------------------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(models.Post).where(models.Post.id == id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if post.id_user != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )

    await db.delete(post)
    await db.commit()