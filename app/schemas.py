from datetime import datetime
from pydantic import BaseModel


# schema validation using pydantic
class PostBase(BaseModel):
    title: str  # mandatory
    content: str  # mandatory
    published: bool = True  # default value


class PostCreate(
    PostBase
):  # use a class to specifically create a post taking PostBase as parent
    pass


# A response model is defined
class ResponsePost(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
