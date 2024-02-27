from pydantic import BaseModel, Field, ConfigDict
from uuid import uuid4
from typing import Optional

class Collaborator(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)  # GUID
    name: str
    position: str
    email: Optional[str] = None
    phone: Optional[str] = None
    birth_date: Optional[str] = None
    address: Optional[str] = None

    #etc...

    model_config = ConfigDict(json_schema_extra={
        "id": "af5c3b3964fb4708b3d4ad6b74ec62f6",
        "name": "Example",
        "position": "Developer",
        "email": "example@email.com",
        "phone": "912345789",
        "birth_date": "2001-12-03",
        "address": "123 Example Street",
    })
