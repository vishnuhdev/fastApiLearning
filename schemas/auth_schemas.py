import uuid
from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    exp: int = None
    email: str = None
    id: str = None
    token_type: str = None


class UserAuth(BaseModel):
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")


class TokenRequest(BaseModel):
    id: str
    email: str


class user_request(BaseModel):
    email: str
    password: str
    mobile_number: str


class change_password_request(BaseModel):
    old_password: str
    new_password: str
