from typing import Optional

from pydantic import BaseModel


class Comment(BaseModel):
    user_id: int
    post_id: int
    comment: str

    class Config:
        orm_mode = True

