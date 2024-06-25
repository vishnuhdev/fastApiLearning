from sqlalchemy import Column, String, TIMESTAMP, text, UUID

from backend.database import Base


class User(Base):
    __tablename__ = "user_details"

    user_id = Column(UUID, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    mobile_number = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))