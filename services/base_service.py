from sqlalchemy.orm import Session

from models.user import User


class BaseService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_id(self) -> str:
        user = self.db.query(User).filter(User.email == "test@gmail.com").first()
        if user:
            print(f"User found: {user.user_id}")
            return user.user_id
        print("User not found")
        return ""
