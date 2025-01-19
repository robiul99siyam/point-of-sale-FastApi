from fastapi import APIRouter,Form ,File,UploadFile ,Depends,HTTPException,status
from fastapi.staticfiles import StaticFiles
from schemas import CustomModel
from models import Customer
from database import get_db
from sqlalchemy.orm import Session
from uuid import uuid4
import os
from typing import List
from oauth2 import get_current_user



routers = APIRouter(
    prefix="/api/v1/customers",
    tags=["Customer"]
)


routers.mount("/uploads", StaticFiles(directory="uploads"), name="uploads") 
UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)



@routers.get("/",response_model=List[CustomModel])

async def get_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    return customers

@routers.post("/", response_model= CustomModel)

async def create_customer(
    name : str = Form(...),
    phone : str = Form(...),
    email : str = Form(...),
    address : str = Form(...),
    upload_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if upload_file:
        file_extension = os.path.splitext(upload_file.filename)[-1]
        if file_extension.lower() not in [".jpg", ".jpeg", ".png"]:
            raise HTTPException(status_code=400, detail="Invalid image format. Only JPG, JPEG, and PNG are allowed.")

        filename = f"{uuid4().hex}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        # Write the file to the uploads directory
        with open(file_path, "wb") as f:
            f.write(await upload_file.read())

        image_url = file_path  # Store the file path as the image URL
    else:
        image_url = None
    
    new_customer = Customer(name=name, phone=phone, email=email, address=address, image=image_url)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer 






@routers.put("/{id}",response_model=CustomModel)

async def update(
    id:int,
    name : str = Form(...),
    upload_file: UploadFile = File(...), 
    db:Session = Depends(get_db)
    ):
    
    if upload_file:
        file_extension = os.path.splitext(upload_file.filename)[-1]
        if file_extension.lower() not in [".jpg", ".jpeg", ".png"]:
            raise HTTPException(status_code=400, detail="Invalid image format. Only JPG, JPEG, and PNG are allowed.")

        filename = f"{uuid4().hex}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        # Write the file to the uploads directory
        with open(file_path, "wb") as f:
            f.write(await upload_file.read())

        image_url = file_path  # Store the file path as the image URL
    else:
        image_url = None   
    
    update_customer = db.query(Customer).filter(Customer.id == id).first()
    if not update_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"customer {id} is not found")
    
    update_customer.name = name
    update_customer.image = image_url
    db.commit()
    db.refresh(update_customer)
    return "update customer done"


@routers.delete("/{id}")
async def delete(id:int,db : Session = Depends(get_db)):
    customer_delete = db.query(Customer).filter(Customer.id ==id).first()
    if not customer_delete :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"customer{id} is not found")
    db.delete(customer_delete)
    db.commit()
    return "customer is delete successfully done"

