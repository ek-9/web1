from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, status
from controller import userController

'''
HTTPException : 에러를 발생시켜 FastAPI에게 알아서 에러 응답을 만들라고 하는 것/ 에러 상황을 명확히 알림
JSONResponse : 원하는 JSON을 직접 만들어 반환하는 것/ 성공 실패 여부와 상관없이 응답 직접 반영
'''

'''
Users
1. 회원가입
2. 로그인
3. 유저 정보 수정
4. 유저 정보 삭제
'''

router = APIRouter(prefix="/users")


'''
return : user_id
200 : 회원가입 성공
400 : 중복된 이메일 
401 : 이메일 or 비밀번호 null
'''
@router.post("/create")
def createUser(request: userController.UserRequest):
    user_id = userController.createUser(request)
    # return user_id
    return {"user_id": user_id}


'''
200 : 정상 응답
400 : 이메일 틀림
401 : 비밀번호 틀림
'''
@router.post("/login", responses={
    200 : {"description" : "success"},
    400 : {"description" : "wrong request"}
})
def loginUser(request: userController.loginUserRequest):
    user_id = userController.loginUser(request)
    return {"user_id": user_id}


@router.patch("/edit/{user_id}")
def editUser(user_id: int, request: userController.EditUserRequest):
    editUser_id = userController.editUser(user_id, request)
    return {"user_id": editUser_id}


@router.delete("/delete/{user_id}")
def deleteUser(user_id: int):
    userController.deleteUser(user_id)
    return {"status": "deleted"}









