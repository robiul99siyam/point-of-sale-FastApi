from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    image = Column(String, nullable=True)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete")
    day_closures = relationship("DayClosure", back_populates="user", cascade="all, delete")
    current_cash = relationship("CurrentCash", back_populates="user", cascade="all, delete", uselist=False)


class CurrentCash(Base):
    __tablename__ = "current_cash"
    id = Column(Integer, primary_key=True, index=True)
    current_cash = Column(Float, default=0.0, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    user = relationship("User", back_populates="current_cash")


class DayClosure(Base):
    __tablename__ = "day_closures"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    closure_date = Column(DateTime, nullable=False, server_default=func.now())
    closed_cash = Column(Float, nullable=False)
    user = relationship("User", back_populates="day_closures")


class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    contact = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    address = Column(String, nullable=False)
    image = Column(String, nullable=True)
    
    # Relationships
    products = relationship("Product", back_populates="supplier", cascade="all, delete")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    image = Column(String, nullable=True)
    
    # Relationships
    products = relationship("Product", back_populates="category", cascade="all, delete")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    stock = Column(Integer, nullable=False, default=0)
    cost_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id", ondelete="SET NULL"))
    image = Column(String, nullable=True)
    
    # Relationships
    category = relationship("Category", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")
    transactions = relationship("Transaction", back_populates="product", cascade="all, delete")


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=True, index=True)
    address = Column(String, nullable=True)
    image = Column(String, nullable=True)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="customer", cascade="all, delete")


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"))
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="SET NULL"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    payment_method = Column(String, nullable=True)
    date = Column(String, nullable=False)
    profit = Column(Float, nullable=True)
    loss = Column(Float, nullable=True)
    current_cash = Column(Float, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    product = relationship("Product", back_populates="transactions")
    customer = relationship("Customer", back_populates="transactions")

    # def update_user_cash(self, db_session):
    #     current_cash_record = db_session.query(CurrentCash).filter_by(user_id=self.user_id).first()
    #     if not current_cash_record:
    #         raise Exception("CurrentCash record not found for the user.")
        
    #     if self.payment_method.lower() == "cash":
    #         current_cash_record.current_cash = max(0, current_cash_record.current_cash - self.subtotal)
    #         db_session.commit()