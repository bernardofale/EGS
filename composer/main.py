from typing import List, Optional
from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel, EmailStr

app = FastAPI()


todo_service_url = "http://egs-todo_api:8002"
meetings_service_url = "http://egs-meetings-docs-api:80"
documents_service_url = "http://egs-notification_service:8000"


# Helper function to make requests
def make_request(url, method="GET", data=None):
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500,
                            detail="An error occurred while fetching data")


@app.get("/todos")
def get_todos(completed: Optional[bool] = None,
              priority: Optional[int] = None,
              due_date: Optional[str] = None,
              sort_by_due_date: Optional[str] = None):
    url = f"{todo_service_url}/v1/todos"
    params = {
        "completed": completed,
        "priority": priority,
        "due_date": due_date,
        "sort_by_due_date": sort_by_due_date
    }
    return make_request(url, params=params)


@app.post("/todos")
def create_todo(todo_data: dict):
    url = f"{todo_service_url}/v1/todos"
    return make_request(url, method="POST", data=todo_data)


@app.get("/todos/{todo_id}")
def get_todo_by_id(todo_id: int):
    url = f"{todo_service_url}/v1/todos/{todo_id}"
    return make_request(url)


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo_data: dict):
    url = f"{todo_service_url}/v1/todos/{todo_id}"
    return make_request(url, method="PUT", data=todo_data)


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    url = f"{todo_service_url}/v1/todos/{todo_id}"
    return make_request(url, method="DELETE")


# Meetings endpoints
@app.get("/meetings")
def get_meetings(user_id: Optional[str] = None):
    url = f"{meetings_service_url}/meetings"
    params = {"user_id": user_id}
    return make_request(url, params=params)


@app.get("/meetings/{meeting_id}")
def get_meeting(meeting_id: str):
    url = f"{meetings_service_url}/meetings/{meeting_id}"
    return make_request(url)


@app.post("/meetings")
def create_meeting(meeting_data: dict):
    url = f"{meetings_service_url}/meetings/"
    meeting = make_request(url, method="POST", data=meeting_data)
    return meeting


@app.put("/meetings/{meeting_id}")
def update_meeting(meeting_id: str, meeting_data: dict):
    url = f"{meetings_service_url}/meetings/{meeting_id}"
    return make_request(url, method="PUT", data=meeting_data)


@app.delete("/meetings/{meeting_id}")
def delete_meeting(meeting_id: str):
    url = f"{meetings_service_url}/meetings/{meeting_id}"
    return make_request(url, method="DELETE")


@app.get("/documents")
def get_documents(user_id: Optional[str] = None):
    url = f"{documents_service_url}/documents/"
    params = {"user_id": user_id}
    return make_request(url, params=params)


@app.get("/documents/{document_id}")
def get_document(document_id: str, user_id: Optional[str] = None):
    url = f"{documents_service_url}/documents/{document_id}"
    params = {"user_id": user_id}
    return make_request(url, params=params)


@app.post("/documents/upload")
def upload_document(user_id: str, meeting_id: str, file: bytes):
    url = f"{documents_service_url}/documents/upload"
    files = {"file": file}
    params = {"user_id": user_id, "meeting_id": meeting_id}
    return make_request(url, method="POST", data=files, params=params)


@app.get("/documents/m/{meeting_id}")
def get_documents_by_meeting(meeting_id: str):
    url = f"{documents_service_url}/documents/m/{meeting_id}"
    return make_request(url)


@app.post("/documents/{document_id}/sign")
def sign_document(document_id: str, sign_data: dict):
    url = f"{documents_service_url}/documents/{document_id}/sign/"
    return make_request(url, method="POST", data=sign_data)


@app.post("/documents/{document_id}/sign/verify")
def verify_document(document_id: str):
    url = f"{documents_service_url}/documents/{document_id}/sign/verify"
    return make_request(url, method="POST")


@app.get("/documents/{document_id}/download")
def download_document(document_id: str):
    url = f"{documents_service_url}/documents/{document_id}/download"
    return make_request(url)
