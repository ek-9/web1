from pydantic import BaseModel, EmailStr
from fastapi import Form, UploadFile

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

class EditUserPasswordRequest(BaseModel):
    user_id: int
    password: str
