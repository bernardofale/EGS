from sqlmodel import create_engine, SQLModel
import os

DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASE_URL = "postgresql://postgres:example@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
