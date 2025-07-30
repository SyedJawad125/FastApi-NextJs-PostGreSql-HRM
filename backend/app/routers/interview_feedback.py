from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from .. import database, schemas, models, oauth2
from app.utils import filter_interview_feedbacks, paginate_data  # You'll need to create filter_interview_feedbacks
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/interview-feedbacks",
    tags=["Interview Feedbacks"]
)

# ✅ Get all interview feedbacks with filtering + pagination
@router.get("/", response_model=schemas.InterviewFeedbackListResponse)
def get_interview_feedbacks(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.InterviewFeedback)
        # You'll need to implement filter_interview_feedbacks in your utils
        query = filter_interview_feedbacks(request.query_params, query)

        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        serialized_data = [schemas.InterviewFeedbackOut.from_orm(feedback) for feedback in paginated_data]

        response_data = {
            "count": count,
            "data": serialized_data
        }

        return {
            "status": "SUCCESSFUL",
            "result": response_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Create new interview feedback
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.InterviewFeedbackOut)
def create_interview_feedback(
    feedback: schemas.InterviewFeedbackCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        # Verify that the interview exists
        interview = db.query(models.Interview).filter(models.Interview.id == feedback.interview_id).first()
        if not interview:
            raise HTTPException(status_code=404, detail=f"Interview with id {feedback.interview_id} not found")

        # Verify panel member exists if provided
        if feedback.panel_member_id:
            panel_member = db.query(models.User).filter(models.User.id == feedback.panel_member_id).first()
            if not panel_member:
                raise HTTPException(status_code=404, detail=f"Panel member with id {feedback.panel_member_id} not found")

        feedback_data = feedback.dict(exclude_unset=True)
        feedback_data["created_by_user_id"] = current_user.id
        feedback_data["updated_by_user_id"] = None

        new_feedback = models.InterviewFeedback(**feedback_data)
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)

        return new_feedback

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Get single interview feedback by ID
@router.get("/{id}", response_model=schemas.InterviewFeedbackOut)
def get_interview_feedback(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    feedback = db.query(models.InterviewFeedback).filter(models.InterviewFeedback.id == id).first()

    if not feedback:
        raise HTTPException(status_code=404, detail=f"Interview feedback with id {id} not found")

    return feedback

# ✅ Update interview feedback
@router.patch("/{id}", response_model=schemas.InterviewFeedbackOut)
def update_interview_feedback(
    id: int,
    updated_data: schemas.InterviewFeedbackUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        feedback_instance = db.query(models.InterviewFeedback).filter(models.InterviewFeedback.id == id).first()

        if not feedback_instance:
            raise HTTPException(status_code=404, detail=f"Interview feedback with id {id} not found")

        # Verify interview exists if being updated
        if updated_data.interview_id:
            interview = db.query(models.Interview).filter(models.Interview.id == updated_data.interview_id).first()
            if not interview:
                raise HTTPException(status_code=404, detail=f"Interview with id {updated_data.interview_id} not found")

        # Verify panel member exists if being updated
        if updated_data.panel_member_id:
            panel_member = db.query(models.User).filter(models.User.id == updated_data.panel_member_id).first()
            if not panel_member:
                raise HTTPException(status_code=404, detail=f"Panel member with id {updated_data.panel_member_id} not found")

        update_dict = updated_data.dict(exclude_unset=True)
        update_dict["updated_by_user_id"] = current_user.id

        for key, value in update_dict.items():
            setattr(feedback_instance, key, value)

        db.commit()
        db.refresh(feedback_instance)

        return feedback_instance

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Delete interview feedback
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_interview_feedback(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    feedback_query = db.query(models.InterviewFeedback).filter(models.InterviewFeedback.id == id)
    feedback = feedback_query.first()

    if not feedback:
        raise HTTPException(status_code=404, detail=f"Interview feedback with id {id} not found")

    feedback_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Interview feedback deleted successfully"}

# ✅ Get feedbacks by interview ID
@router.get("/interview/{interview_id}", response_model=schemas.InterviewFeedbackListResponse)
def get_feedbacks_by_interview(
    interview_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        # Verify interview exists
        interview = db.query(models.Interview).filter(models.Interview.id == interview_id).first()
        if not interview:
            raise HTTPException(status_code=404, detail=f"Interview with id {interview_id} not found")

        query = db.query(models.InterviewFeedback).filter(models.InterviewFeedback.interview_id == interview_id)
        
        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        serialized_data = [schemas.InterviewFeedbackOut.from_orm(feedback) for feedback in paginated_data]

        response_data = {
            "count": count,
            "data": serialized_data
        }

        return {
            "status": "SUCCESSFUL",
            "result": response_data
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Get feedbacks by panel member ID
@router.get("/panel-member/{panel_member_id}", response_model=schemas.InterviewFeedbackListResponse)
def get_feedbacks_by_panel_member(
    panel_member_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        # Verify panel member exists
        panel_member = db.query(models.User).filter(models.User.id == panel_member_id).first()
        if not panel_member:
            raise HTTPException(status_code=404, detail=f"Panel member with id {panel_member_id} not found")

        query = db.query(models.InterviewFeedback).filter(models.InterviewFeedback.panel_member_id == panel_member_id)
        
        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        serialized_data = [schemas.InterviewFeedbackOut.from_orm(feedback) for feedback in paginated_data]

        response_data = {
            "count": count,
            "data": serialized_data
        }

        return {
            "status": "SUCCESSFUL",
            "result": response_data
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))