from fastapi import FastAPI 
from database import  engine
import models
from fastapi.middleware.cors import CORSMiddleware
from routers import users,suppliers,category,customer,products,transaction,cash,login,dayClosed
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


models.Base.metadata.create_all(bind=engine)

app.include_router(users.routers)
app.include_router(suppliers.routers)
app.include_router(category.routers)
app.include_router(customer.routers)
app.include_router(products.routers)
app.include_router(transaction.routers)
app.include_router(cash.routers)
app.include_router(login.routers)
app.include_router(dayClosed.routers)

