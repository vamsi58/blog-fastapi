from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DATETIME, BigInteger, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    mobile = Column(String(15), nullable=False)
    registered_at = Column(DateTime, nullable=False)
    last_login = Column(DateTime)
    intro = Column(String(500), nullable=False)
    profile = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True)

    posts = relationship("Post", back_populates="author")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(75), nullable=False)
    content = Column(String(500), index=True)
    summary = Column(String(50), index=True)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")
