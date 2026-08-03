from pydantic import BaseModel , Field, ConfigDict
from datetime import datetime

class PostBase(BaseModel):
    title:str = Field(min_length=3 , max_length=100)
    content: str = Field(min_length=10)
    
class PostCreate(PostBase):
    id_user:int

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    id_user: int
    created_at : datetime 

class PostUpdate(BaseModel):
    title: str | None = Field( default=None, min_length=3, max_length=100)
    content: str | None = Field( default=None, min_length=3, max_length=100)
    
    
class UserBase(BaseModel):
    username:str = Field(min_length=3, max_length=50)
    email:str = Field(min_length=5, max_length=100)
    
class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
    
class UserUpdate(BaseModel):
    username: str | None = Field( default=None, min_length=3, max_length=50)
    email:str | None = Field( default=None, min_length=5, max_length=100)
    
