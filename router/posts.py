from fastapi import  HTTPException, status , APIRouter

## models + schemas + database
from schemas import PostCreate , PostResponse, PostUpdate 
import models 
from database import get_db 

## Dependency injection for database session
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select


router = APIRouter()

#get all posts
@router.get("" , response_model=list[PostResponse])
def get_posts(db:Annotated[Session , Depends(get_db)]):
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return posts

#get post by id
@router.get("/{id_post}" , response_model=PostResponse)
def get_post(id_post:int , db:Annotated[Session , Depends(get_db)]):
    result = db.execute(select(models.Post).where(models.Post.id==id_post))
    post = result.scalars().first()
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post
        
#create post
@router.post("" , response_model=PostResponse , status_code=status.HTTP_201_CREATED)
def create_post(post : PostCreate  , db:Annotated[Session , Depends(get_db)]):
    user = db.execute(select(models.User).where(models.User.id == post.id_user)).scalars().first()
    if not user:
        raise HTTPException(404, "User not found")
    
    new_post = models.Post(title=post.title , content=post.content , id_user=post.id_user  )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#update post
@router.patch("/{id}" , response_model=PostResponse)
def update_post(id:int , updated_post:PostUpdate , db:Annotated[Session , Depends(get_db)]):
    result = db.execute(select(models.Post).where(models.Post.id == id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    update_data = updated_post.model_dump(exclude_unset=True)
    for field,value in update_data.items():
        setattr(post , field , value)
        
    db.commit()
    db.refresh(post)
    return post

#delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT )
def delete_post(id:int , db: Annotated[Session , Depends(get_db)]):
    result = db.execute(select(models.Post).where(models.Post.id == id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    db.delete(post)
    db.commit()
    return {"message":"post deleted successfully"}

