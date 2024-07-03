from datetime import datetime
from typing import List

import uuid
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    name: str = Field(..., examples=['Chat Name'])
    is_group_chat: bool
    participant_ids: List[str]
    image_url: str


class ChatResponse(BaseModel):
    name: str = Field(..., examples=['Chat Name'])
    is_group_chat: bool
    participant_ids: List[str]
    created_at: datetime
    image_url: str
    chat_id: uuid.UUID
    message_count: int
    messages: List[str]
