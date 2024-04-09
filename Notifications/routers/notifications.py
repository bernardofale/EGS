from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Header, Depends,Body
from fastapi import APIRouter
from pydantic import BaseModel
from ..db.crud import usercrud, telergamcrud
from ..db.database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from .email import send_email_async, EmailSchema
from .telegram import sendTgMessage, TelegramMessageSchema
import re
from starlette.responses import JSONResponse

router = APIRouter()

class NotifySchema(BaseModel):
    poc: str #point of contact
    body: str

def validate_email(email:str):
    if re.match(r'[\w.]+\@[\w.]+', email):
        return True
    return False

def validate_telegram(teegram_id:str, db:Session):
    telegram = telergamcrud.get_Telegram_by_username(db, teegram_id)
    if telegram :
        return str(telegram.id)
    return False


@router.post("/",  status_code=200)
async def sendNotification(notify_body: Annotated[
    NotifySchema,
    Body(openapi_examples={
            "email" : {
                "summary": "A Email Example",
                "description": "A **normal** Email works correctly.",
                "value": {
                        "poc": "filipevale@ua.pt",
                        "body": "Hello, this is a test",
                },
            },
            "Telegram" : {
                "summary": "A Telegram Example",
                "description": "A **normal** Telegram works correctly.",
                "value": {
                        "poc": "FilipeMiguelVale",
                        "body": "Hello, this is a test",
                },
            },
        }
    )
    ],api_key: Annotated[str, Header()], db: Session = Depends(get_db)):
    try:
        db_user = usercrud.check_api_key(db, api_key=api_key)
        if not db_user:
            return HTTPException(status_code=400, detail="Invalid Api Key")

        if (validate_email(notify_body.poc)):
            email = EmailSchema(recipients=notify_body.poc, body=notify_body.body)
            await send_email_async(email)
            return JSONResponse(status_code=200, content={'ok': "Email sent successfully"})
        chat_id = validate_telegram(notify_body.poc, db)
        if (chat_id):
            tg = TelegramMessageSchema(chat_id=chat_id, body=notify_body.body)
            await sendTgMessage(tg)
            return JSONResponse(status_code=200, content={'ok': "Telegram sent successfully"})

    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={'error': "Internal server error"})
    return JSONResponse(status_code=500, content={'error': "Internal server error"})

