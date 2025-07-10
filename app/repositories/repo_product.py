from sqlalchemy.orm import Session
from app.models.model_product import Product
from app.common.types.product_schema import ProductCreate

def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session):
    return db.query(Product).all()

def get_product(db: Session, product_id: str):
    return db.query(Product).filter(Product.id == product_id).first()