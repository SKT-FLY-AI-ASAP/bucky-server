from pydantic import BaseModel, field_validator, EmailStr
from starlette import status

from core.exceptions import BaseCustomException

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator('email', 'password')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise BaseCustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Value required.'
            )
        return v


class LogoutResponse(BaseModel):
    user_id: int


class EmailAuthRequest(BaseModel):
    email: EmailStr

    @field_validator('email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise BaseCustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Value required.'
            )
        return v


class NewUserRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: str
    address: str
    phone: str

    @field_validator('email', 'password', 'nickname', 'phone')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise BaseCustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Value required.'
            )
        return v

    # @field_validator('password')
    # def password_len(cls, v):
    #     if len(v) < 10:
    #         raise BaseCustomException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail='Password is too short.'
    #         )
    #     return v

    # @field_validator('nickname')
    # def nickname_len(cls, v):
    #     if len(v) > 8:
    #         raise BaseCustomException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail='Nickname is too long.'
    #         )
    #     return v


class NewUserResponse(BaseModel):
    user_id: int


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_id: int


class EmailVerification(BaseModel):
    code: str
    verified: bool


class NicknameValidRequest(BaseModel):
    nickname: str

    # @field_validator('nickname')
    # def nickname_len(cls, v):
    #     if len(v) > 8:
    #         raise BaseCustomException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail='Nickname is too long.'
    #         )
    #     return v
