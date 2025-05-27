from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
