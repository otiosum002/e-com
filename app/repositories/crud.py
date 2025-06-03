from sqlalchemy.orm import Session
from app.models import models
from app.common.types import schemas



# Products

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session):
    return db.query(models.Product).all()



# Users

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(models.User).all()



# Orders
def create_order(db: Session, order: schemas.OrderCreate):
   
    products = db.query(models.Product).filter(models.Product.id.in_(order.product_ids)).all()

    db_order = models.Order(customer_id=order.customer_id, products=products)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session):
    return db.query(models.Order).all()
