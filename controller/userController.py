from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, HTTPException, status

class UserRequest(BaseModel) :
    email: EmailStr
    password: str
    nickname: str

class loginUserRequest(BaseModel) :
    email: EmailStr
    password: str

class EditUserRequest(BaseModel):
    user_id: int
    nickname: str


class User(BaseModel):
    '''
    email,
    password,
    nickname
    '''
    user_id: int
    email: EmailStr
    password: str
    nickname: str

user_list = dict()
USER_ID_GLOBAL = 0
'''
1. 회원가입
2. 로그인
'''

### Q
'''
USER DB 어떤자료형 쓸건지?
POST DB도 어떤 자료형 쓸건지??

'''



def createUser(userDao: UserRequest) -> int:
    global USER_ID_GLOBAL
    if not userDao.email or not userDao.password:
        raise HTTPException(status_code=401, detail="아이디나 패스워드를 둘다 입력하세요")
    for u_id, find_user in user_list.items():
        # find_user : userid, email, password, nickname
        if find_user.email == userDao.email :
            raise HTTPException(status_code=400, detail="중복된 이메일입니다.")
    USER_ID_GLOBAL += 1
    user = User(
        user_id=USER_ID_GLOBAL,
        email= userDao.email,
        password= userDao.password,
        nickname= userDao.nickname
    )
    user_list[USER_ID_GLOBAL] = user
    return USER_ID_GLOBAL

def loginUser(loginUser: loginUserRequest) -> int :
    '''
    1. email 보고 사람 찾기
    2. password 일치여부 확인
    3. 회원정보 불러오기
    :param email:
    :param password:
    :return:
    '''
    email = loginUser.email
    password = loginUser.password

    for u_id, user in user_list.items() :
        # 발견한 경우
        if user.email == email and user.password == password :
            return u_id
        # 발견했는데 비번 다른 경우
        if user.email == email and user.password != password :
            raise HTTPException(status_code=401, detail="비밀번호가 다릅니다.")
    # 이메일도 발견 못한경우
    raise HTTPException(status_code=401, detail="비밀번호가 다릅니다.")

def editUser(user_id: int, request: EditUserRequest) -> int:
    # user info
    # change nickname
    if len(user_list) <= user_id :
        raise HTTPException(status_code=404, detail="User Not Found")
    if request.nickname == "" or request.nickname is None :
        raise HTTPException(status_code=400, detail="닉네임을 정확히 입력해주세요")
    find_user = user_list[user_id]
    find_user.nickname = request.nickname
    edit_user = EditUserRequest(
        user_id= user_id,
        nickname= find_user.nickname
    )
    user_list[user_id] = edit_user
    return user_id


def deleteUser(user_id: int) :
    if user_id in user_list:
        del user_list[user_id]
        return True
    raise HTTPException(status_code=404, detail="User not found")

