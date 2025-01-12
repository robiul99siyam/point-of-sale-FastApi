from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the correct PostgreSQL connection URL
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:12345@localhost/point_of_sale"
# SQLALCHEMY_DATABASE_URL = "sqlite"

# Create the SQLAlchemy engine for PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session local instance
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for your models
Base = declarative_base()
