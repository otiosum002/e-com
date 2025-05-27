from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import UUID

class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    price: float
    in_stock: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: str

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: str

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    customer_id: str
    product_ids: List[str]

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: str

    class Config:
        orm_mode = True
