from pydantic import BaseModel
from typing import List, Optional

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