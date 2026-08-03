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
    created_at : datetime  = Field(default_factory=datetime.now)
    