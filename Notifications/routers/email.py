from fastapi import APIRouter, Body,Header, Depends, HTTPException
import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
from starlette.responses import JSONResponse
from pydantic import BaseModel
from typing import Literal, Annotated
from ..db.crud import usercrud
from ..db.database import get_db
from sqlalchemy.orm import Session

_TYPES = Literal["html", "plain"]
load_dotenv()
class Envs:
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_FROM_NAME = os.getenv('MAIN_FROM_NAME')

class EmailSchema(BaseModel):
    name: str | None = ""
    subject: str | None = ""
    recipients: list | str
    cc: list | None = []
    bcc: list | None = []
    reply_to: list | None = []
    charset: str | None = "UTF-8"
    body: str
    alternative_body: str | None = ""
    attachments: list | None = []
    subtype: _TYPES | None = "plain"




conf = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_FROM,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,
    USE_CREDENTIALS=True,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS = False,
    )


router = APIRouter()

async def send_email_async(email_body: EmailSchema):

    if isinstance(email_body.recipients, str):
        a = []
        email_body.recipients = [email_body.recipients]

    message = MessageSchema(
        subject=email_body.subject,
        recipients=email_body.recipients,
        body=email_body.body,
        subtype=email_body.subtype,
        cc=email_body.cc,
        bcc=email_body.bcc,
        reply_to=email_body.reply_to,
        charset=email_body.charset,
        alternative_body=email_body.alternative_body,
        attachments=email_body.attachments
    )

    fm = FastMail(conf)
    await fm.send_message(message)


@router.post("/", status_code=200)
async def send_email_asynchronous(email_body: Annotated[
    EmailSchema,
    Body(openapi_examples={
            "normal" : {
                "summary": "A Normal Example",
                "description": "A **normal** item works correctly.",
                "value": {
                        "name": "Filipe Vale",
                        "subject": "Teste",
                        "recipients": "fmmvale@hotmail.com",
                        "body": "Hello, this is a test",
                },
            },
            "Full" : {
                "summary": "A Full Example",
                "description": "A **Full** item works correctly.",
                "value": {
                        "name": "Filipe Vale",
                        "subject": "Test Email",
                        "recipients": "fmmvale@hotmail.com",
                        "body": "<html><body>Hello,<p>this is a test.</p></body></html>",
                        "cc":["bernardo.marcal@ua.pt", "filipe.vale@ua.pt"],
                        "bcc":["diogo.correia99@ua.pt"],
                        "reply_to": [""],
                        "charset":"UTF-8",
                        "alternative_body": "Hello, this is a test",
                        "subtype":"html",
                        "attatchments":["attachments"],

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
        await send_email_async(email_body)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={'error': "Internal server error"})
    return 'Email Sent with Success'

