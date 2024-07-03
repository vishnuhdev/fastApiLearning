from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from backend.database import get_db
from deps import JWTBearer
from schemas.chats_schemas import ChatRequest, ChatResponse
from services.chat_service import ChatService

chat_route = APIRouter(prefix="/chats", tags=["Chat"])


@chat_route.post('', status_code=201)
async def create_chat(request: ChatRequest, db: Session = Depends(get_db), user=Depends(JWTBearer())):
    service = ChatService(db)
    return service.create_chat(request, user)


@chat_route.get('', status_code=200, response_model=List[ChatResponse])
async def retrieve_chats(db: Session = Depends(get_db), user=Depends(JWTBearer())):
    service = ChatService(db)
    return service.retrieve_chats(user)


@chat_route.delete("/{chat_id}",status_code=204)
async def delete_chat(chat_id: str, db: Session = Depends(get_db), user=Depends(JWTBearer())):
    service = ChatService(db)
    return service.delete_chat(chat_id, user)