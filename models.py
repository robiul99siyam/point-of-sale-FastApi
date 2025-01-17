from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  
    image = Column(String, nullable=True)  
    current_cash = Column(Float, default=0.0, nullable=False) 
    transactions = relationship("Transaction", back_populates="user")
    day_closures = relationship("DayClosure", back_populates="user")

class DayClosure(Base):
    __tablename__ = "day_closures"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="day_closures")
    closure_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    closed_cash = Column(Float, nullable=False)  


class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    contact = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    address = Column(String, nullable=False)
    image = Column(String, nullable=True) 
    products = relationship("Product", back_populates="supplier")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    image = Column(String, nullable=True)  
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")
    stock = Column(Integer, nullable=False, default=0)  
    cost_price = Column(Float, nullable=False)  
    selling_price = Column(Float, nullable=False)  
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    supplier = relationship("Supplier", back_populates="products")
    image = Column(String, nullable=True) 
    transactions = relationship("Transaction", back_populates="product")


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    address = Column(String, nullable=True)
    image = Column(String, nullable=True)  
    transactions = relationship("Transaction", back_populates="customer")


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  
    user = relationship("User", back_populates="transactions") 
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="transactions")
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="transactions")
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    payment_method = Column(String, nullable=True)
    date = Column(String, nullable=True)
    profit = Column(Float, nullable=True) 
    loss = Column(Float, nullable=True)
    current_cash = Column(Float, nullable=True)

    def update_user_cash(self, db_session):
        user = db_session.query(User).filter_by(id=self.user_id).first()
        if user and self.payment_method == "cash":
            user.current_cash -= self.subtotal
            db_session.commit()
