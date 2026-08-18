from fastapi import  HTTPException, status , APIRouter, Query
from typing import Annotated

## models + schemas + database
from schemas import PostCreate , PostResponse, PostUpdate , PaginatedPostResponse
import models 
from database import get_db 

## Dependency injection for database session
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, func


#Authorization
from auth import CurrentUser

#---------------

router = APIRouter()


# ---------------------------------------------------------
# GET all posts
# Public — no authentication required
# Anyone can read the feed
# ---------------------------------------------------------
from sqlalchemy.orm import selectinload

@router.get("", response_model=PaginatedPostResponse)
def get_posts(  db: Annotated[Session, Depends(get_db)],
                skip: Annotated[int, Query(ge=0)] = 0,
                limit: Annotated[int, Query(ge=1, le=100)] = 10,):
    
    total_result = db.execute(
        select(func.count()).select_from(models.Post)
    )
    total = total_result.scalar() or 0
    
    result = db.execute(
        select(models.Post)
        .options(selectinload(models.Post.user))   # <-- eager load
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
def get_post(id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
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
# A client cannot fake being another user
# ---------------------------------------------------------
@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    # current_user.id is trusted because it came from our verified JWT
    # not from anything the client sent in the request body
    new_post = models.Post(
        title=post.title,
        content=post.content,
        id_user=current_user.id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# ---------------------------------------------------------
# PATCH /{id} — update a post
# Protected — requires valid JWT
# Ownership check — you can only edit your own posts
# 401 = not logged in
# 403 = logged in but not the post owner
# ---------------------------------------------------------
@router.patch("/{id}", response_model=PostResponse)
def update_post(
    id: int,
    updated_post: PostUpdate,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    result = db.execute(select(models.Post).where(models.Post.id == id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Ownership check
    # We compare the post's stored author ID to the authenticated user's ID
    if post.id_user != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post"
        )

    update_data = updated_post.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)

    db.commit()
    db.refresh(post)
    return post


# ---------------------------------------------------------
# DELETE /{id} — delete a post
# Protected — requires valid JWT
# Ownership check — you can only delete your own posts
# ---------------------------------------------------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    result = db.execute(select(models.Post).where(models.Post.id == id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Ownership check
    if post.id_user != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )

    db.delete(post)
    db.commit()