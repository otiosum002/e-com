from sqlalchemy import Column, String, Float, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
import uuid

from app.db.database import Base

order_product = Table(
    "order_product",
    Base.metadata,
    Column("order_id", String, ForeignKey("orders.id"), primary_key=True),
    Column("product_id", String, ForeignKey("products.id"), primary_key=True)
)


# Product Model

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    in_stock = Column(Integer, default=0)



# User Model

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    orders = relationship("Order", back_populates="customer")



# Order Model

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
