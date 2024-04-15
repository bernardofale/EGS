from sqlalchemy.orm import Session

from ..models import usermodel
from ..schemas import userschema
from hashlib import sha256

def get_user(db: Session, user_id: int):
    return db.query(usermodel.User).filter(usermodel.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(usermodel.User).filter(usermodel.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(usermodel.User).offset(skip).limit(limit).all()

def check_api_key(db: Session, api_key:str):
    return db.query(usermodel.User).filter(usermodel.User.api_key == api_key).first()

def create_user(db: Session, user: userschema.UserBase):
    fake_hashed_username = user.username #+ "notreallyhashed"
    db_user = usermodel.User(name_of_service=user.name_of_service, username=fake_hashed_username,
                             api_key=sha256(fake_hashed_username.encode()).hexdigest())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
