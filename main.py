from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form 
from sqlalchemy.orm import Session 
from typing import List,Optional
from database import SessionLocal, engine
import models
from fastapi.middleware.cors import CORSMiddleware
from models import User , Supplier, Category,Product,Transaction ,Customer
import os
from uuid import uuid4
from fastapi.staticfiles import StaticFiles
from schemas import UserModel, CategoryModel, ProductModel,SupplierModel,CustomModel,TransactionModel,UserAdminRole,PaymentRole
import uvicorn


app = FastAPI()
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads") 
UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*', 'http://localhost:3000'],
    allow_credentials=True,
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)


#########################  User api url ###########################################
@app.post('/api/users/', response_model=UserModel)
async def create_user(
    username: str = Form(...),
    password: str = Form(...),
    role: UserAdminRole = Form(...),
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

    # Create a new user
    new_user = User(username=username, password=password, role=role, image=image_url)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user





@app.get("/api/users/",response_model=List[UserModel])

async def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    
    return users

@app.get("/api/users/{id}", response_model=UserModel)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@app.put("/api/users/{id}",response_model=UserModel)

async def update_user(id:int, username: str = Form(...),
    password: str = Form(...),
    role: UserAdminRole = Form(...),
    upload_file: UploadFile = File(...),
    db : Session = Depends(get_db)):
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
    return user




@app.delete("/api/users/{id}" , response_model=UserModel)
async def delete_user(id : int,db : Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user


############################ supplier #########################




@app.post("/api/v1/suppliers", response_model=SupplierModel)
async def create_supplier(
    name : str = Form(...),
    contact : str = Form(...),
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
    new_supplier = Supplier(name=name, contact=contact,email=email,address=address, image= image_url)
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    return new_supplier



@app.get("/api/v1/suppliers", response_model=List[SupplierModel])
async def get_supplier(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    suppliers = db.query(Supplier).offset(skip).limit(limit).all()
    return suppliers


@app.get("/api/v1/suppliers/{id}", response_model=SupplierModel)
async def get_supplier_by_id(id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id == id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier
@app.put('/api/v1/suppliers/{id}', response_model=SupplierModel)

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
    return update_supplier


@app.delete("/api/suppliers/{id}",response_model=SupplierModel)


async def delete_supplier(id : int, db: Session = Depends(get_db)):
    delete_supplier = db.query(Supplier).filter(Supplier.id == id).first()
    if not delete_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db.delete(delete_supplier)
    db.commit()
    return delete_supplier
##################### Category #################################################

@app.post("/api/v1/categories", response_model=CategoryModel)
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



@app.get('/api/v1/category',response_model= List[CategoryModel])

async def get_categories(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories



################################# Customer Database Methods ############################


@app.get("/api/v1/customers",response_model=List[CustomModel])

async def get_customers(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    customers = db.query(models.Customer).offset(skip).limit(limit).all()
    return customers

@app.post("/api/v1/customers", response_model= CustomModel)

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


############################ Product Management Functions #########################


@app.post("/api/v1/products", response_model=ProductModel)
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


@app.get("/api/v1/products", response_model=List[ProductModel])
async def get_products(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products


################ translations #################################
@app.post("/api/v1/transactions", response_model=TransactionModel)
async def create_transaction(
    user_id: int = Form(...),
    product_id: int = Form(...),
    quantity: int = Form(...),
    unit_price: float = Form(...),
    subtotal: float = Form(...),
    customer_id: int = Form(...),
    payment_method: PaymentRole = Form(...),
    db: Session = Depends(get_db),
):
    # Fetch the product by ID
    product = db.query(Product).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check stock availability
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    
    # Deduct stock
    product.stock -= quantity
    
    # Validate subtotal
    calculated_subtotal = quantity * unit_price
    print(calculated_subtotal)
    if subtotal != calculated_subtotal:
        raise HTTPException(
            status_code=400, 
            detail=f"Subtotal mismatch. Expected: {calculated_subtotal}, Provided: {subtotal}"
        )

    # Create the transaction
    new_transaction = Transaction(
        subtotal=subtotal,
        quantity=quantity,
        unit_price=unit_price,
        user_id=user_id,
        customer_id=customer_id,
        product_id=product_id,
        payment_method=payment_method
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction


@app.get("/api/v1/transactions",response_model=List[TransactionModel])
async def get_transactions(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).offset(skip).limit(limit).all()
    return transactions





if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)