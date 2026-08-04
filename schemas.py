from pydantic import BaseModel, EmailStr , Field, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    username:str = Field(min_length=3, max_length=50)
    email: EmailStr  = Field(max_length=120)
    
class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    
    
class UserUpdate(BaseModel):
    username: str | None = Field( default=None, min_length=3, max_length=50)
    email:str | None = Field( default=None, min_length=5, max_length=100)
    


class PostBase(BaseModel):
    title:str = Field(min_length=3 , max_length=100)
    content: str = Field(min_length=10)
    
class PostCreate(PostBase):
    id_user:int

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user: UserResponse
    created_at : datetime 

class PostUpdate(BaseModel):
    title: str | None = Field( default=None, min_length=3, max_length=100)
    content: str | None = Field( default=None, min_length=10)
    
    
