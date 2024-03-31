from sqlmodel import SQLModel, create_engine
from app.resp_models import models

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:example@localhost:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
