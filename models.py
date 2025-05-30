from sqlalchemy import Column, String, Float, Integer, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import relationship
import uuid

from .database import Base

order_product = Table(
    "order_product", Base.metadata,
    Column("order_id", String, ForeignKey("orders.id")),
    Column("product_id", String, ForeignKey("products.id"))
)

class Product(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    in_stock = Column(Integer, default=0)

class User(Base):  
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, ForeignKey("users.id"))
    customer = relationship("User")
    products = relationship("Product", secondary=order_product)
