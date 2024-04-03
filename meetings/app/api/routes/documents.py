from fastapi import APIRouter, Query, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from app.resp_models.models import Document, DocumentResponse
from app.db.database import engine
from sqlmodel import Session, select
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from tempfile import NamedTemporaryFile

app = APIRouter()


@app.post("/upload", status_code=201)
async def upload_document(user_id: str, meeting_id: str, file: UploadFile = File(...)):
    # Mock function to upload document to the database
    new_doc = Document(name=file.filename, content_type=file.content_type, content=bytes(file.file.read()), signed=False, uploaded_by=user_id, meeting_id=meeting_id)
    with Session(engine) as session:
        session.add(new_doc)
        session.commit()
        session.refresh(new_doc)
    return DocumentResponse(id=new_doc.id, name=new_doc.name, content_type=new_doc.content_type, signed=False, uploaded_by=new_doc.uploaded_by, meeting_id=new_doc.meeting_id)


@app.get("/", status_code=200)
async def get_all_documents(user_id: str = Query(None)):
    # Function to retrieve all documents of given user from the database
    with Session(engine) as session:
        results = session.exec(select(Document).where(Document.uploaded_by == user_id)).all()
        if len(results) == 0:
            raise HTTPException(status_code=404, detail="ERROR: No documents found for this user")
        docs = [DocumentResponse(id=doc.id, name=doc.name, content_type=doc.content_type, signed=doc.signed, uploaded_by=doc.uploaded_by, meeting_id=doc.meeting_id) for doc in results]
        return docs


def delete_tempfile(file_path: str):
    import os
    os.unlink(file_path)


@app.get("/{document_id}", status_code=200)
async def get_document(background_tasks: BackgroundTasks, document_id: str, user_id: str = Query(None)):
    # Function to retrieve a document from the database
    with Session(engine) as session:
        try:
            results = session.exec(select(Document).where(Document.id == document_id)).one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="ERROR: No document found")
        except MultipleResultsFound:
            raise HTTPException(status_code=500, detail="ERROR: Multiple documents found")

        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(results.content)
            background_tasks.add_task(delete_tempfile, temp_file.name)
            return FileResponse(temp_file.name, media_type=results.content_type, filename=results.name)


@app.get("/m/{meeting_id}", status_code=200)
async def get_documents_by_meeting(meeting_id: str):
    # Function to retrieve all documents of a meeting from the database
    with Session(engine) as session:
        results = session.exec(select(Document).where(Document.meeting_id == meeting_id)).all()
        if len(results) == 0:
            raise HTTPException(status_code=404, detail="ERROR: No documents found for this meeting")
        docs = [DocumentResponse(id=doc.id, name=doc.name, content_type=doc.content_type, signed=doc.signed, uploaded_by=doc.uploaded_by, meeting_id=doc.meeting_id) for doc in results]
        return docs


@app.delete("/{document_id}", status_code=204)
async def delete_document(document_id: str):
    # Check if document exists
    with Session(engine) as session:
        results = session.exec(select(Document).where(Document.id == document_id))
        if results is None:
            raise HTTPException(status_code=404, detail="No document found")
        session.delete(results.one())
        session.commit()


@app.post("/{document_id}/sign/", status_code=200)
async def sign_document(document_id: int, signature: str):
    # Mock function to sign a document
    return {"document_id": document_id, "signature": signature}
