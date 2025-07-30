from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from app import database, schemas, models, oauth2
from app.utils import filter_interview_schedules, paginate_data

router = APIRouter(
    prefix="/interview-schedules",
    tags=["Interview Schedules"]
)
# GET /interview-schedules/?status=scheduled&mode=online&page=1&limit=5

# ✅ Get all interview schedules (with pagination)
@router.get("/", response_model=schemas.InterviewScheduleListResponse)
def get_interview_schedules(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.InterviewSchedule).order_by(models.InterviewSchedule.scheduled_datetime.desc())

        query = filter_interview_schedules(dict(request.query_params), query)
        # Fetch and paginate
        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        # Serialize
        serialized_data = [schemas.InterviewScheduleOut.from_orm(item) for item in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized_data
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Create new interview schedule
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.InterviewScheduleOut)
def create_interview_schedule(
    schedule: schemas.InterviewScheduleCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        data = schedule.dict(exclude_unset=True)
        data["created_by_user_id"] = current_user.id

        new_schedule = models.InterviewSchedule(**data)
        db.add(new_schedule)
        db.commit()
        db.refresh(new_schedule)

        return new_schedule

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Get interview schedule by ID
@router.get("/{id}", response_model=schemas.InterviewScheduleOut)
def get_interview_schedule(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    schedule = db.query(models.InterviewSchedule).filter(models.InterviewSchedule.id == id).first()

    if not schedule:
        raise HTTPException(status_code=404, detail=f"Interview Schedule with ID {id} not found")

    return schedule


# ✅ Update interview schedule
@router.patch("/{id}", response_model=schemas.InterviewScheduleOut)
def update_interview_schedule(
    id: int,
    updated_data: schemas.InterviewScheduleUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        schedule = db.query(models.InterviewSchedule).filter(models.InterviewSchedule.id == id).first()

        if not schedule:
            raise HTTPException(status_code=404, detail=f"Interview Schedule with ID {id} not found")

        update_dict = updated_data.dict(exclude_unset=True)
        update_dict["updated_by_user_id"] = current_user.id

        for key, value in update_dict.items():
            setattr(schedule, key, value)

        db.commit()
        db.refresh(schedule)

        return schedule

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Delete interview schedule
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_interview_schedule(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    schedule_query = db.query(models.InterviewSchedule).filter(models.InterviewSchedule.id == id)
    schedule = schedule_query.first()

    if not schedule:
        raise HTTPException(status_code=404, detail=f"Interview Schedule with ID {id} not found")

    schedule_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Interview schedule deleted successfully"}
