from sqlalchemy.orm import Session
from app.models.user import User
from app.common.types.user_schema import UserCreate
from app.utils.auth import verify_password

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=user.password,
        disabled=False,
        is_verified=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_user(db: Session, username: str) -> bool:
    user = get_user(db, username)
    if user:
        user.is_verified = True
        db.commit()
        return True
    return False

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def get_users(db: Session):
    return db.query(User).all()