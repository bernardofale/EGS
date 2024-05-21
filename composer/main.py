from typing import Optional
from fastapi import FastAPI, HTTPException, Header, UploadFile, File
from fastapi.responses import StreamingResponse
import requests


app = FastAPI()


todo_service_url = "http://0.0.0.0:8002"
meetings_service_url = "http://0.0.0.0:80"  # + Docs API
notifications_service_url = "http://0.0.0.0:8000"


# Helper function to make requests
def make_request(url, method="GET", params=None, data=None, headers=None):
    try:
        if method == "GET":
            response = requests.get(url, params=params, headers=headers)
            print(response.request.url)
            print(response.request.headers)
        elif method == "POST":
            response = requests.post(url, files=data, json=params, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=params, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
            return "deleted"
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500,
                            detail=response.json())


# Todo endpoints
@app.get("/todos", tags=["Todo"])
def get_todos(completed: Optional[bool] = None,
              priority: Optional[int] = None,
              due_date: Optional[str] = None,
              sort_by_due_date: Optional[str] = None,
              api_key: Optional[str] = Header(None)):
    url = f"{todo_service_url}/v1/todos"
    params = {
        "completed": completed,
        "priority": priority,
        "due_date": due_date,
        "sort_by_due_date": sort_by_due_date
    }
    headers = {"api-key": api_key} if api_key else None
    return make_request(url, params=params, headers=headers)


@app.post("/todos", tags=["Todo"])
def create_todo(todo_data: dict, api_key: Optional[str] = Header(None)):
    url = f"{todo_service_url}/v1/todos"
    headers = {"api-key": api_key} if api_key else None
    return make_request(url, method="POST", params=todo_data, headers=headers)


@app.get("/todos/{todo_id}", tags=["Todo"])
def get_todo_by_id(todo_id: int, api_key: Optional[str] = Header(None)):
    url = f"{todo_service_url}/v1/todos/{todo_id}"
    headers = {"api-key": api_key} if api_key else None
    return make_request(url, headers=headers)


@app.put("/todos/{todo_id}", tags=["Todo"])
def update_todo(todo_id: int, todo_data: dict,
                api_key: Optional[str] = Header(None)):
    url = f"{todo_service_url}/v1/todos/{todo_id}"
    headers = {"api-key": api_key} if api_key else None
    return make_request(url, method="PUT", params=todo_data, headers=headers)


@app.delete("/todos/{todo_id}", tags=["Todo"])
def delete_todo(todo_id: int, api_key: Optional[str] = Header(None)):
    url = f"{todo_service_url}/v1/todos/{todo_id}"
    headers = {"api-key": api_key} if api_key else None
    return make_request(url, method="DELETE", headers=headers)


# Meetings endpoints
@app.get("/meetings", tags=["Meetings"])
def get_meetings(user_id: Optional[str] = None,
                 api_key: Optional[str] = Header(None)):
    url = f"{meetings_service_url}/meetings"
    params = {"user_id": user_id}
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None
    return make_request(url, params=params, headers=headers)


@app.get("/meetings/{meeting_id}", tags=["Meetings"])
def get_meeting(meeting_id: str,
                api_key: Optional[str] = Header(None)):
    url = f"{meetings_service_url}/meetings/{meeting_id}"
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None
    return make_request(url, headers=headers)


@app.post("/meetings", tags=["Meetings"])
def create_meeting(meeting_data: dict,
                   api_key: Optional[str] = Header(None)):
    url = f"{meetings_service_url}/meetings/"
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None
    meeting = make_request(url, method="POST", params=meeting_data,
                           headers=headers)
    return meeting


@app.put("/meetings/{meeting_id}", tags=["Meetings"])
def update_meeting(meeting_id: str, meeting_data: dict,
                   api_key: Optional[str] = Header(None)):
    url = f"{meetings_service_url}/meetings/{meeting_id}"
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None
    return make_request(url, method="PUT", params=meeting_data, headers=headers)


@app.delete("/meetings/{meeting_id}", tags=["Meetings"])
def delete_meeting(meeting_id: str,
                   api_key: Optional[str] = Header(None)):
    url = f"{meetings_service_url}/meetings/{meeting_id}"
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None
    return make_request(url, method="DELETE", headers=headers)


