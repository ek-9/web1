from fastapi import APIRouter
from week9.controller import postController

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

Restful API
1. 자원의 계층 구조를 URL로 표현
2. 같은 URL에 따라서도 요청방식에 따라 완전히 다른 기능 수행 가능

body(request)에는 변동되는 내용을 넣어서
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
def create_reply(post_id: int, req: postController.ReplyRequest):
    post_id = postController.createReply(req, post_id)
    return {"post_id": post_id, "message": "reply created"}

@router.patch("/details/{post_id}/reply/{r_id}")
def edit_reply(post_id: int, r_id:int, req: postController.ReplyRequest):
    r_id = postController.editReply(post_id, r_id, req)
    return r_id

@router.delete("/details/{post_id}/reply/{r_id}")
def delete_reply(post_id: int, r_id: int):
    postController.deleteReply(post_id, r_id)
    return

@router.post("/details/{post_id}/like")
def like(user_id: int, post_id:int) :
    return postController.increaseLiked(user_id, post_id)
