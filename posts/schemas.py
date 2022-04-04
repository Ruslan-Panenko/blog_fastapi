from typing import Optional, List

from pydantic import BaseModel

from comments.schemas import Comment
from users.schemas import UserOut


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    owner_id: int
    comments: List[Comment]

    class Config:
        orm_mode = True


