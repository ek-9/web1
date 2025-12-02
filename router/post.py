from fastapi import FastAPI, APIRouter
from controller import userController
from controller import postController

router = APIRouter()

@router.post("/post")
def create(req: postController.PostRequest) :
    post_id = postController.createPost(req)
    return {"post_id" : post_id}

@router.get("/posts")
def list() :
    return list(postController.post_list.values())


@router.patch("/edit/{post_id}")
def edit(req: postController.PostEditRequest, post_id: int) :
    post_id = postController.editPost(req, post_id)
    return {"post_id" : post_id}

@router.delete("/delete/{post_id}")
def delete(post_id: int):
    return postController.deletePost(post_id)

@router.post("/posts/{post_id}/reply")
def create_reply(post_id: int, req: postController.Reply):
    post_id = postController.createReply(req, post_id)
    return {"post_id": post_id, "message": "reply created"}