# Documents endpoints
@app.get("/documents", tags=["Documents"])
def get_documents(user_id: Optional[str] = None,
                  api_key: Optional[str] = Header(None)):
    url = f"{meetings_service_url}/documents/"
    params = {"user_id": user_id}
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None
    return make_request(url, params=params, headers=headers)


@app.get("/documents/{document_id}", tags=["Documents"])
def get_document(document_id: str, user_id: Optional[str] = None,
                 api_key: Optional[str] = Header(None)):
    url = f"{meetings_service_url}/documents/{document_id}"
    params = {"user_id": user_id}
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None

    # Send the request to your service
    response = requests.get(url, params=params, headers=headers)

    print(response.headers)
    # Raise an HTTPException if the request failed
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    # Get the file content and metadata from the response
    file_content = response.content
    file_type = response.headers["Content-Type"]
    content_disposition = response.headers["Content-Disposition"]
    filename_index = content_disposition.find("filename*=")
    if filename_index != -1:
        file_name = content_disposition.split("filename*=utf-8")[1].strip('"')
    else:
        file_name = content_disposition.split("filename=")[1].strip('"')
    # Create a StreamingResponse to return the file content as a downloadable file
    response = StreamingResponse(
        iter([file_content]),
        media_type=file_type
    )
    response.headers["Content-Disposition"] = f"attachment; filename={file_name}"

    return response


@app.post("/documents/upload", tags=["Documents"])
def upload_document(user_id: Optional[str], meeting_id: Optional[str],
                    file: UploadFile = File(...),
                    api_key: Optional[str] = Header(None)):
    url = f"{meetings_service_url}/documents/upload?user_id={user_id}&meeting_id={meeting_id}"
    files = {"file": (file.filename, file.file.read(), file.content_type)}
    params = {"user_id": user_id, "meeting_id": meeting_id}
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None
    return make_request(url, method="POST", params=params, data=files, headers=headers)


@app.get("/documents/m/{meeting_id}", tags=["Documents"])
def get_documents_by_meeting(meeting_id: str,
                             api_key: Optional[str] = Header(None)):
    url = f"{meetings_service_url}/documents/m/{meeting_id}"
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None
    return make_request(url, headers=headers)


@app.delete("/documents/{document_id}", tags=["Documents"])
def delete_document(document_id: str, api_key: Optional[str] = Header(None)):
    url = f"{meetings_service_url}/documents/{document_id}"
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None
    return make_request(url, method="DELETE", headers=headers)


@app.post("/documents/{document_id}/sign", tags=["Documents"])
def sign_document(document_id: str, sign_data: dict,
                  api_key: Optional[str] = Header(None)):
    url = f"{meetings_service_url}/documents/{document_id}/sign/"
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None
    return make_request(url, method="POST", params=sign_data, headers=headers)


@app.post("/documents/{document_id}/sign/verify", tags=["Documents"])
def verify_document(document_id: str, api_key: Optional[str] = Header(None)):
    url = f"{meetings_service_url}/documents/{document_id}/sign/verify"
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None
    return make_request(url, method="POST", headers=headers)


@app.get("/documents/{document_id}/download", tags=["Documents"])
def download_document(document_id: str, api_key: Optional[str] = Header(None)):
    url = f"{meetings_service_url}/documents/{document_id}/download"
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None
    params = {"document_id": document_id}
    response = requests.get(url, params=params, headers=headers)

    print(response.headers)
    # Raise an HTTPException if the request failed
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail=response.text)

    # Get the file content and metadata from the response
    file_content = response.content
    file_type = response.headers["Content-Type"]
    content_disposition = response.headers["Content-Disposition"]
    filename_index = content_disposition.find("filename*=")
    if filename_index != -1:
        file_name = content_disposition.split("filename*=utf-8")[1].strip('"')
    else:
        file_name = content_disposition.split("filename=")[1].strip('"')
    # Create a StreamingResponse to return the file content as a downloadable file
    response = StreamingResponse(
        iter([file_content]),
        media_type=file_type
    )
    response.headers["Content-Disposition"] = f"attachment; filename={file_name}"

    return response
