from fastapi import FastAPI , HTTPException, status

## models + schemas + database
from schemas import PostCreate , PostResponse, PostUpdate , UserCreate, UserResponse , UserUpdate
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
@app.post("/api/posts" , response_model=PostResponse , status_code=status.HTTP_201_CREATED)
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
@app.delete("/api/posts/{id}", status_code=status.HTTP_204_NO_CONTENT )
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
@app.post("/api/users" , response_model=UserResponse , status_code=status.HTTP_201_CREATED)
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
@app.patch("/api/users/{id}", response_model=UserResponse)
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
@app.delete("/api/users/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int , db: Annotated[Session , Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    
    db.delete(user)
    db.commit()
    return {"message":"user deleted successfully"}






#HTTP Exception Handler 
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import Request

#Validation Error Handler
from fastapi.exceptions import RequestValidationError 


# Global HTTP Exception Handler
@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request: Request, exception: StarletteHTTPException):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "error": {
                "message": exception.detail,
                "status_code": exception.status_code
            }
        }
    )


# Global Validation Error Handler
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "message": "Validation failed",
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "details": exception.errors()
            }
        }
    )


# Global Unexpected Error Handler
@app.exception_handler(Exception)
def global_exception_handler(request: Request, exception: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "Internal server error",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        }
    )
    
    
