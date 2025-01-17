from fastapi import APIRouter,Form ,File,UploadFile ,Depends,HTTPException
from fastapi.staticfiles import StaticFiles
from schemas import CategoryModel
from models import Category
from database import get_db
from sqlalchemy.orm import Session
from uuid import uuid4
import os
from typing import List


routers = APIRouter(
    prefix="/api/v1/categories",
    tags=["Category"]
)


routers.mount("/uploads", StaticFiles(directory="uploads"), name="uploads") 
UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@routers.post("/", response_model=CategoryModel)
async def create_category(
    name : str = Form(...),
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
    
    new_category = Category(name=name, image=image_url)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category



@routers.get('/',response_model= List[CategoryModel])

async def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories
