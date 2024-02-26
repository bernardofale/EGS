from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from resp_models.models import Meeting, Document

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/v1/meetings/", tags=["meetings"], status_code=200)
async def get_all_meetings(user_id: str = Query(None)) -> Meeting:
    # Mock function to retrieve all meetings from the database
    return Meeting(title = "Ponto de situação", created_by = "bernardo")

# Other endpoints remain unchanged
@app.get("/v1/meetings/{meeting_id}", tags=["meetings"], status_code=200)
async def get_meeting(meeting_id: str, user_id: str = Query(None)) -> Meeting:
    # Mock function to retrieve meeting details from the database
    #if meeting.id == meeting_id:
    #       return meeting
    #raise HTTPException(status_code=404, detail="Meeting not found")
    return Meeting(title = "Ponto de situação", created_by = "bernardo")

@app.post("/v1/meetings/", tags=["meetings"], status_code=201)
async def create_meeting(meeting: Meeting):
    # Mock function to create a new meeting
    return {"message": "Meeting created successfully"}

@app.put("/v1/meetings/{meeting_id}", tags=["meetings"], status_code=200)
async def update_meeting(meeting_id: str) -> Meeting:
    # Mock function to update an existing meetingreturn {"message": f"Meeting {meeting_id} updateVVd successfully"}
    return Meeting(title = "Ponto de situação", created_by = "bernardo")

@app.delete("/v1/meetings/{meeting_id}", tags=["meetings"], status_code=204)
async def delete_meeting(meeting_id: str):
    # Mock function to delete a meeting
    return {"message": f"Meeting {meeting_id} deleted successfully"}

@app.post("/v1/documents/upload", tags=["documents"], status_code=201)
async def upload_document(user_id: str, file: UploadFile = File(...)) -> Document:
    # Mock function to upload document to the database
    document_id = 123  # ID assigned by the database
    return Document(name = file.filename, content_type = file.content_type, signed = False, uploaded_by = "bernardo" ) 

@app.get("/v1/documents/", tags = ["documents"], status_code = 200)
async def get_all_documents(user_id: str = Query(None)):
    return

@app.get("/v1/documents/{document_id}", tags = ["documents"], status_code = 200)
async def get_all_documents(document_id: str):
    return { "message" : document_id }

@app.delete("/v1/documents/{document_id}", tags=["documents"], status_code=204)
async def delete_document(document_id: str):
    # Check if document exists
    return { "message": "Document deleted" }

@app.put("/v1/documents/{document_id}", tags=["documents"], status_code=200)
async def update_document(document_id: str, updated_content: UploadFile = File(...)):
    # Check if document exists
    return {"message": "Document updated successfully" }

@app.post("/v1/documents/{document_id}/sign/", tags=["documents"], status_code=200)
async def sign_document(document_id: int, signature: str):
    # Mock function to sign a document
    return {"document_id": document_id, "signature": signature}
