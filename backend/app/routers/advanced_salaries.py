from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from .. import models, schemas, database, oauth2
from app.utils import filter_advanced_salaries, paginate_data  # ensure you have this utility

router = APIRouter(
    prefix="/advanced-salaries",
    tags=["Advanced Salaries"]
)

# ✅ GET all advanced salaries (paginated with filters)
@router.get("/", response_model=schemas.AdvancedSalaryListResponse)
def get_advanced_salaries(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.AdvancedSalary)

        # ✅ Apply filters using query parameters
        query = filter_advanced_salaries(request.query_params, query)

        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        serialized = [schemas.AdvancedSalaryOut.from_orm(sal) for sal in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# ✅ POST create advanced salary
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AdvancedSalaryOut)
def create_advanced_salary(
    salary: schemas.AdvancedSalaryCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        data = salary.dict()
        data["created_by_user_id"] = current_user.id
        data["updated_by_user_id"] = None

        new_salary = models.AdvancedSalary(**data)
        db.add(new_salary)
        db.commit()
        db.refresh(new_salary)

        return new_salary

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ GET advanced salary by ID
@router.get("/{id}", response_model=schemas.AdvancedSalaryOut)
def get_advanced_salary_by_id(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    salary = db.query(models.AdvancedSalary).filter(models.AdvancedSalary.id == id).first()

    if not salary:
        raise HTTPException(status_code=404, detail=f"AdvancedSalary with id {id} not found")

    return salary


# ✅ PATCH update advanced salary
@router.patch("/{id}", response_model=schemas.AdvancedSalaryOut)
def update_advanced_salary(
    id: int,
    salary_update: schemas.AdvancedSalaryUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        salary = db.query(models.AdvancedSalary).filter(models.AdvancedSalary.id == id).first()

        if not salary:
            raise HTTPException(status_code=404, detail=f"AdvancedSalary with id {id} not found")

        update_dict = salary_update.dict(exclude_unset=True)
        update_dict["updated_by_user_id"] = current_user.id

        for key, value in update_dict.items():
            setattr(salary, key, value)

        db.commit()
        db.refresh(salary)

        return salary

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ DELETE advanced salary
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_advanced_salary(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    salary_query = db.query(models.AdvancedSalary).filter(models.AdvancedSalary.id == id)
    salary = salary_query.first()

    if not salary:
        raise HTTPException(status_code=404, detail=f"AdvancedSalary with id {id} not found")

    salary_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "AdvancedSalary deleted successfully"}
