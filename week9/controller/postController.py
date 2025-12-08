import datetime
from pydantic import BaseModel, Field
from week9.controller import userController
from fastapi import HTTPException, UploadFile
from week9.model.posts import Post, Reply
from week9.schema.postSchema import ReplyRequest, PostEditRequest, PostDetails, PostRequest
import os


POST_ID_GLOBAL = 0
REPLY_ID_GLOBAL = 0

post_list = dict()
'''
post_list 0 -> [post, content]
'''

def find_all_post() :
    return list(post_list.values())


def createPost(req: PostRequest, content_image: UploadFile) :
    global POST_ID_GLOBAL
    if req.title == "" or req.title is None :
        raise HTTPException(status_code=401, detail="제목을 입력해주세요")
    POST_ID_GLOBAL += 1
    image_path = save_image(POST_ID_GLOBAL, content_image)
    post = Post(
        post_id=POST_ID_GLOBAL,
        title=req.title,
        content=req.content,
        author=req.author,
        created=Field(default_factory=datetime.now),
        liked=0,
        view=0,
        content_image = image_path,
        reply=[]
    )

    post_list[POST_ID_GLOBAL] = post
    return POST_ID_GLOBAL

def detailPost(p_id: int) :
    if p_id not in post_list:
        raise HTTPException(status_code=400, detail="error")
    return post_list[p_id]


def editPost(req: PostEditRequest, post_id: int, content_image: UploadFile):
    if post_id not in post_list:
        raise HTTPException(status_code=404, detail="Post not found")
    post_list[post_id].title = req.title
    post_list[post_id].content = req.content
    if content_image:
        image_path = save_image(post_id, content_image)
        post_list[post_id].content_image = image_path
    return post_id

def deletePost(post_id: int):
    if post_id in post_list:
        del post_list[post_id]
        return True
    raise HTTPException(status_code=404, detail="Post not found")



def createReply(req: ReplyRequest, post_id: int):
    if post_id not in post_list:
        raise HTTPException(status_code=404, detail="Post not found")
    if req.user_id not in userController.user_list :
        raise HTTPException(status_code=405, detail="User not found")
    idx = len(post_list[post_id].reply)

    new_reply = Reply(
        post_id = req.post_id,
        reply_id= idx,
        user_id = req.user_id,
        content = req.content
    )
    post_list[post_id].reply.append(new_reply)
    return post_id

def editReply(post_id: int, r_id: int, req: ReplyRequest):
    if post_id not in post_list :
        raise HTTPException(status_code=404, detail="Post not found")
    find_post = post_list[post_id]
    if req.content == "" or req.content is None :
        raise HTTPException(status_code=400, detail="내용을 작성해주세요.")
    find_post.reply[r_id].content = req.content
    return r_id

def deleteReply(post_id: int, r_id: int) :
    find_post = post_list[post_id]
    if r_id >= len(find_post.reply) :
        raise HTTPException(status_code=400, detail='서버오류')
    find_post.pop(r_id)
    return



# 좋아요, 조회수 로직
def increaseLiked(u_id: int, p_id:int) :
    '''
    같은 유저가 홀수번 누르면 좋아요 증가
    짝수번 누르면 다시 감소
    :return:
    '''
    status = 0
    idx = 0
    # 유저가 좋아요를 눌렀었는지 찾기
    findUser = userController.user_list[u_id]
    findPost = post_list[p_id]
    for pl in range(len(findUser.post_like)):
        if p_id == findUser.post_like[pl] :
            status = 1 # 이미 좋아요 누른경우
            idx = pl

    if status == 0 :
        findPost.liked += 1
        findUser.post_like.append(p_id)
    else :
        findPost.liked -= 1
        findUser.post_like.pop(idx)

    return p_id

UPLOAD_DIR = "static/content_images"

def save_image(post_id: int, file: UploadFile):
    if file is None:
        return None

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_ext = file.filename.split(".")[-1]
    filename = f"post_{post_id}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path  # 이 경로만 DB에 저장






