from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.repositories import crud
from app.common.types import schemas
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@router.get("/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)
