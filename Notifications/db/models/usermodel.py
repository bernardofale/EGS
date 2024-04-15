from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    api_key = Column(String, unique=True,)
    username = Column(String, unique=True, index=True)
    name_of_service = Column(String)
    is_active = Column(Boolean, default=True)

