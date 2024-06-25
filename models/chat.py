from sqlalchemy import Column, UUID, Boolean, ARRAY, TIMESTAMP, text, String, ForeignKey

from backend.database import Base


class Chat(Base):
    __tablename__ = "chats"

    chat_id = Column(UUID, primary_key=True)
    name = Column(String, nullable=False)
    is_group_chat = Column(Boolean, nullable=False)
    participant_id = Column(ARRAY(String), nullable=False)
    image_url = Column(String, nullable=True)
    created_by = Column(UUID, ForeignKey("user_details.user_id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))