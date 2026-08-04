from fastapi import HTTPException, status, APIRouter

## models + schemas + database
from schemas import  UserCreate, UserResponse , UserUpdate
import models 
from database import get_db 

## Dependency injection for database session
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select



router = APIRouter(
    
)


# get all users
@router.get("" ,  response_model=list[UserResponse])
def get_users(db : Annotated[Session , Depends(get_db)]):
    result = db.execute(select(models.User))
    users = result.scalars().all()
    return users    

# get user by id 
@router.get("/{id}" ,  response_model=UserResponse)
def get_user_by_id(id:int , db : Annotated[Session , Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id ==id ))
    user = result.scalars().first()
    if user:
        return user
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

#create a user
@router.post("" , response_model=UserResponse , status_code=status.HTTP_201_CREATED)
def create_user(user:UserCreate , db : Annotated[Session , Depends(get_db)]):
    existing = db.execute(
        select(models.User).where(
            (models.User.username == user.username) | (models.User.email == user.email)
        )
    ).scalars().first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    new_user = models.User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#update a user
@router.patch("/{id}", response_model=UserResponse)
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





