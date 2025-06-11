from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.auth import get_password_hash, verify_password

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, username: str, email: str, password: str, full_name: str = None) -> User:
        hashed_password = get_password_hash(password)
        db_user = User(
            username=username,
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
            disabled=False,
            is_verified=False
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def verify_user(self, username: str) -> bool:
        user = self.get_user(username)
        if user:
            user.is_verified = True
            self.db.commit()
            return True
        return False

    def authenticate_user(self, username: str, password: str) -> User:
        user = self.get_user(username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user 