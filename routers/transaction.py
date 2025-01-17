from fastapi import APIRouter,Form ,Depends,HTTPException
from fastapi.staticfiles import StaticFiles
from schemas import TransactionModel,PaymentRole
from models import Transaction,Product
from database import get_db
from sqlalchemy.orm import Session
import os
from typing import List,Optional




routers = APIRouter(
    prefix="/api/v1/transactions",
    tags=["Supplier"]
)


routers.mount("/uploads", StaticFiles(directory="uploads"), name="uploads") 
UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)



@routers.post("/", response_model=TransactionModel)
async def create_transaction(
    user_id: int = Form(...),
    product_id: int = Form(...),
    quantity: int = Form(...),
    unit_price: float = Form(...),
    subtotal: float = Form(...),
    customer_id: int = Form(...),
    payment_method: PaymentRole = Form(...),
    date: Optional[str] = Form(None),
    profit: float = Form(None),
    loss: float = Form(None),
    db: Session = Depends(get_db),
):
    # Fetch the product by ID
    product = db.query(Product).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Validate cost price
    if product.cost_price is None:
        raise HTTPException(status_code=400, detail="Product cost price is missing")
    
    # Check stock availability
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    
    # Deduct stock
    product.stock -= quantity
    
    # Validate subtotal
    calculated_subtotal = quantity * unit_price
    if subtotal != calculated_subtotal:
        raise HTTPException(
            status_code=400,
            detail=f"Subtotal mismatch. Expected: {calculated_subtotal}, Provided: {subtotal}"
        )

    # Create the transaction
    new_transaction = Transaction(
        subtotal=subtotal,
        quantity=quantity,
        unit_price=unit_price,
        user_id=user_id,
        customer_id=customer_id,
        product_id=product_id,
        payment_method=payment_method,
        date=date,
        profit = profit,
        loss = loss,
    )
    
    # If profit and loss are still None (in case they are not set by the input)
    if unit_price > product.cost_price:
        new_transaction.profit = (unit_price - product.cost_price) * quantity
        new_transaction.loss = 0  # No loss if there is a profit
    elif unit_price < product.cost_price:
        new_transaction.loss = (product.cost_price - unit_price) * quantity
        new_transaction.profit = 0  # No profit if there is a loss
    else:
        new_transaction.profit = 0  # No profit or loss if prices are the same
        new_transaction.loss = 0
    

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


@routers.get("/",response_model=List[TransactionModel])
async def get_transactions(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).offset(skip).limit(limit).all()
    return transactions

