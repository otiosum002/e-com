from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.model_product import Product
from app.models.model_order import Order
from app.utils.auth import get_password_hash
import uuid

# Ensure all tables are created
Base.metadata.create_all(bind=engine)

# Create a new database session
session: Session = SessionLocal()

# --- USERS ---
admin_user = User(
    id=str(uuid.uuid4()),
    username="admin",
    email="admin@example.com",
    full_name="Admin User",
    hashed_password=get_password_hash("adminpass"),
    is_verified=True,
    role="admin"
)

customer_user = User(
    id=str(uuid.uuid4()),
    username="customer",
    email="customer@example.com",
    full_name="Customer User",
    hashed_password=get_password_hash("customerpass"),
    is_verified=True,
    role="customer"
)

session.add_all([admin_user, customer_user])
session.commit()

# --- PRODUCTS ---
product1 = Product(
    id=str(uuid.uuid4()),
    name="Laptop",
    description="A powerful laptop",
    price=1200.0
)
product2 = Product(
    id=str(uuid.uuid4()),
    name="Smartphone",
    description="A modern smartphone",
    price=800.0
)
product3 = Product(
    id=str(uuid.uuid4()),
    name="Headphones",
    description="Noise-cancelling headphones",
    price=200.0
)

session.add_all([product1, product2, product3])
session.commit()

# --- ORDERS ---
# Assuming Order has customer_id and products relationship
order1 = Order(
    customer_id=customer_user.id,
    products=[product1, product2]
)
order2 = Order(
    customer_id=customer_user.id,
    products=[product3]
)

session.add_all([order1, order2])
session.commit()

print("Seed data inserted successfully.")
session.close() 