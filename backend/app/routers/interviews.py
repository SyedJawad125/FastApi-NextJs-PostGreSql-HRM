from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from app import database, schemas, models, oauth2
from app.utils import filter_interviews, paginate_data

router = APIRouter(
    prefix="/interviews",
    tags=["Interviews"]
)


# ✅ Get all interviews (with pagination)
@router.get("/", response_model=schemas.InterviewListResponse)
def get_interviews(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.Interview)

        # Apply filters
        query = filter_interviews(request.query_params, query)

        # Fetch filtered data
        all_data = query.all()

        # Apply pagination
        paginated_data, count = paginate_data(all_data, request)

        # Serialize
        serialized_data = [schemas.InterviewOut.from_orm(item) for item in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized_data
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Create new interview
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.InterviewOut)
def create_interview(
    interview: schemas.InterviewCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        data = interview.dict(exclude_unset=True)
        data["created_by_user_id"] = current_user.id
        data["updated_by_user_id"] = None

        new_interview = models.Interview(**data)
        db.add(new_interview)
        db.commit()
        db.refresh(new_interview)

        return new_interview

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Get interview by ID
@router.get("/{id}", response_model=schemas.InterviewOut)
def get_interview(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    interview = db.query(models.Interview).filter(models.Interview.id == id).first()

    if not interview:
        raise HTTPException(status_code=404, detail=f"Interview with ID {id} not found")

    return interview


# ✅ Update interview
@router.patch("/{id}", response_model=schemas.InterviewOut)
def update_interview(
    id: int,
    updated_data: schemas.InterviewUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        interview = db.query(models.Interview).filter(models.Interview.id == id).first()

        if not interview:
            raise HTTPException(status_code=404, detail=f"Interview with ID {id} not found")

        update_dict = updated_data.dict(exclude_unset=True)
        update_dict["updated_by_user_id"] = current_user.id

        for key, value in update_dict.items():
            setattr(interview, key, value)

        db.commit()
        db.refresh(interview)

        return interview

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Delete interview
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_interview(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    interview_query = db.query(models.Interview).filter(models.Interview.id == id)
    interview = interview_query.first()

    if not interview:
        raise HTTPException(status_code=404, detail=f"Interview with ID {id} not found")

    interview_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Interview deleted successfully"}
