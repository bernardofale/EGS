from typing import Optional
from fastapi import FastAPI, HTTPException, Header, UploadFile, File, \
    Depends, Response
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm
import requests
from models.models import ToDoItemCreate
from models.auth_model import UserInDB
from models import meeting_models
from models import documents_models
import redis
import json
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REDIS_HOST = os.getenv("REDIS_HOST")
TODO_HOST = os.getenv("TODO_HOST")
TODO_PORT = os.getenv("TODO_PORT")
MEETINGS_HOST = os.getenv("MEETINGS_HOST")
MEETINGS_PORT = os.getenv("MEETINGS_PORT")
DOCS_HOST = os.getenv("DOCS_HOST")
DOCS_PORT = os.getenv("DOCS_PORT")
NOTIFICATIONS_HOST = os.getenv("NOTIFICATIONS_HOST")
NOTIFICATIONS_PORT = os.getenv("NOTIFICATIONS_PORT")
AUTH_HOST = os.getenv("AUTH_HOST")
AUTH_PORT = os.getenv("AUTH_PORT")

# Connect to redis
r = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)

todo_service_url = f"http://{TODO_HOST}:{TODO_PORT}"
todo_api_key = "CGtZ10f6JytK0EOMeuI6noSfZEmDowqn"
meetings_service_url = f"http://{MEETINGS_HOST}:{MEETINGS_PORT}"
meetings_api_key = "3e17a9d25945d0d7d009ccd62a5a7816265d3c6ffa03334a85cfd74be10c55e7"
docs_service_url = f"http://{DOCS_HOST}:{DOCS_PORT}"
docs_api_key = "19e33835-b178-4ff9-98d5-6d5cf7ef15c0"
notifications_service_url = f"http://{NOTIFICATIONS_HOST}:{NOTIFICATIONS_PORT}"
notifications_api_key = ""
auth_service_url = f"http://{AUTH_HOST}:{AUTH_PORT}"



# Helper function to make requests
def make_request(url, method="GET", params=None, data=None,
                 headers=None,
                 files=None):
    try:
        if method == "GET":
            response = requests.get(url, params=params, headers=headers)
        elif method == "POST":
            response = requests.post(url, data=data, json=params,
                                     headers=headers, files=files)
        elif method == "PUT":
            response = requests.put(url, json=params, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
            return "deleted"
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=response.status_code,
                            detail=response.json())


# Auth endpoints
@app.post("/register", tags=["Auth"])
def register(user: UserInDB):
    url = f"{auth_service_url}/auth/register"
    return make_request(url, method="POST", params=user.dict())

@app.post("/admin/notifications/token", tags=["Admin"])
def register(token:str):
    global notifications_api_key
    notifications_api_key= token
    return {"status":"ok"}, 200

@app.post("/admin/todo/token", tags=["Admin"])
def register(token:str):
    global todo_api_key
    todo_api_key= token
    return {"status":"ok"}, 200

@app.post("/login", tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    url = f"{auth_service_url}/auth/"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': form_data.grant_type,
        'username': form_data.username,
        'password': form_data.password,
        'scope': form_data.scopes,
        'client_id': form_data.client_id,
        'client_secret': form_data.client_secret
    }
    r = make_request(url, method="POST", headers=headers,
                     data=data)
    response = Response(content=json.dumps(r))
    response.set_cookie(key="access_token", value=r["access_token"])
    return response


# @app.get("/verify", tags=["Auth"])
def verify_token(token: str):
    url = f"{auth_service_url}/auth/verify"
    params = {"token": token}
    return make_request(url, params=params)


@app.get("/users/me", tags=["Auth"])
def get_user(token: str):
    url = f"{auth_service_url}/users/me"
    verify_token(token)
    headers = {"Authorization": f"Bearer {token}"}
    return make_request(url, headers=headers)


# Todo endpoints
@app.get("/todos", tags=["Todo"])
def get_todos(token: str,
              completed: Optional[bool] = None,
              priority: Optional[int] = None,
              due_date: Optional[str] = None,
              sort_by_due_date: Optional[str] = None):
    u = verify_token(token)
    user_key = "user:" + str(u["id"]) + ":todos"
    todo_ids = r.smembers(user_key)
    print(todo_ids)
    d = {}
    for todo_id in todo_ids:
        id = todo_id.split(":")[1]
        d[id] = get_todo_by_id(token, id)
    return d


