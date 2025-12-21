from pydantic import BaseModel, EmailStr, Field
from typing import List

class User(BaseModel):
    '''
    email,
    password,
    nickname
    '''
    user_id: int
    email: EmailStr
    # 8~20자, 대문자, 소문자, 숫자, 특수문자 하나씩 갖고 있어야함
    password: str = Field(min_length=8,max_length=20)
    # 닉네임 : 공백 없어야함, 10글자 이내
    nickname: str = Field(max_length=20)
    # 프로필 이미지 경로 저장
    profile_image: str
    # 좋아요 누른 게시글 목록 저장
    post_like: List = Field(default_factory=list)

class UserRequest(BaseModel) :
    email: EmailStr
    password: str
    nickname: str

class LoginUserRequest(BaseModel) :
    email: EmailStr
    password: str

class EditUserRequest(BaseModel):
    email: EmailStr
    nickname: str

class EditUserPasswordRequest(BaseModel):
    user_id: int
    password: str
