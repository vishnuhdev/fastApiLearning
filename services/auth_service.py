from sqlalchemy.orm import Session
from models.user import User
from fastapi import HTTPException
import uuid
from schemas.auth_schemas import login_request, change_password_request, user_request
from services.base_service import BaseService


class AuthService(BaseService):
    def create_account(self, user: user_request):
        new_user = User(user_id=uuid.uuid4(), email=user.email, password=user.password,
                        mobile_number=user.mobile_number)
        user_already_present = self.db.query(User).filter(User.email == user.email).first()
        if user_already_present:
            raise HTTPException(status_code=409, detail='Email already registered')
        self.db.add(new_user)
        self.db.commit()
        return {"detail": "User created successfully"}

    def login_user(self, login: login_request):
        user = self.db.query(User).filter(User.email == login.email).first()
        password = self.db.query(User).filter(User.password == login.password).first()
        if not user:
            raise HTTPException(status_code=401, detail='Email is not registered')
        if not password:
            raise HTTPException(status_code=401, detail='Incorrect password')
        return {"detail": "User logged in"}

    def change_password(self, password: change_password_request):
        user = self.db.query(User).filter(User.email == password.email).first()
        if not user:
            raise HTTPException(status_code=404, detail='Email is not registered')
        is_correct = user.password == password.old_password
        if not is_correct:
            raise HTTPException(status_code=401, detail='Incorrect Old password')
        user.password = password.new_password
        self.db.commit()
        return {"detail": "Password changed successfully"}

    def delete_account(self, email: str):
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail='User not found')
        self.db.delete(user)
        self.db.commit()
        return {"detail": "User deleted successfully"}