from pydantic import BaseModel 
from typing import List,Optional

class UserModel(BaseModel):
    id: int
    username: str
    password: str
    role: str
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
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float

    class Config:
        orm_mode = True
