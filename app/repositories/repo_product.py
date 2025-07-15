from sqlalchemy.orm import Session
from app.models.model_product import Product
from app.common.types.product_schema import ProductCreate
from app.utils.cache import cache

def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    # Invalidate products list cache
    cache.invalidate('products_list')
    return db_product

def get_products(db: Session):
    cached = cache.get('products_list')
    if cached is not None:
        return cached
    products = db.query(Product).all()
    cache.set('products_list', products, ttl=60)  # cache for 60 seconds
    return products

def get_product(db: Session, product_id: str):
    cache_key = f'product_{product_id}'
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        cache.set(cache_key, product, ttl=60)  # cache for 60 seconds
    return product