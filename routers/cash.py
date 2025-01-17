from fastapi import APIRouter,Form ,Depends,HTTPException
from fastapi.staticfiles import StaticFiles
from schemas import CurrentCashBaseModel
from models import CurrentCash
from database import get_db
from sqlalchemy.orm import Session
import os
from typing import List,Optional


routers = APIRouter(
    prefix="/api/cash",
    tags=['Cash']
)


@routers.post("/")
async def post(request:CurrentCashBaseModel,db:Session = Depends(get_db)):
    cash = CurrentCash(
        user_id = request.user_id,
        current_cash = request.current_cash
    )

    db.add(cash)
    db.commit()
    db.refresh(cash)
    return "Cash Add Successfully"

@routers.get("/",response_model=List[CurrentCashBaseModel])
async def get(db:Session = Depends(get_db)):
    cash = db.query(CurrentCash).all()
    return cash
