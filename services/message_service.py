import uuid

from models.chat import Chat
from models.message import Message
from schemas.message_schemas import MessageRequest, MessageResponse
from services.base_service import BaseService


class MessageService(BaseService):
    def create_message(self, request: MessageRequest):
        chat = self.db.query(Chat).filter(Chat.chat_id == request.chat_id).first()
        user_id = self.get_user_id()
        if not user_id:
            return {
                'status': "Error",
                "message": "User not found"
            }
        if chat:
            message = Message(
                message_id=uuid.uuid4(),
                chat_id=request.chat_id,
                content=request.content,
                name=chat.name,
                image_url=chat.image_url,
                sender_id=user_id
            )
            self.db.add(message)
            self.db.commit()
        return {
                'status': "Ok",
                "message": "Message send successfully"
            }

    def get_all_message(self, chat_id):
        chat = self.db.query(Message).filter(Message.chat_id == chat_id).all()
        if not chat:
            return {
                'status': "Error",
                "message": "Chat not found"
            }

        return [
            MessageResponse(
                message_id=message.message_id,
                content=message.content,
                sender_id=message.sender_id,
                created_at=message.created_at,
            )
            for message in chat
        ]


