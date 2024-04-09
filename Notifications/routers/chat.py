from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi import APIRouter

router = APIRouter(prefix="/chat",tags=["chat"])

@router.get("/",  status_code=200)
async def get_all_chats(user_id: str = Query(None)):
     return {"message": "Hello World"}

@router.get("/{chat_id}", status_code=200)
async def get_chat(chat_id: str,user_id: str = Query(None)):
     return {"message": "Hello World"}

@router.post("/", status_code=201)
async def create_chat(chat: int):
    # Mock function to create a new meeting
    return {"message": "Chat created successfully"}

@router.put("/{chat_id}", status_code=202)
async def update_chat(chat: int):
    # Mock function to create a new meeting
    return {"message": "Chat created successfully"}

@router.delete("/{chat_id}" ,status_code=200)
async def delete_chat(chat: int):
    # Mock function to create a new meeting
    return {"message": "Chat created successfully"}