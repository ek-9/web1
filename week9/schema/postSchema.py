from pydantic import BaseModel

class ReplyRequest(BaseModel) :
    user_id: int
    post_id: int
    content: str

class PostDetails(BaseModel) :
    title: str
    content: str

class PostRequest(BaseModel):
    title: str
    content: str
    author: int

class PostEditRequest(BaseModel):
    title: str
    content: str