@app.post("/todos", tags=["Todo"])
def create_todo(token: str,
                todo_data: ToDoItemCreate):
    url = f"{todo_service_url}/v1/todos"
    u = verify_token(token)
    todo_data.due_date = todo_data.due_date.isoformat()
    headers = {"api-key": todo_api_key}
    rsp = make_request(url, method="POST", params=todo_data.dict(),
                       headers=headers)
    todo_id = "todo:" + str(rsp["id"])
    user_key = "user:" + str(u["id"]) + ":todos"
    r.sadd(user_key, todo_id)
    return rsp


@app.post("/associate-todo", tags=["Todo"])
def associate_todo_with_meeting(token: str,
                                todo_id: int,
                                meeting_id: str):
    u = verify_token(token)
    if r.sismember("user:" + str(u["id"]) + ":todos", "todo:" + str(todo_id)):
        meeting_key = "meeting:" + meeting_id
        for key in r.scan_iter("meeting:*"):
            # Check if the value is a member of the Set
            if r.sismember(key, "todo:" + str(todo_id)):
                # Remove the value from the Set
                r.srem(key, "todo:" + str(todo_id))
        r.sadd(meeting_key, "todo:" + str(todo_id))
    return {"todo_id": todo_id,
            "meeting_id": meeting_id,
            "message": "Todo associated with meeting"}


@app.get("/todos/meeting/{meeting_id}", tags=["Todo"])
def get_todos_by_meeting(token: str,
                         meeting_id: str):
    verify_token(token)
    meeting_key = "meeting:" + meeting_id
    todo_ids = r.smembers(meeting_key)
    d = {}
    for todo_id in todo_ids:
        id = todo_id.split(":")[1]
        d[id] = get_todo_by_id(token, id)
    return d


@app.get("/todos/{todo_id}", tags=["Todo"])
def get_todo_by_id(token: str,
                   todo_id: int):
    url = f"{todo_service_url}/v1/todos/{todo_id}"
    u = verify_token(token)
    if r.sismember("user:" + str(u["id"]) + ":todos", "todo:" + str(todo_id)):
        headers = {"api-key": todo_api_key}
        return make_request(url, headers=headers)
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


@app.put("/todos/{todo_id}", tags=["Todo"])
def update_todo(todo_id: int,
                token: str,
                todo_data: ToDoItemCreate):
    url = f"{todo_service_url}/v1/todos/{todo_id}"
    u = verify_token(token)
    if r.sismember("user:" + str(u["id"]) + ":todos", "todo:" + str(todo_id)):
        todo_data.due_date = todo_data.due_date.isoformat()
        headers = {"api-key": todo_api_key}
        return make_request(url, method="PUT",
                            params=todo_data.dict(),
                            headers=headers)
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


@app.delete("/todos/{todo_id}", tags=["Todo"])
def delete_todo(token: str,
                todo_id: int):
    url = f"{todo_service_url}/v1/todos/{todo_id}"
    u = verify_token(token)
    if r.sismember("user:" + str(u["id"]) + ":todos", "todo:" + str(todo_id)):
        headers = {"api-key": todo_api_key}
        r.srem("user:" + str(u["id"]) + ":todos", "todo:" + str(todo_id))
        for key in r.scan_iter("meeting:*"):
            print(key)
            # Check if the value is a member of the Set
            if r.sismember(key, "todo:" + str(todo_id)):
                # Remove the value from the Set
                r.srem(key, "todo:" + str(todo_id))
                break
        return make_request(url, method="DELETE", headers=headers)
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


# Meetings endpoints
@app.get("/meetings", tags=["Meetings"])
def get_meetings(token: str):

    u = verify_token(token)
    user_key = "user:" + str(u["id"]) + ":meetings"
    meetings_ids = r.smembers(user_key)
    d = {}
    for meeting_id in meetings_ids:
        id = meeting_id.split(":")[1]
        m = get_meeting(token, id)
        m["created_by"] = u["id"]
        d[id] = m
    return d


@app.get("/meetings/{meeting_id}", tags=["Meetings"])
def get_meeting(token: str,
                meeting_id: str):
    url = f"{meetings_service_url}/meetings/{meeting_id}"
    verify_token(token)
    headers = {"Authorization": f"Bearer {meetings_api_key}"}
    return make_request(url, headers=headers)


@app.post("/meetings", tags=["Meetings"])
def create_meeting(meeting_data: meeting_models.MeetingReceive,
                   token: str):
    url = f"{meetings_service_url}/meetings/"
    u = verify_token(token)
    headers = {"Authorization": f"Bearer {meetings_api_key}"}
    meeting_data.start_date = meeting_data.start_date.isoformat()
    meeting_data.end_date = meeting_data.end_date.isoformat()
    rsp = make_request(url, method="POST", params=meeting_data.dict(),
                       headers=headers)
    meeting_id = "meeting:" + str(rsp["id"])
    user_key = "user:" + str(u["id"]) + ":meetings"
    r.sadd(user_key, meeting_id)
    return rsp


