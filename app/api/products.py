from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.repositories import crud
from app.common.types import schemas
from app.db.database import get_db
from app.utils.auth import require_role

router = APIRouter()

@router.post("/", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin"]))
):
    return crud.create_product(db, product)

@router.get("/", response_model=list[schemas.Product])
def read_products(db: Session = Depends(get_db)):
    return crud.get_products(db)
