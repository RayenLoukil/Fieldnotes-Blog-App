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

#auth
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, select
from auth import hash_password, create_access_token, verify_access_token, oauth2_scheme, verify_password 
from config import settings
from schemas import Token

router = APIRouter()


# get all users
@router.get("" ,  response_model=list[UserPublic])
def get_users(db : Annotated[Session , Depends(get_db)]):
    result = db.execute(select(models.User))
    users = result.scalars().all()
    return users    


# create a user (register)
@router.post("", response_model=UserPrivate, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    existing = db.execute(
        select(models.User).where(
            (func.lower(models.User.username) == user.username.lower()) |
            (func.lower(models.User.email) == user.email.lower())
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



# login (issues a JWT)
@router.post("/token", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    # nOTE: OAuth2PasswordRequestForm calls the field "username", but we use it for email
    result = db.execute(
        select(models.User).where(func.lower(models.User.email) == form_data.username.lower())
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


# get currently logged-in user (used by frontend to check auth state)
@router.get("/me", response_model=UserPrivate)
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
):
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        user_id_int = int(user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    result = db.execute(select(models.User).where(models.User.id == user_id_int))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    return user


# get user by id 
@router.get("/{id}" ,  response_model=UserPublic)
def get_user_by_id(id:int , db : Annotated[Session , Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id ==id ))
    user = result.scalars().first()
    if user:
        return user
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")


#update a user
@router.patch("/{id}", response_model=UserPrivate)
def update_user(id: int, user_update: UserUpdate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user_update.username is not None and user_update.username != user.username:
        result = db.execute(
            select(models.User).where(models.User.username == user_update.username)
        )
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )

    if user_update.email is not None and user_update.email != user.email:
        result = db.execute(
            select(models.User).where(models.User.email == user_update.email)
        )
        existing_email = result.scalars().first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


#delete a user
@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int , db: Annotated[Session , Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    
    db.delete(user)
    db.commit()
    return {"message":"user deleted successfully"}





