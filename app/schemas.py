from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# validation of user login data
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# schema validation using pydantic
class PostBase(BaseModel):
    title: str  # mandatory
    content: str  # mandatory
    published: bool = True  # default value


class PostCreate(
    PostBase
):  # use a class to specifically create a post taking PostBase as parent
    pass


# A response model is defined, derived from PostBase
class ResponsePost(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: ResponsePost
    votes: int

    class Config:
        from_attributes = True


# validation of login token
class Token(BaseModel):
    access_token: str
    token_type: str


# validation of login token data
class TokenData(BaseModel):
    id: Optional[int] = None


# Validation for voting system
class Vote(BaseModel):
    class votedir(Enum):
        add_vote: int = 1
        sub_vote: int = 0

    post_id: int
    dir: votedir
