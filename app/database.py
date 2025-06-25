from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


load_dotenv()  # Load from .env


DB_URL = os.getenv("DATABASE_URL")


if DB_URL is None:
    raise ValueError("❌ DATABASE_URL is not set. Please check your .env file.")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
