from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from schemas.auth_schemas import user_request, login_request, change_password_request
from services.auth_service import AuthService

auth_router = APIRouter()


@auth_router.post('/signup', tags=['auth'])
async def create_account(user: user_request, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.create_account(user)


@auth_router.post('/login', tags=['auth'])
async def login_user(login: login_request, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login_user(login)


@auth_router.post('/change_password', tags=['auth'])
async def change_password(password: change_password_request,  db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.change_password(password)


@auth_router.delete('/delete_user', tags=['auth'])
async def delete_account(email: str, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.delete_account(email)
