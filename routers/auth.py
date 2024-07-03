from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from deps import JWTBearer
from schemas.auth_schemas import user_request, change_password_request, TokenResponse, UserAuth, TokenPayload
from services.auth_service import AuthService

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post('/signup', response_model=TokenResponse)
async def create_account(user: user_request, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.create_account(user)


@auth_router.post('/login', tags=['auth'], response_model=TokenResponse)
async def login_user(login: UserAuth, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login_user(login)


@auth_router.post('/change_password', tags=['auth'])
async def change_password(password: change_password_request,
                          db: Session = Depends(get_db),
                          user=Depends(JWTBearer())):
    service = AuthService(db)
    return service.change_password(password, user)


@auth_router.delete('/delete_user', tags=['auth'])
async def delete_account(db: Session = Depends(get_db),
                         user=Depends(JWTBearer())):
    service = AuthService(db)
    return service.delete_account(user)


@auth_router.get('', tags=['auth'],summary="Retrieve Token", response_model=TokenResponse)
async def get_refresh_token(token: str, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.get_refresh_token(token)
