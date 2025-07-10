from pydantic import BaseModel
from typing import List, Optional

class OrderBase(BaseModel):
    customer_id: str
    product_ids: List[str]

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: str

    class Config:
        orm_mode = True