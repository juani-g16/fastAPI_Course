from datetime import datetime
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
        orm_mode = True


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
        orm_mode = True


# validation of login token
class Token(BaseModel):
    access_token: str
    token_type: str


# validation of login token data
class TokenData(BaseModel):
    id: Optional[int] = None
