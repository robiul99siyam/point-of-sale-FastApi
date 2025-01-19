from fastapi import APIRouter,Depends,HTTPException,status
from schemas import CurrentCashBaseModel,CashModel
from models import CurrentCash
from database import get_db
from sqlalchemy.orm import Session
from typing import List
from oauth2 import get_current_user


routers = APIRouter(
    prefix="/api/cash",
    tags=['Cash']
)
@routers.post("/")
async def post(request: List[CurrentCashBaseModel], db: Session = Depends(get_db)):


    cash_amount = 0

    for item in request:
        cash_amount += item.current_cash

    user_id = item.user_id
    existing_cash_record = db.query(CurrentCash).filter_by(user_id=user_id).first()

    if existing_cash_record:
       
        existing_cash_record.current_cash += cash_amount
    else:
        cash = CurrentCash(
            user_id=user_id,
            current_cash=cash_amount
        )
        db.add(cash)

    db.commit()

    updated_cash_record = db.query(CurrentCash).filter_by(user_id=user_id).first()

    return {
        "message": "Cash updated successfully",
        "total_cash": updated_cash_record.current_cash  # Reflect the actual updated value
    }

@routers.get("/",response_model=List[CashModel])
async def get(db:Session = Depends(get_db)):
    cash = db.query(CurrentCash).all()
    return cash

@routers.delete("/{id}")
async def get(id:int,db:Session = Depends(get_db)):

    cash = db.query(CurrentCash).filter(CurrentCash.id == id).first()
    if not cash:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"customer{id} is not found")
    db.delete(cash)
    db.commit()
    return "delete done"

