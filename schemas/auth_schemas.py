from pydantic import BaseModel


class user_request(BaseModel):
    email: str
    password: str
    mobile_number: str


class login_request(BaseModel):
    email: str
    password: str


class change_password_request(BaseModel):
    email: str
    old_password: str
    new_password: str
