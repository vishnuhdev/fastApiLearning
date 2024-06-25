from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from backend.database import get_db
from schemas.chats_schemas import ChatRequest
from services.chat_service import ChatService

chat_route = APIRouter(tags=["Chat"])


@chat_route.post('/create_chat', status_code=201)
async def create_chat(request: ChatRequest, db: Session = Depends(get_db)):
    service = ChatService(db)
    return service.create_chat(request)


@chat_route.get('/{email}', status_code=201)
async def retrieve_chats(email, db: Session = Depends(get_db)):
    service = ChatService(db)
    return service.retrieve_chats(email)


@chat_route.delete("/{chat_id}",status_code=204)
async def delete_chat(chat_id: str, db: Session = Depends(get_db)):
    service = ChatService(db)
    return service.delete_chat(chat_id)