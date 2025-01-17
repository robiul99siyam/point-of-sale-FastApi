from database import get_db
from fastapi import HTTPException,status , APIRouter,Depends
from models import User
from sqlalchemy.orm import Session
from hashing import Hash
from Tokens import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
routers = APIRouter(
    prefix="/login",
    tags=['Authentication']
)

@routers.post("/")

def login(request : OAuth2PasswordRequestForm = Depends() , db : Session = Depends(get_db)):
    user  = db.query(User).filter(User.username == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invaild Cranditals")
    

    if not Hash.verfiy(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Increated Password")
    

   
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token":access_token, "token_type":"bearer"}
    