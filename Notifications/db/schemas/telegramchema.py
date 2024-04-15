from pydantic import BaseModel

class TelegramBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    chat_id: int

class Telegram(TelegramBase):
    is_active: bool

    class Config:
        orm_mode = True