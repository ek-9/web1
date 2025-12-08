
from fastapi import APIRouter, HTTPException, status, UploadFile
import os
from week9.model.users import User
from week9.schema.userSchema import UserRequest, EditUserRequest, loginUserRequest, EditUserPasswordRequest


user_list = dict()
USER_ID_GLOBAL = 0
'''
1. 회원가입
2. 로그인
'''

def createUser(userDao: UserRequest, profile_image: UploadFile) -> int:
    global USER_ID_GLOBAL
    if not userDao.email or not userDao.password:
        raise HTTPException(status_code=401, detail="아이디나 패스워드를 둘다 입력하세요")
    for u_id, find_user in user_list.items():
        # find_user : userid, email, password, nickname
        if find_user.email == userDao.email :
            raise HTTPException(status_code=400, detail="중복된 이메일입니다.")
    if not valid_password(userDao.password) :
        raise HTTPException(status_code=402, detail="비밀번호는 소문자, 대문자, 숫자, 특수문자가 하나씩 포함되어야 합니다.")
    if not validate_nickname(userDao.nickname) :
        raise HTTPException(status_code=402, detail="닉네임은 공백없이 작성해주세요")

    USER_ID_GLOBAL += 1
    image_path = save_image(profile_image)
    user = User(
        user_id=USER_ID_GLOBAL,
        email= userDao.email,
        password= userDao.password,
        nickname= userDao.nickname,
        profile_image = image_path
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
    raise HTTPException(status_code=401, detail="존재하지 않는 이메일입니다.")

def editUser(user_id: int, request: EditUserRequest) -> int:
    # user info
    # change nickname
    if len(user_list) <= user_id :
        raise HTTPException(status_code=404, detail="User Not Found")
    if request.nickname == "" or request.nickname is None :
        raise HTTPException(status_code=400, detail="닉네임을 정확히 입력해주세요")
    if not validate_nickname(request.nickname) :
        raise HTTPException(status_code= 402, detail = "닉네임은 공백없이 작성해주세요")
    user_list[user_id].nickname = request.nickname
    return user_id

def editpw(user_id:int, request: EditUserPasswordRequest) :
    user_list[user_id].password = request.password
    if not valid_password(request.password) :
        raise HTTPException(status_code=402, detail = "비밀번호는 소문자, 대문자, 숫자, 특수문자가 하나씩 포함되어야 합니다.")
    return user_id

def deleteUser(user_id: int) :
    if user_id in user_list:
        del user_list[user_id]
        return True
    raise HTTPException(status_code=404, detail="User not found")

# 비밀번호 검증로직
def valid_password(pw: str):
    flag_num = 0
    flag_upper = 0
    flag_lower = 0
    flag_special = 0
    for p in pw:
        if p.isnumeric() :
            flag_num = 1
        if p.islower() :
            flag_lower = 1
        if p.isupper() :
            flag_upper = 1
        if not p.isalnum() :
            flag_special = 1
    if flag_num + flag_upper + flag_lower + flag_special  == 4 :
        return True
    else :
        return False

# 닉네임 검증로직
def validate_nickname(nickname: str) :
    for nm in nickname :
        if nm == ' ' :
            return False
    return True

UPLOAD_DIR = "static/profile_images"

# 프로필사진 저장
def save_image(file: UploadFile):
    if file is None:
        return None

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_ext = file.filename.split(".")[-1]
    filename = f"user_{USER_ID_GLOBAL}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path  # 이 경로만 DB에 저장


