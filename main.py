from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import UUID, uuid4

app = FastAPI()

class Product(BaseModel):
    id: Optional[UUID] = None
    name: str
    description: Optional[str] = None
    price: float
    in_stock: int

class Customer(BaseModel):
    id: Optional[UUID] = None
    name: str
    email: EmailStr

class Order(BaseModel):
    id: Optional[UUID] = None
    customer_id: UUID
    product_ids: List[UUID]

products = []
customers = []
orders = []

@app.post("/products/", response_model=Product)
def create_product(product: Product):
    product.id = uuid4()
    products.append(product)
    return product

@app.get("/products/", response_model=List[Product])
def list_products():
    return products

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: UUID):
    for product in products:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: UUID, product_update: Product):
    for i, product in enumerate(products):
        if product.id == product_id:
            updated = product.copy(update=product_update.dict(exclude_unset=True))
            products[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}", response_model=Product)
def delete_product(product_id: UUID):
    for i, product in enumerate(products):
        if product.id == product_id:
            return products.pop(i)
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/customers/", response_model=Customer)
def create_customer(customer: Customer):
    customer.id = uuid4()
    customers.append(customer)
    return customer

@app.get("/customers/", response_model=List[Customer])
def list_customers():
    return customers

@app.get("/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: UUID):
    for customer in customers:
        if customer.id == customer_id:
            return customer
    raise HTTPException(status_code=404, detail="Customer not found")

@app.post("/orders/", response_model=Order)
def create_order(order: Order):
    if not any(c.id == order.customer_id for c in customers):
        raise HTTPException(status_code=404, detail="Customer not found")

    for pid in order.product_ids:
        if not any(p.id == pid for p in products):
            raise HTTPException(status_code=404, detail=f"Product with ID {pid} not found")

    order.id = uuid4()
    orders.append(order)
    return order

@app.get("/orders/", response_model=List[Order])
def list_orders():
    return orders

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
