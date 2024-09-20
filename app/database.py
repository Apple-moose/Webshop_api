import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "postgresql://postgres:secret@localhost:4000/postgres"
DATABASE_URL = os.getenv("DATABASE_URL")


# create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# create SessionLocal class with sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class, will use later to create models or classes
Base = declarative_base() 

