from sqlalchemy import Column, String, Float, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
import uuid

from app.db.database import Base

# Association table for many-to-many relationship between Order and Product
order_products = Table(
    'order_products', Base.metadata,
    Column('order_id', String, ForeignKey('orders.id'), primary_key=True),
    Column('product_id', String, ForeignKey('products.id'), primary_key=True)
)

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, nullable=False)
    products = relationship("Product", secondary=order_products, back_populates="orders")