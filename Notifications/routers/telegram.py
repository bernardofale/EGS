from fastapi import APIRouter, Body,Header, Depends, HTTPException, Request
from fastapi_utilities import repeat_every
import os
from dotenv import load_dotenv
from starlette.responses import JSONResponse
from pydantic import BaseModel
from typing import Literal, Annotated
from ..db.crud import telergamcrud
from ..db.schemas import telegramchema
from ..db.crud import usercrud
from ..db.database import get_db
from sqlalchemy.orm import Session
import httpx

router = APIRouter()

load_dotenv()

TOKEN = os.getenv("TOKEN")  # Telegram Bot API Key

class TelegramMessageSchema(BaseModel):
    chat_id: str
    body: str

async def sendTgMessage(telegram_body: TelegramMessageSchema):
    """
      Sends the Message to telegram with the Telegram BOT API
      """

    tg_msg = {"chat_id": telegram_body.chat_id, "text": telegram_body.body, "parse_mode": "Markdown"}
    API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    print(tg_msg)
    print(TOKEN)
    async with httpx.AsyncClient() as client:
        try:
            await client.post(API_URL, json=tg_msg)
        except Exception as e:
            print(e)
            return JSONResponse(status_code=500, content={'error': "Internal server error"})

@router.post("/")
async def sendTelegram(telegram_body: Annotated[
    TelegramMessageSchema,
    Body(openapi_examples={
            "normal" : {
                "summary": "A Normal Example",
                "description": "A **normal** message works correctly.",
                "value": {
                        "chat_id": "6425928272",
                        "body": "Hello, this is a test",
                },
            },
        }
    )
    ],api_key: Annotated[str, Header()]
    , db: Session = Depends(get_db)
):
    try:
        db_user = usercrud.check_api_key(db, api_key=api_key)
        if not db_user:
            return HTTPException(status_code=400, detail="Invalid Api Key")
        await sendTgMessage(telegram_body)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={'error': "Internal server error"})
    return 'Telegram Sent with Success'

