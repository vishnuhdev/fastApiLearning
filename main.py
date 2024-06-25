from fastapi import FastAPI

from routers.auth import auth_router
from routers.chat import chat_route
from backend.database import db_init
from routers.message import message_route

app = FastAPI()

app.include_router(auth_router)
app.include_router(chat_route)
app.include_router(message_route)


db_init()
