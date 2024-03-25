from fastapi import Query, APIRouter
from app.resp_models.models import Meeting, MeetingReceive, MeetingAttendees
from datetime import datetime
from app.db.database import engine
from sqlmodel import Session


app = APIRouter()


@app.get("/", status_code=200)
async def get_all_meetings(user_id: str = Query(None)) -> Meeting:
    # Mock function to retrieve all meetings from the database
    return Meeting(title="Ponto de situação", created_by="bernardo")


# Other endpoints remain unchanged
@app.get("{meeting_id}", status_code=200)
async def get_meeting(meeting_id: str, user_id: str = Query(None)) -> Meeting:
    # Mock function to retrieve meeting details from the database
    # if meeting.id == meeting_id:
    #       return meeting
    # raise HTTPException(status_code=404, detail="Meeting not found")
    return Meeting(title="Ponto de situação", created_by="bernardo")


@app.post("/", status_code=201)
async def create_meeting(meeting: MeetingReceive):
    # Mock function to create a new meeting
    if meeting.start_date.timestamp() < datetime.today().timestamp():
        return {"message": "Meeting start date cannot be in the past"}
    elif meeting.end_date < meeting.start_date:
        return {"message": "Meeting end date cannot be before start date"}

    new_meet = Meeting(id=meeting.id, title=meeting.title, location=meeting.location, start_date=meeting.start_date,
                       end_date=meeting.end_date, created_by=meeting.created_by)
    attendees = [MeetingAttendees(meeting_id=new_meet.id, user_id=attendee) for attendee in meeting.attendees]

    with Session(engine) as session:
        session.add(new_meet)
        session.add_all(attendees)
        session.commit()

    return {"message": "Meeting created successfully",
            "meeting_id": meeting.id}


@app.put("/{meeting_id}", status_code=200)
async def update_meeting(meeting_id: str) -> Meeting:
    # Mock function to update an existing meetingreturn {"message": f"Meeting {meeting_id} updateVVd successfully"}
    return Meeting(title="Ponto de situação", created_by="bernardo")


@app.delete("/{meeting_id}", status_code=204)
async def delete_meeting(meeting_id: str):
    # Mock function to delete a meeting
    return {"message": f"Meeting {meeting_id} deleted successfully"}
