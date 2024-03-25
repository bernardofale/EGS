from fastapi import APIRouter, Query, UploadFile, File
from app.resp_models.models import Document

app = APIRouter()


@app.post("/upload", status_code=201)
async def upload_document(user_id: str, file: UploadFile = File(...)) -> Document:
    # Mock function to upload document to the database
    return Document(name=file.filename, content_type=file.content_type, content=bytes(), signed=False, uploaded_by="bernardo")


@app.get("/", status_code=200)
async def get_all_documents(user_id: str = Query(None)):
    return


@app.get("/{document_id}", status_code=200)
async def get_document(document_id: str, user_id: str = Query(None)):
    return {"message": document_id}


@app.delete("/{document_id}", status_code=204)
async def delete_document(document_id: str):
    # Check if document exists
    return {"message": "Document deleted"}


@app.put("/{document_id}", status_code=200)
async def update_document(document_id: str, updated_content: UploadFile = File(...)):
    # Check if document exists
    return {"message": "Document updated successfully"}


@app.post("/{document_id}/sign/", status_code=200)
async def sign_document(document_id: int, signature: str):
    # Mock function to sign a document
    return {"document_id": document_id, "signature": signature}
