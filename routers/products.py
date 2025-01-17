from fastapi import APIRouter,Form ,File,UploadFile ,Depends,HTTPException,status
from typing import Optional
from fastapi.staticfiles import StaticFiles
from models import Product
from database import get_db
from sqlalchemy.orm import Session
from uuid import uuid4
import os
from typing import List
from schemas import ShowProductBaseModel



routers = APIRouter(
    prefix="/api/v1/products",
    tags=["Product"]
)


routers.mount("/uploads", StaticFiles(directory="uploads"), name="uploads") 
UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@routers.post("/")
async def create_product(
    name : str = Form(...),
    selling_price : float = Form(...),
    description : Optional[str] = Form(None),
    cost_price : str = Form(...),
    stock : int = Form(...),
    supplier_id : int = Form(...),
    product_id : int = Form(...),
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
    
    new_product = Product(name=name, selling_price=selling_price, stock=stock, description=description, cost_price=cost_price, supplier_id=supplier_id, product_id=product_id, image=image_url)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@routers.get("/", response_model=List[ShowProductBaseModel])
async def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products



@routers.put("/{id}",response_model=ShowProductBaseModel)

async def update(
    id:int,
    name : str = Form(...),
    selling_price : float = Form(...),
    description : Optional[str] = Form(None),
    cost_price : str = Form(...),
    stock : int = Form(...),
    supplier_id : int = Form(...),
    product_id : int = Form(...),
    upload_file: UploadFile = File(...),
    db:Session = Depends(get_db)):
    
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
    
    update_product = db.query(Product).filter(Product.id == id).first()
    if not update_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"product {id} is not found")
    
    update_product.name = name
    update_product.image = image_url
    update_product.selling_price = selling_price
    update_product.cost_price = cost_price
    update_product.supplier_id = supplier_id
    update_product.product_id = product_id
    update_product.stock = stock
    update_product.description = description
    
    db.commit()
    db.refresh(update_product)
    return "update product done"


@routers.delete("/{id}")
async def delete(id:int,db : Session = Depends(get_db)):
    product_delete = db.query(Product).filter(Product.id ==id).first()
    if not product_delete :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"product{id} is not found")
    db.delete(product_delete)
    db.commit()
    return "product is delete successfully done"



