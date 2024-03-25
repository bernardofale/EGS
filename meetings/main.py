from fastapi import FastAPI
from app.api.main import router
from app.db.database import SQLModel, engine

app = FastAPI(title="Meetings API", version="0.1.0")
app.include_router(router)
SQLModel.metadata.create_all(engine)
