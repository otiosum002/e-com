from fastapi import FastAPI
from app.db.database import Base, engine
from app.api import products, users, orders, auth, simple_auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(simple_auth.router, prefix="/simple-auth", tags=["Simple Authentication"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
