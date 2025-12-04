from fastapi import FastAPI, APIRouter
from controller import userController
from controller import postController


'''
Posts
1. 글 목록
2. 글 쓰기
3. 글 읽기
4. 글 수정
5. 글 삭제
6. 댓글 달기
7. 댓글 수정
8. 댓글 삭제
'''
router = APIRouter(prefix= "/post")

@router.get("/list")
def list() :
    return list(postController.post_list.values())

@router.post("/create")
def create(req: postController.PostRequest) :
    post_id = postController.createPost(req)
    return {"post_id" : post_id}


@router.get("/details/{post_id}")
def details(p_id: int):
    return postController.detailPost(p_id)


@router.patch("/edit/{post_id}")
def edit(req: postController.PostEditRequest, post_id: int) :
    post_id = postController.editPost(req, post_id)
    return {"post_id" : post_id}

@router.delete("/delete/{post_id}")
def delete(post_id: int):
    return postController.deletePost(post_id)

@router.post("/details/{post_id}/reply")
def create_reply(post_id: int, req: postController.Reply):
    post_id = postController.createReply(req, post_id)
    return {"post_id": post_id, "message": "reply created"}
