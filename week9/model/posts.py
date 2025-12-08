import datetime
from pydantic import BaseModel, Field

class Post(BaseModel):
    post_id: int
    title: str = Field(max_length=26)
    content: str
    author: int
    # image: str
    liked: int
    view: int
    reply: list = []
    created: datetime.datetime = Field(default_factory=datetime.datetime.now)
    content_image: str



class Reply(BaseModel):
    post_id: int
    reply_id: int
    user_id: int
    content: str
    created: datetime.datetime = Field(default_factory=datetime.datetime.now)