from pydantic import BaseModel, field_validator, EmailStr

class NewUserRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: str
    address: str
    phone: str

    @field_validator('email', 'password', 'nickname', 'phone')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Value required.')
        return v

    @field_validator('password')
    def password_len(cls, v):
        if len(v) < 10:
            raise ValueError('Password is too short.')
        return v

    @field_validator('nickname')
    def nickname_len(cls, v):
        if len(v) > 8:
            raise ValueError('Nickname is too long.')
        return v

class NewUserResponse(BaseModel):
    user_id: int

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: str
