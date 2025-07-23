from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any
from app import database, schemas, models, oauth2
from app.utils import paginate_data
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/holidays",
    tags=["Holidays"]
)


# ---------------------- GET All Holidays ----------------------
@router.get("/", response_model=Any)
def get_holidays(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    try:
        query = db.query(models.HolidayCalendar)
        data = query.all()
        paginated_data, count = paginate_data(data, request)

        serialized_data = [schemas.HolidayCalendarOut.from_orm(holiday) for holiday in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized_data
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------- POST Create Holiday ----------------------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.HolidayCalendarOut)
def create_holiday(
    holiday: schemas.HolidayCalendarCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        holiday_data = holiday.dict()
        employee_ids = holiday_data.pop("employee_ids", [])  # Remove before creating model instance
        holiday_data["created_by_user_id"] = current_user.id

        # Create holiday record
        new_holiday = models.HolidayCalendar(**holiday_data)

        # Attach employees (many-to-many)
        if employee_ids:
            employees = db.query(models.Employee).filter(models.Employee.id.in_(employee_ids)).all()
            new_holiday.employees = employees

        db.add(new_holiday)
        db.commit()
        db.refresh(new_holiday)

        return new_holiday

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Create error: {str(e)}")



# ---------------------- GET One Holiday ----------------------
@router.get("/{id}", response_model=schemas.HolidayCalendarOut)
def get_holiday(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    holiday = db.query(models.HolidayCalendar).filter(models.HolidayCalendar.id == id).first()
    if not holiday:
        raise HTTPException(status_code=404, detail=f"Holiday with id {id} not found")
    return holiday


# ---------------------- PATCH Update Holiday ----------------------
@router.patch("/{id}", response_model=schemas.HolidayCalendarOut)
def update_holiday(
    id: int,
    updated_data: schemas.HolidayCalendarUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    try:
        holiday = db.query(models.HolidayCalendar).filter(models.HolidayCalendar.id == id).first()
        if not holiday:
            raise HTTPException(status_code=404, detail=f"Holiday with id {id} not found")

        update_fields = updated_data.dict(exclude_unset=True)

        # Handle employee reassignment if provided
        if "employee_ids" in update_fields:
            employee_ids = update_fields.pop("employee_ids")
            if employee_ids is not None:
                employees = db.query(models.Employee).filter(models.Employee.id.in_(employee_ids)).all()
                holiday.employees = employees

        for key, value in update_fields.items():
            setattr(holiday, key, value)

        holiday.updated_by_user_id = current_user.id

        db.commit()
        db.refresh(holiday)

        return holiday

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update error: {str(e)}")


# ---------------------- DELETE Holiday ----------------------
@router.delete("/{id}", status_code=200)
def delete_holiday(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        holiday_query = db.query(models.HolidayCalendar).filter(models.HolidayCalendar.id == id)
        holiday = holiday_query.first()

        if not holiday:
            raise HTTPException(status_code=404, detail=f"Holiday with id {id} not found")

        holiday_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Holiday deleted successfully"}

    except Exception as e:
        print(f"❌ ERROR deleting holiday {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
