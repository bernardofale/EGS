from fastapi import APIRouter, Depends
from app.api.routes import meeting, documents
from app.dependencies import verify_key

router = APIRouter(dependencies=[Depends(verify_key)])

router.include_router(meeting.app, prefix="/meetings", tags=["meetings"])
router.include_router(documents.app, prefix="/documents", tags=["documents"])
