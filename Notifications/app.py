from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Request
from .routers import email, auth, register, telegram, notifications
from fastapi.templating import Jinja2Templates
from .db.models import usermodel, telegrammodel
from .db.database import engine

usermodel.Base.metadata.create_all(bind=engine)
telegrammodel.Base.metadata.create_all(bind=engine)

description = """
Notification API helps you do awesome stuff. 🚀

## Items


"""

app = FastAPI(title="Notification API",
    description=description,
    summary="Deadpool's favorite app. Nuff said.",
    version="1.0.1",
    root_path="/api/v1")


app.include_router(auth.router, prefix="/auth",tags=["auth"])
app.include_router(register.router,prefix="/admin/register",tags=["register"])
app.include_router(telegram.router,prefix="/telegram",tags=["telegram"])
app.include_router(email.router, prefix="/email",tags=["email"])
app.include_router(notifications.router, prefix="/notify",tags=["notify"])

templates = Jinja2Templates(directory="templates")


@app.get("/")
def register(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
