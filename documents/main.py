from fastapi import FastAPI
from app.api.main import router
from app.db.database import SQLModel, engine

app = FastAPI(title="Documents API", version="0.1.0")
app.include_router(router)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
