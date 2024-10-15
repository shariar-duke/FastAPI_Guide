from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    user_id: int
    created_at: datetime
    owner: UserOut

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# for createing vote
class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)  # type: ignore

    class Config:
        orm_mode = True


# New schema to combine Post and Vote
class PostOut(BaseModel):
    post: Post
    vote_count: int

    class Config:
        orm_mode = True
