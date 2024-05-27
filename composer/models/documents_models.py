from sqlmodel import Field, SQLModel
from pydantic import ConfigDict, BaseModel
from uuid import uuid4


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


class DocumentSign(BaseModel):
    # User email
    user_email: str
    # User name
    user_name: str
    # Document subject
    subject: str
    # Message
    message: str
