from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from .. import database, schemas, models, oauth2
from app.utils import paginate_data
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/job-applications",
    tags=["Job Applications"]
)


# ✅ Get all job applications (with pagination)
@router.get("/", response_model=schemas.JobApplicationListResponse)
def get_job_applications(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.JobApplication)

        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        serialized_data = [schemas.JobApplicationOut.from_orm(item) for item in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized_data
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Create new job application
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.JobApplicationOut)
def create_job_application(
    job_application: schemas.JobApplicationCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        data = job_application.dict(exclude_unset=True)
        data["created_by_user_id"] = current_user.id
        data["updated_by_user_id"] = None

        new_application = models.JobApplication(**data)
        db.add(new_application)
        db.commit()
        db.refresh(new_application)

        return new_application

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Get single job application by ID
@router.get("/{id}", response_model=schemas.JobApplicationOut)
def get_job_application(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    application = db.query(models.JobApplication).filter(models.JobApplication.id == id).first()

    if not application:
        raise HTTPException(status_code=404, detail=f"Job Application with ID {id} not found")

    return application


# ✅ Update job application
@router.patch("/{id}", response_model=schemas.JobApplicationOut)
def update_job_application(
    id: int,
    updated_data: schemas.JobApplicationUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        application = db.query(models.JobApplication).filter(models.JobApplication.id == id).first()

        if not application:
            raise HTTPException(status_code=404, detail=f"Job Application with ID {id} not found")

        update_dict = updated_data.dict(exclude_unset=True)
        update_dict["updated_by_user_id"] = current_user.id

        for key, value in update_dict.items():
            setattr(application, key, value)

        db.commit()
        db.refresh(application)

        return application

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Delete job application
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_job_application(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    application_query = db.query(models.JobApplication).filter(models.JobApplication.id == id)
    application = application_query.first()

    if not application:
        raise HTTPException(status_code=404, detail=f"Job Application with ID {id} not found")

    application_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Job Application deleted successfully"}
