from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.database import get_db
from app.models.user import User
from app.common.types.user_schema import UserCreate, Token, UserResponse
from app.repositories.repo_user import create_user, get_user, verify_user
from app.utils.auth import create_token, oauth2_scheme, verify_token, get_password_hash
from app.utils.email import send_verification_email
from app.common.constants.auth import ACCESS_TOKEN_EXPIRE_MINUTES, VERIFICATION_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/register", response_model=dict)
async def register(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    db_user = get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user.password)
    db_user = create_user(
        db=db,
        user=UserCreate(
            username=user.username,
            email=user.email,
            password=hashed_password,
            full_name=user.full_name
        )
    )

    token_data = {"sub": user.username}
    token = create_token(token_data, timedelta(minutes=VERIFICATION_TOKEN_EXPIRE_MINUTES))
    verification_url = f"http://localhost:8000/verify-email?token={token}"

    background_tasks.add_task(
        send_verification_email,
        email=user.email,
        username=user.username,
        verification_url=verification_url
    )
    
    return {"msg": "User created. Please verify your email."}

@router.get("/verify-email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    username = payload.get("sub")
    if verify_user(db, username):
        return {"msg": "Email verified successfully"}
    raise HTTPException(status_code=400, detail="Invalid token")

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_user(db, form_data.username)
    if not user or not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials or email not verified",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    payload = verify_token(token)
    if not payload:
        raise credentials_exception
        
    username = payload.get("sub")
    if not username:
        raise credentials_exception
        
    user = get_user(db, username)
    if not user:
        raise credentials_exception
        
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled or not current_user.is_verified:
        raise HTTPException(status_code=400, detail="Inactive or unverified user")
    return current_user

@router.get("/users/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user 