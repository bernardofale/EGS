from typing import Optional
from fastapi import APIRouter, Depends, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
import json
from db.crud import usercrud
from db.schemas import userschema
from sqlalchemy.orm import Session
from db.database import get_db

router = APIRouter()


templates = Jinja2Templates(directory="templates")

@router.get("/")
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# @router.post("/", response_model=userschema.User)
# def create_user(user: userschema.UserBase, db: Session = Depends(get_db)):
#     db_user = usercrud.get_user_by_username(db, username=user.username)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return usercrud.create_user(db=db, user=user)

@router.post("/")
def register(request: Request, name_of_service: str = Form(...), username: str= Form(...), db: Session = Depends(get_db)):
    errors = []
    try:
        db_user = usercrud.get_user_by_username(db, username=username)
        usercrud.create_user(db=db, user= userschema.UserBase(username=username, name_of_service=name_of_service))
        db_user = usercrud.get_user_by_username(db, username=username)
        # return responses.RedirectResponse(router.url_path_for(name='homepage')
        #                         +"/?alert=Successfully%20Registered",status_code=status.HTTP_302_FOUND)
        return templates.TemplateResponse(
            "/home.html", {"request": request, "alert": "Successfully Registered", "username": db_user.username,
                           "name_of_service": db_user.name_of_service, "api_key": db_user.api_key }     )
    except ValidationError as e:
        errors_list = json.loads(e.json())
        for item in errors_list:
            errors.append(item.get("loc")[0]+ ": " + item.get("msg"))
        return templates.TemplateResponse("auth/register.html",{"request":request,"errors":errors})
