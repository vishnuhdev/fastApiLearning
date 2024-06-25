import uuid


from models.chat import Chat
from models.user import User
from schemas.chats_schemas import ChatRequest
from services.base_service import BaseService


class ChatService(BaseService):
    def create_chat(self, request: ChatRequest):
        new_chat = Chat(
            chat_id=uuid.uuid4(),
            name=request.name,
            is_group_chat=request.is_group_chat,
            participant_id=request.participant_ids,
            image_url=request.image_url,
            created_by=self.get_user_id()
        )
        self.db.add(new_chat)
        self.db.commit()
        return {
            'status': "Ok",
            'message': 'Chat created'
        }

    def retrieve_chats(self, email):
        get_user_id = self.db.query(User).filter(User.email == email).first().user_id
        chats = self.db.query(Chat).filter(Chat.created_by == get_user_id).all()
        return chats

    def delete_chat(self, chat_id):
        self.db.query(Chat).filter(Chat.chat_id == chat_id).delete()
        self.db.commit()
        return {
            'status': "Ok",
            'message': 'Chat deleted'
        }
