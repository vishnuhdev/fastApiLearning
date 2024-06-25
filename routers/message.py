import uuid
from typing import List

from fastapi import APIRouter, Depends

from backend.database import get_db
from schemas.message_schemas import MessageRequest, MessageResponse
from services.message_service import MessageService

message_route = APIRouter(prefix="/message", tags=["Message"])


@message_route.post('/create_message', status_code=201)
async def create_message(request: MessageRequest, db: Depends = Depends(get_db)):
    service = MessageService(db)
    return service.create_message(request)


@message_route.get('/{chat_id}', status_code=200, response_model=List[MessageResponse])
async def get_messages(chat_id, db: Depends = Depends(get_db)):
    service = MessageService(db)
    return service.get_all_message(chat_id)