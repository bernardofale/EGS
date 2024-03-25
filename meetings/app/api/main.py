from fastapi import APIRouter
from app.api.routes import meeting, documents


router = APIRouter()

router.include_router(meeting.app, prefix="/meetings", tags=["meetings"])
router.include_router(documents.app, prefix="/documents", tags=["documents"])
