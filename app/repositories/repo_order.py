from sqlalchemy.orm import Session
from app.models import models
from app.common.types import schemas

def create_order(db: Session, order: schemas.OrderCreate):
   
    products = db.query(models.Product).filter(models.Product.id.in_(order.product_ids)).all()

    db_order = models.Order(customer_id=order.customer_id, products=products)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session):
    return db.query(models.Order).all()
