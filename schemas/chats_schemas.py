from typing import List

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    name: str = Field(..., examples=['Chat Name'])
    is_group_chat: bool
    participant_ids: List[str]
    image_url: str


class ChatResponse(ChatRequest):
    chat_id: str
