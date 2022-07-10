from typing import List, Union

from pydantic import BaseModel

import datetime


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    mobile: str
    registered_at: datetime.datetime
    intro: str
    profile: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    last_login: datetime.datetime = None

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    summary: str
    is_published: bool


class PostCreate(PostBase):
    author_id: int
    created_at: datetime.datetime


class PostUpdate(PostBase):
    updated_at: datetime.datetime


class Post(PostBase):
    id: int
    author_id: int
    updated_at: datetime.datetime = None
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class Response(BaseModel):
    message: str
