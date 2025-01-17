from fastapi import APIRouter,Form ,File,UploadFile ,Depends,HTTPException
from typing import Optional
from fastapi.staticfiles import StaticFiles
from schemas import ProductModel
from models import Product
from database import get_db
from sqlalchemy.orm import Session
from uuid import uuid4
import os
from typing import List




routers = APIRouter(
    prefix="/api/v1/products",
    tags=["Product"]
)


routers.mount("/uploads", StaticFiles(directory="uploads"), name="uploads") 
UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@routers.post("/", response_model=ProductModel)
async def create_product(
    name : str = Form(...),
    selling_price : float = Form(...),
    description : Optional[str] = Form(None),
    cost_price : str = Form(...),
    stock : int = Form(...),
    supplier_id : int = Form(...),
    category_id : int = Form(...),
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
    
    new_product = Product(name=name, selling_price=selling_price, stock=stock, description=description, cost_price=cost_price, supplier_id=supplier_id, category_id=category_id, image=image_url)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@routers.get("/", response_model=List[ProductModel])
async def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products
