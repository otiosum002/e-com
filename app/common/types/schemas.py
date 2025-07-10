from pydantic import BaseModel
from typing import List, Optional


# Product Schemas

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: str

    class Config:
        orm_mode = True



# User Schemas

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: str

    class Config:
        orm_mode = True



# Order Schemas

class OrderBase(BaseModel):
    customer_id: str
    product_ids: List[str]

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: str

    class Config:
        orm_mode = True

