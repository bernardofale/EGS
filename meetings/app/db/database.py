from sqlmodel import create_engine, SQLModel
from dotenv import load_dotenv
import os

load_dotenv()

PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")

SQLALCHEMY_DATABASE_URL = "postgresql://"+PG_USER+":"+PG_PASSWORD+"@localhost:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
