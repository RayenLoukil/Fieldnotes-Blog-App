from fastapi import FastAPI

## models + schemas + database
from schemas import PostCreate , PostResponse
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


@app.get("/api/posts" , response_model=list[PostResponse])
def get_posts(db:Annotated[Session , Depends(get_db)]):
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return posts


@app.post("/api/posts" , response_model=PostResponse)
def create_post(post : PostCreate  , db:Annotated[Session , Depends(get_db)]):
    new_post = models.Post(title=post.title , content=post.content , id_user=post.id_user  )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post