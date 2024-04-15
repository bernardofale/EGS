from sqlalchemy.orm import Session

from ..models import telegrammodel
from ..schemas import telegramchema


def get_Telegram(db: Session, telegram_id: int):
    return db.query(telegrammodel.Telegram).filter(telegrammodel.Telegram.id == telegram_id).first()

def get_Telegram_by_username(db: Session, telegram_username: str):
    return db.query(telegrammodel.Telegram).filter(telegrammodel.Telegram.username == telegram_username).first()


def get_Telegram_by_Telegramname(db: Session, telegramname: str):
    return db.query(telegrammodel.Telegram).filter(telegrammodel.Telegram.Telegramname == telegramname).first()


def get_Telegrams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(telegrammodel.Telegram).offset(skip).limit(limit).all()

def get_Telegram_chat_ids(db: Session):
    return [r for r, in db.query(telegrammodel.Telegram.id).all()]

def create_Telegram(db: Session, telegram: telegramchema.TelegramBase):
    db_Telegram = telegrammodel.Telegram(username=telegram.username,id=telegram.chat_id,
                                         first_name=telegram.first_name,last_name=telegram.last_name)
    db.add(db_Telegram)
    db.commit()
    db.refresh(db_Telegram)
    return db_Telegram
