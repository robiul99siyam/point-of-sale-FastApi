from pydantic import BaseModel 
from typing import List,Optional
from enum import Enum

class UserAdminRole(str,Enum):
    ADMIN = "admin"
    USER = "user"
    CASHIER = "cashier"
    MANAGER = "manager"


class PaymentRole(str,Enum):
    CREDIT = "credit"
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    OTHER = "other"


class UserModel(BaseModel):
    id: int
    username: str
    password: str
    role: UserAdminRole
    image: str

    class Config:
        orm_mode = True



class SupplierModel(BaseModel):
    id : int
    name : str
    contact : str
    email : str
    address : str
    image : str

    class Config:
        orm_model  = True

class CategoryModel(BaseModel):
    id : int
    name : str
    image : str
    class Config:
        orm_model  = True
class CustomModel(BaseModel):
    id : int
    name : str
    phone: str
    email: str
    address: str
    image: str

    class Config:
        orm_model  = True
class ProductModel(BaseModel):
    id : int
    name : str
    selling_price : float
    description : str
    supplier_id : int
    category_id : int
    stock : int
    cost_price : float
    image : str
    class Config:
        orm_model  = True

class TransactionModel(BaseModel):
    id: int
    user_id:int
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float
    customer_id:int
    payment_role: PaymentRole
    class Config:
        orm_mode = True
