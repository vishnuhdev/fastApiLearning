import uuid
from typing import List

from models.chat import Chat
from models.message import Message
from models.user import User
from schemas.auth_schemas import TokenPayload
from schemas.chats_schemas import ChatRequest, ChatResponse
from services.base_service import BaseService


class ChatService(BaseService):
    def create_chat(self, request: ChatRequest, user: TokenPayload):
        participant_ids = request.participant_ids or []
        participant_ids.append(user.id)
        new_chat = Chat(
            chat_id=uuid.uuid4(),
            name=request.name,
            is_group_chat=request.is_group_chat,
            participant_id=participant_ids,
            image_url=request.image_url,
            created_by=self.get_user_id()
        )
        self.db.add(new_chat)
        self.db.commit()
        return {
            'status': "Ok",
            'message': 'Chat created'
        }

    def retrieve_chats(self, payload: TokenPayload) -> List[ChatResponse]:
        # user = self.db.query(User).filter(User.user_id == payload.id).first()
        # if not user:
        #     return []
        #
        # get_user_id = user.user_id

        chats = self.db.query(Chat).filter(Chat.created_by == payload.id).all()
        chat_responses = []
        for chat in chats:
            all_messages = self.db.query(Message).filter(Message.chat_id == chat.chat_id).all()
            message_count = len(all_messages)
            last_three_messages = self.db.query(Message).filter(Message.chat_id == chat.chat_id).order_by(
                Message.created_at.desc()).limit(3).all()
            message_contents = [message.content for message in last_three_messages][
                               ::-1]

            chat_response = ChatResponse(
                name=chat.name,
                is_group_chat=chat.is_group_chat,
                participant_ids=chat.participant_id,
                created_at=chat.created_at,
                image_url=chat.image_url,
                chat_id=chat.chat_id,
                message_count=message_count,
                messages=message_contents
            )
            chat_responses.append(chat_response)

        return chat_responses

    def delete_chat(self, chat_id):
        self.db.query(Chat).filter(Chat.chat_id == chat_id).delete()
        self.db.commit()
        return {
            'status': "Ok",
            'message': 'Chat deleted'
        }
