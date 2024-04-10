from fastapi import Depends
from fastapi_utilities import repeat_every
import os
from dotenv import load_dotenv
from db.crud import telergamcrud
from db.schemas import telegramchema
from sqlalchemy.orm import Session
import httpx
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
db = SessionLocal()

app = FastAPI(title="Telegram Chronjob")

load_dotenv()

TOKEN = os.getenv("TOKEN")  # Telegram Bot API Key


@app.on_event('startup')
@repeat_every(seconds=60*5)
async def cronjob():
    API_URL = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL)
    try:
        chat_ids = telergamcrud.get_Telegram_chat_ids(db = db)
        for r in response.json()['result']:
            if r['message']['chat']['id'] not in chat_ids:
                chat_ids.append(r['message']['chat']['id'])

                telergamcrud.create_Telegram(db=db,
                                     telegram=telegramchema.TelegramBase(username=r['message']['chat']['username'],
                                                                     chat_id=r['message']['chat']['id'],
                                                                     first_name=r['message']['chat']['first_name'],
                                                                     last_name=r['message']['chat']['last_name']))
                print("Chat created with id:"+str(r['message']['chat']['id']))

    except Exception as e:
        print(e)