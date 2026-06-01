from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
import models, schemas

# Products
def get_product(db: Session, product_id: int, user_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id, models.Product.user_id == user_id).first()

def get_product_by_sku(db: Session, sku: str, user_id: int):
    return db.query(models.Product).filter(models.Product.sku == sku, models.Product.user_id == user_id).first()

def get_products(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Product).filter(models.Product.user_id == user_id).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate, user_id: int):
    if product.quantity < 0:
        raise HTTPException(status_code=400, detail="Quantity cannot be negative")
    db_product = get_product_by_sku(db, sku=product.sku, user_id=user_id)
    if db_product:
        raise HTTPException(status_code=400, detail="SKU already registered")
    
    db_product = models.Product(**product.model_dump(), user_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: schemas.ProductUpdate, user_id: int):
    db_product = get_product(db, product_id, user_id)
    if not db_product:
        return None
    
    update_data = product_update.model_dump(exclude_unset=True)
    if 'quantity' in update_data and update_data['quantity'] < 0:
        raise HTTPException(status_code=400, detail="Quantity cannot be negative")

    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    try:
        db.commit()
        db.refresh(db_product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="SKU already registered")
        
    return db_product

def delete_product(db: Session, product_id: int, user_id: int):
    db_product = get_product(db, product_id, user_id)
    if db_product:
        if len(db_product.orders) > 0:
            raise HTTPException(status_code=400, detail="Cannot delete product: Please cancel all related orders first.")
        db.delete(db_product)
        db.commit()
    return db_product

# Customers
def get_customer(db: Session, customer_id: int, user_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id, models.Customer.user_id == user_id).first()

def get_customer_by_email(db: Session, email: str, user_id: int):
    return db.query(models.Customer).filter(models.Customer.email == email, models.Customer.user_id == user_id).first()

def get_customers(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).filter(models.Customer.user_id == user_id).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: schemas.CustomerCreate, user_id: int):
    db_customer = get_customer_by_email(db, email=customer.email, user_id=user_id)
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_customer = models.Customer(**customer.model_dump(), user_id=user_id)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int, user_id: int):
    db_customer = get_customer(db, customer_id, user_id)
    if db_customer:
        if len(db_customer.orders) > 0:
            raise HTTPException(status_code=400, detail="Cannot delete client: Please cancel all related orders first.")
        db.delete(db_customer)
        db.commit()
    return db_customer

# Orders
def get_order(db: Session, order_id: int, user_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id, models.Order.user_id == user_id).first()

def get_orders(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Order).filter(models.Order.user_id == user_id).offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderCreate, user_id: int):
    db_product = get_product(db, order.product_id, user_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    db_customer = get_customer(db, order.customer_id, user_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
        
    if db_product.quantity < order.quantity:
        raise HTTPException(status_code=400, detail="Insufficient inventory")
        
    # Deduct stock
    db_product.quantity -= order.quantity
    
    total_amount = db_product.price * order.quantity
    
    db_order = models.Order(
        customer_id=order.customer_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_amount=total_amount,
        user_id=user_id
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int, user_id: int):
    db_order = get_order(db, order_id, user_id)
    if db_order:
        # Note: Depending on business rules, canceling an order might restock inventory
        db_product = get_product(db, db_order.product_id, user_id)
        if db_product:
             db_product.quantity += db_order.quantity
        db.delete(db_order)
        db.commit()
    return db_order
