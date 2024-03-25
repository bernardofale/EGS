from sqlmodel import Field, SQLModel
from pydantic import ConfigDict, BaseModel
from uuid import uuid4
from datetime import datetime
from typing import List


class Meeting(SQLModel, table=True):
    # GUID
    id: str = Field(default_factory=lambda: uuid4().hex, primary_key=True)
    # Title of the meeting
    title: str
    # Location of the meeting
    location: str | None = None
    # Start date of the meeting
    start_date: datetime = Field(default_factory=lambda: datetime.today())
    # End date of the meeting
    end_date: datetime = Field(default_factory=lambda: datetime.today())
    # User ID of the user that created the meeting / Owner of User ID
    created_by: str
    model_config = ConfigDict(json_schema_extra={
                                                    "id": "af5c3b3964fb4708b3d4ad6b74ec62f6",
                                                    "title": "Example",
                                                    "location": "null",
                                                    "date": "2024-02-26",
                                                    "attendees": "null",
                                                    "created_by": "a76a5d67fsfsdafje8765"
                                                }
                              )


class MeetingAttendees(SQLModel, table=True):
    # GUID
    id: int | None = Field(default=None, primary_key=True)
    # Meeting ID
    meeting_id: str
    # User ID of the user that will attend the meeting
    user_id: str
    model_config = ConfigDict(json_schema_extra={
                                                    "id": "af5c3b3964fb4708b3d4ad6b74ec62f6",
                                                    "meeting_id": "a76a5d67fsfsdafje8765",
                                                    "user_id": "a76a5d67fsfsdafje8765"
                                                  })


class MeetingReceive(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    title: str
    location: str | None = None
    start_date: datetime
    end_date: datetime
    attendees: List[str]
    created_by: str


class Document(SQLModel, table=True):
    # GUID
    id: str = Field(default_factory=lambda: uuid4().hex, primary_key=True)
    # Name of the document
    name: str
    # Content type of the Document
    content_type: str
    # Content of the document
    content: bytes
    # If the document is signed or not
    signed: bool = Field(default=False)
    # User ID of the user that uploaded the document
    uploaded_by: str
    model_config = ConfigDict(json_schema_extra={
                                                    "id": "af5c3b3964fb4708b3d4ad6b74ec62f6",
                                                    "name": "document.pdf",
                                                    "content_type": "image/jpeg",
                                                    "signed": False,
                                                    "uploaded_by": "a76a5d67fsfsdafje8765"
                                                  }
                              )
