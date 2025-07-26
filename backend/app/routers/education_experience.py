from fastapi import APIRouter, HTTPException, status, Depends, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models
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
@router.post("/", response_model=List[EducationExperienceOut])
def create_education_experiences(
    items: List[EducationExperienceCreate],
    db: Session = Depends(get_db),
    created_by_user_id: Optional[int] = 1  # replace with user from token/session
):
    """
    Create one or multiple education experiences.
    """
    created = []
    for item in items:
        experience = models.EducationExperience(**item.dict())
        experience.created_by_user_id = created_by_user_id
        db.add(experience)
        created.append(experience)
    db.commit()
    for c in created:
        db.refresh(c)
    return created


# -------------------- Get All with Pagination --------------------
@router.get("/", response_model=PaginatedEducationExperiences)
def get_all_education_experiences(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get paginated list of all education experiences.
    """
    total = db.query(models.EducationExperience).count()
    experiences = db.query(models.EducationExperience).offset(skip).limit(limit).all()
    return {"count": total, "data": experiences}


# -------------------- Get by Employee --------------------
@router.get("/employee/{employee_id}", response_model=List[EducationExperienceOut])
def get_by_employee_id(employee_id: int, db: Session = Depends(get_db)):
    """
    Get all education experiences for a specific employee.
    """
    results = db.query(models.EducationExperience).filter_by(employee_id=employee_id).all()
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No education experience found for employee {employee_id}"
        )
    return results


# -------------------- Update Education Experience --------------------
@router.patch("/{experience_id}", response_model=EducationExperienceOut)
def update_education_experience(
    experience_id: int,
    update_data: EducationExperienceUpdate,
    db: Session = Depends(get_db),
    updated_by_user_id: Optional[int] = 1  # replace with user from token/session
):
    """
    Update a single education experience.
    """
    exp = db.query(models.EducationExperience).filter_by(id=experience_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Education experience not found")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(exp, key, value)

    exp.updated_by_user_id = updated_by_user_id
    db.commit()
    db.refresh(exp)
    return exp


# -------------------- Delete Education Experience --------------------
@router.delete("/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_education_experience(experience_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific education experience.
    """
    exp = db.query(models.EducationExperience).filter_by(id=experience_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Education experience not found")

    db.delete(exp)
    db.commit()
    return None
