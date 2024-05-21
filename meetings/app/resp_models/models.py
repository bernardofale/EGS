from sqlmodel import Field, SQLModel, Relationship
from pydantic import ConfigDict, BaseModel, validator
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
    # To-Do ID of the To-Do associated with the meeting
    todo_id: str | None = None
    # List of attendees for the Meeting --
    # Actually not a column in the database
    attendees: List["MeetingAttendees"] = Relationship(
        back_populates="meeting")

    model_config = ConfigDict(json_schema_extra={
                                                    "id": "af5c3b3964fb4708b3",
                                                    "title": "Example",
                                                    "location": "null",
                                                    "date": "2024-02-26",
                                                    "attendees": "null",
                                                    "created_by": "a76a5d67fsf"
                                                }
                              )


class MeetingAttendees(SQLModel, table=True):
    # GUID
    id: str = Field(default_factory=lambda: uuid4().hex, primary_key=True)
    # Meeting ID
    meeting_id: str = Field(foreign_key="meeting.id")
    # User ID of the user that will attend the meeting
    user_id: str
    # Status of the attendee -> Accepted, Maybe, Pending, Declined
    status: str = Field(default="pending")
    # Meeting object -- Actually not a column in the database
    meeting: Meeting = Relationship(back_populates="attendees")

    model_config = ConfigDict(json_schema_extra={
                                                    "id": "af5c3b3964fb4708b",
                                                    "meeting_id": "a76a5d67f",
                                                    "user_id": "a76a5d67fsfsda"
                                                  })


class Attendees(BaseModel):
    user_id: str
    status: str = "pending"


class MeetingUpdate(BaseModel):
    title: str
    location: str | None = None
    start_date: datetime
    end_date: datetime = Field(default_factory=lambda: datetime.today())
    attendees: List[Attendees]
    todo_id: str | None = None

    @validator("start_date", always=True)
    def start_date_cannot_be_in_the_past(cls, v):
        if v.timestamp() < datetime.today().timestamp():
            raise ValueError("Meeting start date cannot be in the past")
        return v


class MeetingReceive(BaseModel):
    #id: str = Field(default_factory=lambda: uuid4().hex)
    title: str
    location: str | None = None
    start_date: datetime
    end_date: datetime
    todo_id: str | None = None
    attendees: List[Attendees]
    created_by: str

    @validator("start_date", always=True)
    def start_date_cannot_be_in_the_past(cls, v):
        if v.timestamp() < datetime.today().timestamp():
            raise ValueError("Meeting start date cannot be in the past")
        return v

    @validator("end_date", always=True)
    def end_date_cannot_be_before_start_date(cls, v, values):
        if "start_date" in values and v < values["start_date"]:
            raise ValueError("Meeting end date cannot be before start date")
        return v


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
    # HelloSign signature request ID
    signature_request_id: str | None = None
    # Meeting ID of the meeting the document is associated with
    meeting_id: str = Field(foreign_key="meeting.id")
    model_config = ConfigDict(json_schema_extra={
                                                    "id": "af5c3b3964fb4708b3",
                                                    "name": "document.pdf",
                                                    "content_type": "imag/png",
                                                    "signed": False,
                                                    "uploaded_by": "a76a5d67f"
                                                  }
                              )


class DocumentResponse(BaseModel):
    id: str
    name: str
    content_type: str
    signed: bool
    uploaded_by: str
    meeting_id: str


class DocumentSign(BaseModel):
    # User email
    user_email: str
    # User name
    user_name: str
    # Document subject
    subject: str
    # Message
    message: str
