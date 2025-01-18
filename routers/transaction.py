from fastapi import APIRouter,Form ,Depends,HTTPException,status
from fastapi.staticfiles import StaticFiles
from schemas import TransactionModel,PaymentRole
from models import Transaction,Product,CurrentCash,User
from database import get_db
from sqlalchemy.orm import Session
import os
from typing import List,Optional
from oauth2 import get_current_user
from datetime import datetime



routers = APIRouter(
    prefix="/api/v1/transactions",
    tags=["Transactions"]
)


routers.mount("/uploads", StaticFiles(directory="uploads"), name="uploads") 
UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@routers.post("/",status_code=status.HTTP_201_CREATED)
async def create_transaction(
    user_id: int = Form(...),
    product_id: int = Form(...),
    quantity: int = Form(...,ge=1),
    unit_price: float = Form(...,gt=1),
    subtotal: float = Form(...,gt=1),
    customer_id: int = Form(...),
    payment_method: PaymentRole = Form(...),
    date: Optional[str] = Form(None),
    profit: float = Form(None),
    loss: float = Form(None),
    current_cash: float = Form(None),
    db: Session = Depends(get_db),
):
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

    # Handle current cash
    user = db.query(CurrentCash).filter_by(user_id=user_id).first()
    if user:
        if payment_method == PaymentRole.CASH:
            user.current_cash += subtotal
            db.add(user)  
            db.commit()  
            db.refresh(user)  

    new_transaction = Transaction(
        subtotal=subtotal,
        quantity=quantity,
        unit_price=unit_price,
        user_id=user_id,
        customer_id=customer_id,
        product_id=product_id,
        payment_method=payment_method,
        date=date,
        profit=profit,
        loss=loss,
        current_cash=user.current_cash if user else 0  # Use updated cash value
    )

    # Calculate profit and loss
    if unit_price > product.cost_price:
        new_transaction.profit = (unit_price - product.cost_price) * quantity
        new_transaction.loss = 0
    elif unit_price < product.cost_price:
        new_transaction.loss = (product.cost_price - unit_price) * quantity
        new_transaction.profit = 0
    else:
        new_transaction.profit = 0
        new_transaction.loss = 0
    
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction

@routers.get("/",response_model=List[TransactionModel],status_code=status.HTTP_200_OK)
async def get_transactions( db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    return transactions

