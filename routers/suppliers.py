from fastapi import APIRouter,Form ,File,UploadFile ,Depends,HTTPException
from fastapi.staticfiles import StaticFiles
from schemas import SupplierModel
from models import Supplier
from database import get_db
from sqlalchemy.orm import Session
from uuid import uuid4
import os
from typing import List
from oauth2 import get_current_user



routers = APIRouter(
    prefix="/api/v1/suppliers",
    tags=["Supplier"]
)


routers.mount("/uploads", StaticFiles(directory="uploads"), name="uploads") 
UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@routers.post("/")
async def create_supplier(
    name : str = Form(...),
    contact : str = Form(...),
    email : str = Form(...),
    address : str = Form(...),
    upload_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user:SupplierModel = Depends(get_current_user)
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
    new_supplier = Supplier(name=name, contact=contact,email=email,address=address, image= image_url)
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    return new_supplier



@routers.get("/", response_model=List[SupplierModel])
async def get_supplier(db: Session = Depends(get_db),current_user:SupplierModel = Depends(get_current_user)):
    suppliers = db.query(Supplier).all()
    return suppliers


@routers.get("/{id}", response_model=SupplierModel)
async def get_supplier_by_id(id: int, db: Session = Depends(get_db),current_user:SupplierModel = Depends(get_current_user)):
    supplier = db.query(Supplier).filter(Supplier.id == id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier
@routers.put('/{id}', response_model=SupplierModel)

async def update_supplier(id:int , name : str = Form(...),
    contact : str = Form(...),
    email : str = Form(...),
    address : str = Form(...),
    upload_file: UploadFile = File(...),
    db: Session = Depends(get_db)):
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
    

    update_supplier = db.query(Supplier).filter(Supplier.id == id).first()
    if not update_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    update_supplier.name = name
    update_supplier.contact = contact
    update_supplier.email = email
    update_supplier.address = address
    update_supplier.image = image_url
    
    db.commit()
    db.refresh(update_supplier)
    return "update_supplier done"


@routers.delete("/{id}",response_model=SupplierModel)


async def delete_supplier(id : int, db: Session = Depends(get_db),current_user:SupplierModel = Depends(get_current_user)):
    delete_supplier = db.query(Supplier).filter(Supplier.id == id).first()
    if not delete_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db.delete(delete_supplier)
    db.commit()
    return delete_supplier
