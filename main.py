from fastapi import FastAPI , HTTPException, status

## models + schemas + database
from schemas import PostCreate , PostResponse, PostUpdate , UserCreate, UserResponse
import models 
from database import get_db , engine , Base

## Dependency injection for database session
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

## Create the database tables
Base.metadata.create_all(bind=engine)

## Initialize the FastAPI app
app = FastAPI(
    title="Fieldnotes API",
    description="A Blog API for posting about tech and sharing knowledge",
    version="1.0.0",
)

@app.get("/")
def health_check():
    return {"message" : "ok"}

#get all posts
@app.get("/api/posts" , response_model=list[PostResponse])
def get_posts(db:Annotated[Session , Depends(get_db)]):
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return posts

#get post by id
@app.get("/api/posts/{id_post}" , response_model=PostResponse)
def get_post(id_post:int , db:Annotated[Session , Depends(get_db)]):
    result = db.execute(select(models.Post).where(models.Post.id==id_post))
    post = result.scalars().first()
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post
        
#create post
@app.post("/api/posts" , response_model=PostResponse)
def create_post(post : PostCreate  , db:Annotated[Session , Depends(get_db)]):
    new_post = models.Post(title=post.title , content=post.content , id_user=post.id_user  )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#update post
@app.patch("/api/posts/{id}" , response_model=PostResponse)
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
@app.delete("/api/posts/{id}" )
def delete_post(id:int , db: Annotated[Session , Depends(get_db)]):
    result = db.execute(select(models.Post).where(models.Post.id == id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    db.delete(post)
    db.commit()
    return {"message":"post deleted successfully"}



# get all users
@app.get("/api/users" ,  response_model=list[UserResponse])
def get_users(db : Annotated[Session , Depends(get_db)]):
    result = db.execute(select(models.User))
    users = result.scalars().all()
    return users    

# get user by id 
@app.get("/api/users/{id}" ,  response_model=UserResponse)
def get_user_by_id(id:int , db : Annotated[Session , Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id ==id ))
    user = result.scalars().first()
    if user:
        return user
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

#create a user
@app.post("/api/users" , response_model=UserResponse)
def create_user(user:UserCreate , db : Annotated[Session , Depends(get_db)]):
    new_user= models.User(username = user.username , email = user.email )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


