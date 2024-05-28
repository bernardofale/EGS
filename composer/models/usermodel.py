from pydantic import BaseModel
from typing import Literal


_TYPES = Literal["html", "plain"]


class EmailSchema(BaseModel):
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
