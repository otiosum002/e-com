from sqlalchemy.orm import Session
from app.models.model_order import Order
from app.models.model_product import Product
from app.common.types.order_schema import OrderCreate

def create_order(db: Session, order: OrderCreate):
    products = db.query(Product).filter(Product.id.in_(order.product_ids)).all()
    db_order = Order(customer_id=order.customer_id, products=products)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session):
    return db.query(Order).all()

def get_order(db: Session, order_id: str):
    return db.query(Order).filter(Order.id == order_id).first()
