from __future__ import annotations
from sqlalchemy import Integer , String , Text , DateTime, ForeignKey
from sqlalchemy.orm import Mapped , mapped_column, relationship
from database import Base
from datetime import datetime, UTC
from config import settings

class Post(Base):
    __tablename__ = "posts"
    
    id : Mapped[int] = mapped_column (Integer , primary_key=True , index=True)
    title:Mapped[str] = mapped_column(String(100) , nullable=False)
    content:Mapped[str] = mapped_column(Text , nullable=False)
    id_user : Mapped[int] = mapped_column (Integer, ForeignKey("users.id") , nullable=False, index=True)
    created_at :Mapped[datetime] = mapped_column(DateTime(timezone=True) , default=lambda: datetime.now(UTC))
    user : Mapped[User] = relationship(back_populates="posts")
    
    
class User(Base):
    __tablename__ = "users"
    
    id : Mapped[int] = mapped_column (Integer , primary_key=True , index=True)
    username : Mapped[str] = mapped_column (String(50) , unique=True)
    email : Mapped[str] = mapped_column (String(100) , unique=True)
    
    password_hash : Mapped[str] = mapped_column (String(200) , nullable=False)
    
    image_file: Mapped[str | None] = mapped_column(String(200), nullable=True, default=None)
    
    @property
    def image_path(self) -> str:
        if self.image_file:
            if settings.s3_endpoint_url:
                # MinIO / local S3-compatible: path-style URL
                return (
                    f"{settings.s3_endpoint_url}"
                    f"/{settings.s3_bucket_name}"
                    f"/profile_pics/{self.image_file}"
                )
            # Real AWS S3: virtual-hosted style URL
            return (
                f"https://{settings.s3_bucket_name}"
                f".s3.{settings.s3_region}"
                f".amazonaws.com/profile_pics/{self.image_file}"
            )
        return "/static/profile_pics/default.jpg"

    

    posts : Mapped[list[Post]] = relationship(back_populates="user" , cascade="all, delete-orphan")