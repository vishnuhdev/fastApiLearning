from sqlalchemy import Column, String, TIMESTAMP, text, UUID, ForeignKey

from backend.database import Base


class Message(Base):
    __tablename__ = "messages"

    chat_id = Column(UUID, primary_key=True)
    message_id = Column(UUID, primary_key=True)
    name = Column(String, nullable=False)
    sender_id = Column(UUID, ForeignKey("user_details.user_id"), nullable=False)
    content = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
