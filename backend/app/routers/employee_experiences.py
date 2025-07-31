from fastapi import APIRouter, HTTPException, status, Request, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app import database
from app.utils import filter_employee_experiences, paginate_data
from app import models
from app.schemas import (
    EmployeeExperienceCreate,
    EmployeeExperienceUpdate,
    EmployeeExperienceOut,
    PaginatedEmployeeExperiences
)
from app.database import get_db

router = APIRouter(
    prefix="/employee-experiences",
    tags=["Employee Experiences"]
)

# -------------------- Create One or Many --------------------
@router.post("/", response_model=List[EmployeeExperienceOut])
def create_employee_experiences(
    items: List[EmployeeExperienceCreate],
    db: Session = Depends(get_db),
    created_by_user_id: Optional[int] = 1  # Replace with token-based user
):
    """
    Create one or multiple employee experiences.
    """
    created = []
    for item in items:
        experience = models.EmployeeExperience(**item.dict())
        experience.created_by_user_id = created_by_user_id
        db.add(experience)
        created.append(experience)
    db.commit()
    for c in created:
        db.refresh(c)
    return created


# -------------------- Get All with Pagination --------------------
@router.get("/", response_model=PaginatedEmployeeExperiences)
def get_all_employee_experiences(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Get paginated and optionally filtered list of employee experiences.
    """
    query = db.query(models.EmployeeExperience)

    # Extract query parameters as dictionary
    params = dict(request.query_params)
    query = filter_employee_experiences(params, query)

    all_results = query.all()
    paginated_data, total = paginate_data(all_results, request)

    return {"count": total, "data": paginated_data}


# -------------------- Get by Employee --------------------
@router.get("/employee/{employee_id}", response_model=List[EmployeeExperienceOut])
def get_by_employee_id(employee_id: int, db: Session = Depends(get_db)):
    """
    Get all experiences for a specific employee.
    """
    results = db.query(models.EmployeeExperience).filter_by(employee_id=employee_id).all()
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No experience found for employee {employee_id}"
        )
    return results


# -------------------- Update Employee Experience --------------------
@router.patch("/{experience_id}", response_model=EmployeeExperienceOut)
def update_employee_experience(
    experience_id: int,
    update_data: EmployeeExperienceUpdate,
    db: Session = Depends(get_db),
    updated_by_user_id: Optional[int] = 1  # Replace with token-based user
):
    """
    Update a single employee experience.
    """
    exp = db.query(models.EmployeeExperience).filter_by(id=experience_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(exp, key, value)

    exp.updated_by_user_id = updated_by_user_id
    db.commit()
    db.refresh(exp)
    return exp


# -------------------- Delete Employee Experience --------------------
@router.delete("/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee_experience(
    experience_id: int,
    db: Session = Depends(database.get_db)
):
    """
    Delete a specific employee experience.
    """
    experience_query = db.query(models.EmployeeExperience).filter(models.EmployeeExperience.id == experience_id)
    experience = experience_query.first()

    if not experience:
        raise HTTPException(status_code=404, detail=f"Experience with id {experience_id} not found")

    experience_query.delete(synchronize_session=False)
    db.commit()
    
    return {"message": "Experience deleted successfully"}
