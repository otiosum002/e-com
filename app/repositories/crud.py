from sqlalchemy.orm import Session
from app.models.model_product import Product
from app.models.model_order import Order
from app.models.user import User
from app.common.types.product_schema import ProductCreate
from app.common.types.order_schema import OrderCreate
from app.common.types.user_schema import UserCreate



# Products

def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session):
    return db.query(Product).all()



# Users

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(User).all()



# Orders
def create_order(db: Session, order: OrderCreate):
   
    products = db.query(Product).filter(Product.id.in_(order.product_ids)).all()

    db_order = Order(customer_id=order.customer_id, products=products)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session):
    return db.query(Order).all()
