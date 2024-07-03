from deps import verify_jwt
from models.user import User
from fastapi import HTTPException, status, Depends
import uuid
from schemas.auth_schemas import change_password_request, user_request, TokenResponse, UserAuth, TokenPayload, TokenRequest
from services.base_service import BaseService
from utils.utils import get_hashed_password, verify_password, create_access_token, create_refresh_token


class AuthService(BaseService):
    def create_account(self, user: user_request):
        user_already_present = self.db.query(User).filter_by(email=user.email).first()
        if user_already_present is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exist"
            )
        if user_already_present:
            raise HTTPException(status_code=409, detail='Email already registered')
        new_user = User(user_id=uuid.uuid4(), email=user.email, password=get_hashed_password(user.password),
                        mobile_number=user.mobile_number)
        self.db.add(new_user)
        self.db.commit()
        user_details = self.db.query(User).filter_by(email=user.email).first()
        token_request = TokenRequest(email=user_details.email, id=str(user_details.user_id))
        return TokenResponse(
            access_token=create_access_token(token_request),
            refresh_token=create_refresh_token(token_request)
        )

    def login_user(self, login: UserAuth):
        user = self.db.query(User).filter_by(email=login.email).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password"
            )

        hashed_pass = str(user.password)
        if not verify_password(login.password, hashed_pass):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password"
            )
        token_request = TokenRequest(id=str(user.user_id), email=user.email)
        return TokenResponse(
            access_token=create_access_token(token_request),
            refresh_token=create_refresh_token(token_request)
        )

    def change_password(self, password: change_password_request, user: TokenPayload):
        user = self.db.query(User).filter(User.user_id == user.id).first()
        if not user:
            raise HTTPException(status_code=404, detail='Email is not registered')
        is_correct = user.password == password.old_password
        if not is_correct:
            raise HTTPException(status_code=401, detail='Incorrect Old password')
        user.password = password.new_password
        self.db.commit()
        return {"detail": "Password changed successfully"}

    def delete_account(self, user: TokenPayload):
        user = self.db.query(User).filter(User.user_id == user.id).first()
        if not user:
            raise HTTPException(status_code=401, detail='User not found')
        self.db.delete(user)
        self.db.commit()
        return {"detail": "User deleted successfully"}

    def get_refresh_token(self, token: str):
        payload = verify_jwt(token,is_refresh=True)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token is not valid"
            )
        if payload.token_type != 'refresh_token':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid refresh token'
            )
        token_request = TokenRequest(id=str(payload.id), email=payload.email)
        return TokenResponse(
            access_token=create_access_token(token_request),
            refresh_token=create_refresh_token(token_request)
        )