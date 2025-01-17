from fastapi import FastAPI 
from database import  engine
import models
from fastapi.middleware.cors import CORSMiddleware
from routers import users,suppliers,category,customer,products,transaction

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*', 'http://localhost:3000'],
    allow_credentials=True,
)

models.Base.metadata.create_all(bind=engine)

app.include_router(users.routers)
app.include_router(suppliers.routers)
app.include_router(category.routers)
app.include_router(customer.routers)
app.include_router(products.routers)
app.include_router(transaction.routers)


