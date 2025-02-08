import uvicorn
from fastapi import FastAPI 
from database import engine
import models
from fastapi.middleware.cors import CORSMiddleware
from routers import users, suppliers, category, customer, products, transaction, cash, login, dayClosed
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
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(suppliers.router)
app.include_router(category.router)
app.include_router(customer.router)
app.include_router(products.router)
app.include_router(transaction.router)
app.include_router(cash.router)
app.include_router(login.router)
app.include_router(dayClosed.router)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Use PORT env variable for Render
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
