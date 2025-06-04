from fastapi import FastAPI
from app.db.database import Base, engine
from app.api import products, users, orders

Base.metadata.create_all(bind=engine)

app = FastAPI()

#app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
