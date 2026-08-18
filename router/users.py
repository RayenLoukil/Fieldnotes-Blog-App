from fastapi import HTTPException, status, APIRouter, Query

## models + schemas + database
from schemas import UserCreate, UserPrivate, UserPublic, UserUpdate, PaginatedPostResponse
import models
from database import get_db

## Dependency injection for database session
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

# Authentication
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from auth import hash_password, create_access_token, verify_password
from config import settings
from schemas import Token

# Authorization
from auth import CurrentUser

# Image upload
from fastapi import UploadFile
from PIL import UnidentifiedImageError
from image_utils import delete_profile_image, process_profile_image

#------------

router = APIRouter()


# ---------------------------------------------------------
# GET all users
# Public — no authentication required
# ---------------------------------------------------------
@router.get("", response_model=list[UserPublic])
async def get_users(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.User))
    users = result.scalars().all()
    return users


# ---------------------------------------------------------
# GET /me — must come before /{id} to avoid path conflict
# Protected — requires valid JWT
# ---------------------------------------------------------
@router.get("/me", response_model=UserPrivate)
def get_me(current_user: CurrentUser):
    return current_user


# ---------------------------------------------------------
# GET /{id}
# Public — no authentication required
# NOTE: defined AFTER /me to avoid "me" being treated as an integer ID
# ---------------------------------------------------------
@router.get("/{id}", response_model=UserPublic)
async def get_user_by_id(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.User).where(models.User.id == id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


# ---------------------------------------------------------
# GET /{id}/posts
# Public — no authentication required
# ---------------------------------------------------------
@router.get("/{id}/posts", response_model=PaginatedPostResponse)
async def get_user_posts(
    id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    from sqlalchemy.orm import selectinload
    import models as m
    from schemas import PostResponse

    total_result = await db.execute(
        select(func.count()).select_from(m.Post).where(m.Post.id_user == id)
    )
    total = total_result.scalar() or 0

    result = await db.execute(
        select(m.Post)
        .options(selectinload(m.Post.user))
        .where(m.Post.id_user == id)
        .order_by(m.Post.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    posts = result.scalars().all()

    has_more = skip + len(posts) < total

    return PaginatedPostResponse(
        posts=[PostResponse.model_validate(post) for post in posts],
        total=total,
        skip=skip,
        limit=limit,
        has_more=has_more,
    )


# ---------------------------------------------------------
# POST — register a new user
# Public — no authentication required
# ---------------------------------------------------------
@router.post("", response_model=UserPrivate, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.User).where(
            (func.lower(models.User.username) == user.username.lower())
            | (func.lower(models.User.email) == user.email.lower())
        )
    )
    existing = result.scalars().first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    new_user = models.User(
        username=user.username,
        email=user.email.lower(),
        password_hash=hash_password(user.password),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


# ---------------------------------------------------------
# POST /token — login
# Public — this IS the authentication endpoint
# ---------------------------------------------------------
@router.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(
        select(models.User).where(
            func.lower(models.User.email) == form_data.username.lower()
        )
    )
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    return {"access_token": access_token, "token_type": "bearer"}


# ---------------------------------------------------------
# PATCH /{id} — update a user's own profile
# Protected — requires valid JWT
# ---------------------------------------------------------
@router.patch("/{id}", response_model=UserPrivate)
async def update_user(
    id: int,
    user_update: UserUpdate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )

    result = await db.execute(select(models.User).where(models.User.id == id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user_update.username is not None and user_update.username.lower() != user.username.lower():
        existing_result = await db.execute(
            select(models.User).where(
                func.lower(models.User.username) == user_update.username.lower()
            )
        )
        if existing_result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )

    if user_update.email is not None and user_update.email.lower() != user.email.lower():
        existing_result = await db.execute(
            select(models.User).where(
                func.lower(models.User.email) == user_update.email.lower()
            )
        )
        if existing_result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "email" and value is not None:
            value = value.lower()
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user


# ---------------------------------------------------------
# DELETE /{id} — delete a user's own account
# Protected — requires valid JWT
# ---------------------------------------------------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
        )

    result = await db.execute(select(models.User).where(models.User.id == id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    await db.delete(user)
    await db.commit()


# ---------------------------------------------------------
# PATCH /{id}/picture — upload profile picture
# Protected — requires valid JWT
# ---------------------------------------------------------
@router.patch("/{id}/picture", response_model=UserPrivate)
async def upload_profile_picture(
    id: int,
    file: UploadFile,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if current_user.id != id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this user's picture"
        )

    content = file.file.read()
    if len(content) > settings.max_upload_size_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {settings.max_upload_size_bytes // (1024*1024)}MB",
        )

    try:
        new_filename = process_profile_image(content)
    except UnidentifiedImageError as err:
        raise HTTPException(status_code=400, detail="Invalid image file.") from err

    old_filename = current_user.image_file
    current_user.image_file = new_filename
    await db.commit()
    await db.refresh(current_user)

    if old_filename:
        delete_profile_image(old_filename)
    return current_user