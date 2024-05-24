from fastapi import APIRouter, Depends
from app.api.routes import documents
from app.dependencies import verify_key

router = APIRouter(dependencies=[Depends(verify_key)])

router.include_router(documents.app, prefix="/documents", tags=["documents"])
