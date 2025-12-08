import datetime
from pydantic import BaseModel, Field

class Post(BaseModel):
    post_id: int
    title: str
    content: str
    author: int
    # image: str
    liked: int
    view: int
    reply: dict
    created: datetime.datetime = Field(default_factory=datetime.datetime.now)



class Reply(BaseModel):
    post_id: int
    reply_id: int
    user_id: int
    content: str
    created: datetime.datetime = Field(default_factory=datetime.datetime.now)