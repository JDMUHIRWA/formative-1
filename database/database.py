# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv  # type: ignore

load_dotenv()

POSTGRES_URL = os.getenv("POSTGRES_URL")

if not POSTGRES_URL:
    raise RuntimeError("POSTGRES_URL is not set. Add it to your .env file (e.g. POSTGRES_URL=postgresql://user:pass@host:port/dbname)")

# If using sqlite for local testing, pass connect_args
connect_args = {}
if POSTGRES_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(POSTGRES_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
