from fastapi import APIRouter, Depends
from app.api.routes import meeting
from app.dependencies import verify_key

router = APIRouter(dependencies=[Depends(verify_key)])

router.include_router(meeting.app, prefix="/meetings", tags=["meetings"])
