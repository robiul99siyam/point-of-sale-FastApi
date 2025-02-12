from pydantic import BaseModel , ConfigDict
from typing import List,Optional
from enum import Enum



class UserAdminRole(str,Enum):
    ADMIN = "admin"
    CASHIER = "cashier"
    MANAGER = "manager"

class TshirtSize(str, Enum):
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"


class PaymentRole(str,Enum):
    CREDIT = "credit"
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"


class UserModel(BaseModel):
    id: int
    username: str
    password: str
    role: UserAdminRole
    image: str
    model_config = ConfigDict(from_attributes=True) 


class CurrentCashBaseModel(BaseModel):
    current_cash : float
    user_id  : int
    date : str
    
    model_config = ConfigDict(from_attributes=True) 


class ShowUserBaseModel(BaseModel):

    id:int
    username : str
    
    model_config = ConfigDict(from_attributes=True) 

class CashModel(BaseModel):
    id:int
    current_cash : float
    date : str
    user : Optional[ShowUserBaseModel] = None

    
    model_config = ConfigDict(from_attributes=True) 


class SupplierModel(BaseModel):
    id : int
    name : str
    contact:int
    email : str
    address : str
    image : str

    
    model_config = ConfigDict(from_attributes=True) 

class Supplier(BaseModel):
    id : int
    name : str
    
    model_config = ConfigDict(from_attributes=True) 

class CategoryModel(BaseModel):
    id : int
    name : str
    image : str
    
    model_config = ConfigDict(from_attributes=True)  

class Category(BaseModel):
    id : int
    name:str
    
    model_config = ConfigDict(from_attributes=True)  

class CustomModel(BaseModel):
    id : int
    name : str
    phone: str
    email: str
    address: str
    image: str

    
    model_config = ConfigDict(from_attributes=True)  


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
    sizes: List[str]
    
    model_config = ConfigDict(from_attributes=True)  


class ShowProductBaseModel(BaseModel):
    id: int
    name: str
    selling_price: float
    description: str
    category: Optional[Category] = None  
    supplier: Optional[Supplier] = None  
    stock: int
    cost_price: float
    image: str
    sizes: List[str]

    
    model_config = ConfigDict(from_attributes=True) 

class TransactionModel(BaseModel):
    id: int
    user_id:int
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float
    customer_id:int
    payment_method: PaymentRole
    date: Optional[str] = None
    profit: Optional[float] = None
    loss: Optional[float] = None
    current_cash : Optional[float] = None
    
    model_config = ConfigDict(from_attributes=True)  

class ShowTransactionModel(BaseModel):
    id: int
    user: Optional[ShowUserBaseModel] = None
    product: Optional[ShowProductBaseModel] = None  
    quantity: int
    unit_price: float
    subtotal: float
    customer: Optional[CustomModel] = None  
    payment_method: PaymentRole
    date: Optional[str] = None
    profit: Optional[float] = None
    loss: Optional[float] = None
    current_cash: Optional[float] = None

    
    model_config = ConfigDict(from_attributes=True)  


class Login(BaseModel):
    username : str
    password : str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class DayClosedBaseMode(BaseModel):
    user_id : int
    closure_date : str
    closed_cash : float

    model_config = ConfigDict(from_attributes=True)  


class ShowDayClosedBaseMode(BaseModel):
    user : Optional[ShowUserBaseModel] = None
    closure_date : str
    closed_cash : float

    model_config = ConfigDict(from_attributes=True)