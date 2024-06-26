from fastapi import Depends, FastAPI, HTTPException, status, Response
from app.user_routes import users
from app.auth import auth_routes


app = FastAPI()

app.include_router(users.router)
app.include_router(auth_routes.router)


@app.get("/")
async def root():
    return "root"
