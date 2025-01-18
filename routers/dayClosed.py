from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from models import DayClosure, User, CurrentCash
from database import get_db
from schemas import DayClosedBaseMode,ShowDayClosedBaseMode
from oauth2 import get_current_user

routers = APIRouter(
    prefix="/api/day-closed",
    tags=["Day Closed"]
)

@routers.post("/")
async def post(request: DayClosedBaseMode, db: Session = Depends(get_db)):
    user = db.query(CurrentCash).filter_by(user_id=request.user_id).first()

    if user:
        user.current_cash -= request.closed_cash
        db.add(user)
        db.commit()
        db.refresh(user)

    try:
        # Convert closure_date to a proper datetime object
        closure_date = datetime.strptime(request.closure_date, "%m-%d-%Y").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use MM-DD-YYYY."
        )

    new_dayclosed = DayClosure(
        user_id=request.user_id,
        closed_cash=request.closed_cash,
        closure_date=closure_date
    )
    db.add(new_dayclosed)
    db.commit()
    db.refresh(new_dayclosed)
    return new_dayclosed




@routers.get("/",response_model=List[ShowDayClosedBaseMode])

async def get(db:Session = Depends(get_db)):
    dayClosed = db.query(DayClosure).all()
    return dayClosed