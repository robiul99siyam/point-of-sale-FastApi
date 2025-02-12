from fastapi import APIRouter,Form ,File,UploadFile ,Depends,HTTPException,status
from fastapi.staticfiles import StaticFiles
from schemas import UserAdminRole,ShowUserBaseModel,UserModel
from models import User
from database import get_db
from sqlalchemy.orm import Session
from uuid import uuid4
import os
from typing import List
from hashing import Hash
from oauth2 import get_current_user


routers = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


routers.mount("/uploads", StaticFiles(directory="uploads"), name="uploads") 
UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@routers.post('/')
async def create_user(
    username: str = Form(...),
    password: str = Form(...),
    role: UserAdminRole = Form(...),
    image: UploadFile = File(),
    db: Session = Depends(get_db),
):
    # Handle image upload
    if image:
        file_extension = os.path.splitext(image.filename)[-1].lower()
        if file_extension not in [".jpg", ".jpeg", ".png"]:
            raise HTTPException(status_code=400, detail="Invalid image format. Only JPG, JPEG, and PNG are allowed.")

        filename = f"{uuid4().hex}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(await image.read())

        image_url = f"/uploads/{filename}"  
    else:
        image_url = None

    # Convert Enum to string
    hashPassword = Hash.bcrypt(password)
    new_user = User(
        username=username,
        password=hashPassword,
        role=role.value,  
        image=image_url
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user




@routers.get("/",response_model=List[UserModel])

async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    
    return users

@routers.get("/{id}", response_model=UserModel)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@routers.put("/{id}",response_model=UserModel)

async def update_user(id:int, username: str = Form(...),
    password: str = Form(...),
    role: UserAdminRole = Form(...),
    upload_file: UploadFile = File(None),
    db : Session = Depends(get_db),
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

    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.username = username
    user.password =  password
    user.role = role
    user.image = image_url
    
    db.commit()
    db.refresh(user)
    return f"{id}Update Successfull done"





@routers.delete("/{id}" , response_model=UserModel)
async def delete_user(id : int,db : Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user
