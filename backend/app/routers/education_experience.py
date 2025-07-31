from fastapi import APIRouter, HTTPException, status, Request, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, oauth2, schemas
from app import database
from app.utils import filter_education_experiences, paginate_data
from app.schemas.education_experience import (
    EducationExperienceCreate,
    EducationExperienceUpdate,
    EducationExperienceOut,
    PaginatedEducationExperiences,
)
from app.database import get_db

router = APIRouter(
    prefix="/education-experiences",
    tags=["Education Experiences"]
)

# -------------------- Create One or Many --------------------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[schemas.EducationExperienceOut])
def create_education_experiences(
    items: List[schemas.EducationExperienceCreate],
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        created = []
        for item in items:
            experience = models.EducationExperience(
                **item.dict(),
                created_by_user_id=current_user.id,
                updated_by_user_id=None
            )
            db.add(experience)
            created.append(experience)

        db.commit()
        for c in created:
            db.refresh(c)

        return created

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# -------------------- Get All with Filtering & Pagination --------------------
@router.get("/", response_model=PaginatedEducationExperiences)
def get_all_education_experiences(
    request: Request,
    db: Session = Depends(get_db)
):
    query = db.query(models.EducationExperience)
    params = dict(request.query_params)

    # Remove pagination params from filters if present
    params.pop("page", None)
    params.pop("page_size", None)

    # Apply filters
    query = filter_education_experiences(params, query)
    all_results = query.all()

    # Apply pagination
    paginated_data, total = paginate_data(all_results, request)

    return {
        "count": total,
        "data": paginated_data
    }


# -------------------- Get by Employee --------------------
@router.get("/employee/{employee_id}", response_model=List[EducationExperienceOut])
def get_by_employee_id(employee_id: int, db: Session = Depends(get_db)):
    results = db.query(models.EducationExperience).filter_by(employee_id=employee_id).all()
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No education experience found for employee {employee_id}"
        )
    return results


# -------------------- Update Education Experience --------------------
@router.patch("/{experience_id}", response_model=schemas.EducationExperienceOut)
def update_education_experience(
    experience_id: int,
    update_data: schemas.EducationExperienceUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    exp = db.query(models.EducationExperience).filter_by(id=experience_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Education experience not found")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(exp, key, value)

    exp.updated_by_user_id = current_user.id
    db.commit()
    db.refresh(exp)
    return exp

# -------------------- Delete Education Experience --------------------
@router.delete("/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_education_experience(experience_id: int, db: Session = Depends(get_db)):
    exp = db.query(models.EducationExperience).filter_by(id=experience_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Education experience not found")

    db.delete(exp)
    db.commit()
    return None
