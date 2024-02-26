from pydantic import BaseModel, Field, ConfigDict
from uuid import uuid4
from datetime import date
from typing import List

class Meeting(BaseModel):
    id: str = Field(default_factory = lambda: uuid4().hex) #GUID
    title: str
    location: str = Field(default = None)
    date: str = Field(default_factory = lambda: date.today().isoformat())
    atendees: List[str] = Field(default = None) #Set of user id's
    created_by: str #User ID 

    model_config = ConfigDict(json_schema_extra = {
                                        "id": "af5c3b3964fb4708b3d4ad6b74ec62f6",
                                        "title": "Example",
                                        "location": "null",
                                        "date": "2024-02-26",
                                        "attendees": "null",
                                        "created_by": "a76a5d67fsfsdafje8765"
                                        }
                                )

class Document(BaseModel):
    id: str = Field(default_factory = lambda: uuid4().hex) #GUID
    name: str
    content_type: str
    signed: bool = Field(default = False)
    uploaded_by: str 
    
    model_config = ConfigDict(json_schema_extra = {
                                        "id": "af5c3b3964fb4708b3d4ad6b74ec62f6",
                                        "name": "document.pdf",
                                        "content_type": "image/jpeg",
                                        "signed": False,
                                        "uploaded_by": "a76a5d67fsfsdafje8765"
                                        }
                                )

