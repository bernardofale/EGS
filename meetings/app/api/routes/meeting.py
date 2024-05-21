from fastapi import Query, APIRouter, HTTPException
from app.resp_models.models import Meeting, MeetingReceive, MeetingAttendees, \
                                                            MeetingUpdate
from app.db.database import engine
from sqlmodel import Session, select

app = APIRouter()


@app.get("", status_code=200)
async def get_all_meetings(user_id: str = Query(None)):
    # Function to retrieve all meetings from the database

    with Session(engine) as session:
        results = session.exec(select(Meeting).where(Meeting.created_by ==
                                                     user_id)).all()
        if len(results) == 0:
            raise HTTPException(status_code=404,
                                detail="No meetings found for this user")

        return results


@app.get("/{meeting_id}", status_code=200)
async def get_meeting(meeting_id: str) -> Meeting:
    # Mock function to retrieve meeting details from the database
    with Session(engine) as session:
        results = session.exec(select(Meeting).where(Meeting.id == meeting_id))
        if results is None:
            raise HTTPException(status_code=404, detail="No meeting found")
        return results.one()


@app.post("/", status_code=201)
async def create_meeting(meeting: MeetingReceive) -> Meeting:
    # Function to create a new meeting
    # Pydantic validation will raise an error if the start_date is in the past
    # or the end_date is before the start_date

    new_meet = Meeting(title=meeting.title,
                       location=meeting.location,
                       start_date=meeting.start_date,
                       end_date=meeting.end_date,
                       todo_id=meeting.todo_id,
                       created_by=meeting.created_by)
    attendees = [MeetingAttendees(meeting_id=new_meet.id,
                                  user_id=attendee.user_id)
                 for attendee in meeting.attendees]

    with Session(engine) as session:
        session.add(new_meet)
        session.add_all(attendees)
        session.commit()
        session.refresh(new_meet)
        return new_meet


@app.put("/{meeting_id}", status_code=200)
async def update_meeting(meeting_id: str, edit_meeting: MeetingUpdate):
    # Function to update an existing meeting
    with Session(engine) as session:
        results = session.exec(select(Meeting).where(Meeting.id == meeting_id))
        meeting = results.first()
        if meeting is None:
            raise HTTPException(status_code=404, detail="No meeting found")
        attendees = [MeetingAttendees(meeting_id=meeting_id,
                                      user_id=attendee.user_id,
                                      status=attendee.status)
                     for attendee in edit_meeting.attendees]
        meeting_attendees = session.exec(select(MeetingAttendees).
                                         where(MeetingAttendees.meeting_id ==
                                               meeting_id))
        for attendee in meeting_attendees:
            session.delete(attendee)
        meeting.title = edit_meeting.title
        meeting.location = edit_meeting.location
        meeting.start_date = edit_meeting.start_date
        meeting.end_date = edit_meeting.end_date
        meeting.todo_id = edit_meeting.todo_id
        session.add_all(attendees)
        session.add(meeting)
        session.commit()
        session.refresh(meeting)
        return meeting


@app.delete("/{meeting_id}", status_code=204)
async def delete_meeting(meeting_id: str):
    # Mock function to delete a meeting
    with Session(engine) as session:
        results = session.exec(select(Meeting).where(Meeting.id == meeting_id))
        meeting = results.first()
        if meeting is None:
            raise HTTPException(status_code=404, detail="No meeting found")
        for attendee in meeting.attendees:
            session.delete(attendee)
        session.delete(meeting)
        session.commit()
