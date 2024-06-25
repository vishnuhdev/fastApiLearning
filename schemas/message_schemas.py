import uuid
from datetime import datetime

from pydantic import BaseModel


class MessageRequest(BaseModel):
    content: str
    chat_id: uuid.UUID


class Message(BaseModel):
    message_id: uuid.UUID
    name: str
    content: str
    image_url: str
    sender_id: uuid.UUID
    chat_id: uuid.UUID
    created_at: datetime


class MessageResponse(BaseModel):
    message_id: uuid.UUID
    content: str
    sender_id: uuid.UUID
    created_at: datetime

