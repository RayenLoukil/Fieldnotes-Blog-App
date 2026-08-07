from fastapi import HTTPException, status, APIRouter

## models + schemas + database
from schemas import  UserCreate, UserPrivate  , UserPublic , UserUpdate
import models 
from database import get_db 

## Dependency injection for database session
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

# Authentication
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, select
from auth import hash_password, create_access_token, verify_password 
from config import settings
from schemas import Token


# Authorization 
from  auth import CurrentUser
#------------


router = APIRouter()




# ---------------------------------------------------------
# GET all users
# Public — no authentication required
# Anyone can browse the author list
# ---------------------------------------------------------
@router.get("", response_model=list[UserPublic])
def get_users(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User))
    users = result.scalars().all()
    return users


# ---------------------------------------------------------
# GET /me  — must come before /{id} to avoid path conflict
# Protected — requires valid JWT
# Returns the full private profile of whoever is logged in
# Collapsed from ~20 lines to 3 using CurrentUser dependency
# ---------------------------------------------------------
@router.get("/me", response_model=UserPrivate)
def get_me(current_user: CurrentUser):
    # get_current_user already did all the work:
    # extracted the token, verified it, fetched the user from the DB
    # we just return what it gave us
    return current_user


# ---------------------------------------------------------
# GET /{id}
# Public — no authentication required
# Returns the public profile of any author
# NOTE: defined AFTER /me to avoid "me" being treated as an integer ID
# ---------------------------------------------------------
@router.get("/{id}", response_model=UserPublic)
def get_user_by_id(id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


# ---------------------------------------------------------
# POST  — register a new user
# Public — no authentication required (you can't log in before registering)
# Returns UserPrivate so the new user sees their own email
# ---------------------------------------------------------
@router.post("", response_model=UserPrivate, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    existing = db.execute(
        select(models.User).where(
            (func.lower(models.User.username) == user.username.lower())
            | (func.lower(models.User.email) == user.email.lower())
        )
    ).scalars().first()

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
    db.commit()
    db.refresh(new_user)
    return new_user


# ---------------------------------------------------------
# POST /token — login
# Public — this IS the authentication endpoint
# Accepts form-urlencoded data (OAuth2PasswordRequestForm)
# Returns a JWT access token on success
# ---------------------------------------------------------
@router.post("/token", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    # OAuth2PasswordRequestForm uses "username" field — we treat it as email
    result = db.execute(
        select(models.User).where(
            func.lower(models.User.email) == form_data.username.lower()
        )
    )
    user = result.scalars().first()

    # Deliberately identical error for wrong email AND wrong password
    # Never reveal which one was incorrect — prevents account enumeration
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
# Ownership check — you can only update your own account
# Returns UserPrivate so the user sees their updated email
# ---------------------------------------------------------
@router.patch("/{id}", response_model=UserPrivate)
def update_user(
    id: int,
    user_update: UserUpdate,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    # Ownership check
    # 401 = not logged in at all
    # 403 = logged in but not the owner of this resource
    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )

    result = db.execute(select(models.User).where(models.User.id == id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user_update.username is not None and user_update.username.lower() != user.username.lower():
        existing = db.execute(
            select(models.User).where(
                func.lower(models.User.username) == user_update.username.lower()
            )
        ).scalars().first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )

    if user_update.email is not None and user_update.email.lower() != user.email.lower():
        existing = db.execute(
            select(models.User).where(
                func.lower(models.User.email) == user_update.email.lower()
            )
        ).scalars().first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "email" and value is not None:
            value = value.lower()
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


# ---------------------------------------------------------
# DELETE /{id} — delete a user's own account
# Protected — requires valid JWT
# Ownership check — you can only delete your own account
# Cascade in models.py handles deleting all their posts too
# ---------------------------------------------------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: int,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    # Ownership check
    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
        )

    result = db.execute(select(models.User).where(models.User.id == id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(user)
    db.commit()