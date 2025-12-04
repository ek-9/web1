import datetime
from pydantic import BaseModel
from controller import userController
from fastapi import APIRouter, HTTPException, status

class Reply(BaseModel):
    user_id: int
    content: str
    created: datetime.datetime = datetime.datetime.now()

class Post(BaseModel):
    post_id: int
    title: str
    content: str
    author: int
    # image: str
    liked: int
    view: int
    reply: Reply
    created: datetime.datetime = datetime.datetime.now()

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




POST_ID_GLOBAL = 0
REPLY_ID_GLOBAL = 0

post_list = dict()
'''
post_list 0 -> [post, content]
'''

def find_all_post() :
    return None


def createPost(req: PostRequest) :
    global POST_ID_GLOBAL
    if req.title == "" or req.title is None :
        raise HTTPException(status_code=401, detail="제목을 입력해주세요")
    POST_ID_GLOBAL += 1
    post = Post(
        post_id=POST_ID_GLOBAL,
        title=req.title,
        content=req.content,
        author=req.author,
        created=datetime.datetime.now(),
        liked=0,
        view=0
        # reply=[]
    )
    post_list[POST_ID_GLOBAL] = post
    return POST_ID_GLOBAL

def detailPost(p_id: int) :
    if p_id not in post_list:
        raise HTTPException(status_code=400, detail="error")
    return post_list[p_id]


def editPost(req: PostEditRequest, post_id: int):
    if post_id not in post_list:
        raise HTTPException(status_code=404, detail="Post not found")
    post_list[post_id].title = req.title
    post_list[post_id].content = req.content
    return post_id


def createReply(req: Reply, post_id: int):
    if post_id not in post_list:
        raise HTTPException(status_code=404, detail="Post not found")
    rep = Reply(
        user_id = req.user_id,
        content = req.content
    )
    post_list[post_id].reply.append(rep)
    return post_id

def deletePost(post_id: int):
    if post_id in post_list:
        del post_list[post_id]
        return True
    raise HTTPException(status_code=404, detail="Post not found")

