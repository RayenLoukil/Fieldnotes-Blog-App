from sqlalchemy import Integer , String , Text , DateTime, ForeignKey
from sqlalchemy.orm import Mapped , mapped_column, relationship
from database import Base

from datetime import datetime,timezone,timedelta

UTC_PLUS_1 = timezone(timedelta(hours=1))

class Post(Base):
    __tablename__ = "posts"
    
    id : Mapped[int] = mapped_column (Integer , primary_key=True , index=True)
    title:Mapped[str] = mapped_column(String(100) , nullable=False)
    content:Mapped[str] = mapped_column(Text , nullable=False)
    id_user : Mapped[int] = mapped_column (Integer, ForeignKey("users.id"))
    created_at :Mapped[datetime] = mapped_column(DateTime(timezone=True) , default=lambda: datetime.now(UTC_PLUS_1))
    user : Mapped["User"] = relationship(back_populates="posts")
    
    
class User(Base):
    __tablename__ = "users"
    
    id : Mapped[int] = mapped_column (Integer , primary_key=True , index=True)
    username : Mapped[str] = mapped_column (String(50) , unique=True)
    email : Mapped[str] = mapped_column (String(100) , unique=True)

    posts : Mapped[list[Post]] = relationship(back_populates="user")