@app.put("/meetings/{meeting_id}", tags=["Meetings"])
def update_meeting(token: str,
                   meeting_id: str,
                   meeting_data: meeting_models.MeetingUpdate):
    url = f"{meetings_service_url}/meetings/{meeting_id}"
    u = verify_token(token)
    if r.sismember("user:" + str(u["id"]) + ":meetings",
                   "meeting:" + str(meeting_id)):
        meeting_data.start_date = meeting_data.start_date.isoformat()
        meeting_data.end_date = meeting_data.end_date.isoformat()
        headers = {"Authorization": f"Bearer {meetings_api_key}"}
        return make_request(url, method="PUT", params=meeting_data.dict(),
                            headers=headers)
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


@app.delete("/meetings/{meeting_id}", tags=["Meetings"])
def delete_meeting(token: str,
                   meeting_id: str):
    url = f"{meetings_service_url}/meetings/{meeting_id}"
    u = verify_token(token)
    if r.sismember("user:" + str(u["id"]) + ":meetings",
                   "meeting:" + str(meeting_id)):
        r.srem("user:" + str(u["id"]) + ":meetings", "meeting:" + str(meeting_id))
        headers = {"Authorization": f"Bearer {meetings_api_key}"}
        return make_request(url, method="DELETE", headers=headers)
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


# Documents endpoints
@app.get("/documents", tags=["Documents"])
def get_documents(token: str):
    url = f"{docs_service_url}/documents/"
    u = verify_token(token)
    params = {"user_id": "0"}
    headers = {"Authorization": f"Bearer {docs_api_key}"}
    rsp = make_request(url, params=params, headers=headers)
    user_key = "user:" + str(u["id"]) + ":documents"
    d = {}
    for document in rsp:
        if r.sismember(user_key, "document:" + str(document["id"])):
            d[document["id"]] = document
            d[document["id"]]["uploaded_by"] = u["id"]
    return d


@app.get("/documents/download/{document_id}", tags=["Documents"])
def get_document(token: str,
                 document_id: str):
    url = f"{docs_service_url}/documents/{document_id}"
    u = verify_token(token)
    if r.sismember("user:" + str(u["id"]) + ":documents",
                   "document:" + str(document_id)):
        headers = {"Authorization": f"Bearer {docs_api_key}"}

        params = {"document_id": document_id}
        # Send the request to your service
        response = requests.get(url, params=params, headers=headers)

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
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


@app.post("/documents/upload", tags=["Documents"])
def upload_document(token: str,
                    file: UploadFile = File(...)):
    url = f"{docs_service_url}/documents/upload"
    u = verify_token(token)
    files = {"file": (file.filename, file.file.read(), file.content_type)}
    headers = {"Authorization": f"Bearer {docs_api_key}"}
    rsp = make_request(url, method="POST", files=files, headers=headers)
    user_key = "user:" + str(u["id"]) + ":documents"
    r.sadd(user_key, "document:" + str(rsp["id"]))
    return rsp


@app.delete("/documents/{document_id}", tags=["Documents"])
def delete_document(token: str,
                    document_id: str):
    url = f"{docs_service_url}/documents/{document_id}"
    u = verify_token(token)
    user_key = "user:" + str(u["id"]) + ":documents"
    if r.sismember(user_key, "document:" + str(document_id)):
        r.srem(user_key, "document:" + str(document_id))
        headers = {"Authorization": f"Bearer {docs_api_key}"}
        return make_request(url, method="DELETE", headers=headers)
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")


@app.post("/documents/{document_id}/sign", tags=["Documents"])
def sign_document(token: str,
                  document_id: str, sign_data: documents_models.DocumentSign):
    url = f"{docs_service_url}/documents/{document_id}/sign/"
    verify_token(token)
    headers = {"Authorization": f"Bearer {docs_api_key}"}
    return make_request(url, method="POST", params=sign_data.dict(),
                        headers=headers)


@app.post("/documents/{document_id}/sign/verify", tags=["Documents"])
def verify_document(token: str,
                    document_id: str):
    url = f"{docs_service_url}/documents/{document_id}/sign/verify"
    verify_token(token)
    headers = {"Authorization": f"Bearer {docs_api_key}"}
    return make_request(url, method="POST", headers=headers)


@app.get("/documents/{document_id}/download", tags=["Documents"])
def download_document(token: str,
                      document_id: str):
    url = f"{meetings_service_url}/documents/{document_id}/download"
    verify_token(token)
    headers = {"Authorization": f"Bearer {docs_api_key}"}
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


# Notifications endpoints
