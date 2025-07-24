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
        # Step 1: Fetch holiday
        holiday = db.query(models.HolidayCalendar).filter(models.HolidayCalendar.id == id).first()
        if not holiday:
            raise HTTPException(status_code=404, detail=f"Holiday with id {id} not found")

        # Step 2: Extract fields that were actually sent
        update_fields = updated_data.dict(exclude_unset=True)

        # Step 3: Handle employee_ids if present
        if "employee_ids" in update_fields:
            employee_ids = update_fields.pop("employee_ids")  # Could be [] or List[int]
            employees = (
                db.query(models.Employee).filter(models.Employee.id.in_(employee_ids)).all()
                if employee_ids else []
            )
            holiday.employees = employees  # Assign or clear employees

        # Step 4: Update remaining fields
        for key, value in update_fields.items():
            setattr(holiday, key, value)

        # Step 5: Track the user who updated it
        holiday.updated_by_user_id = current_user.id

        # Step 6: Save changes
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
        # Check if holiday exists
        holiday = db.query(models.HolidayCalendar).get(id)
        if not holiday:
            raise HTTPException(
                status_code=404, 
                detail=f"Holiday with id {id} not found"
            )

        # Attempt deletion
        db.delete(holiday)
        db.commit()
        
        return {"message": "Holiday deleted successfully"}

    except HTTPException:
        # Re-raise HTTP exceptions (like the 404 we might raise)
        raise
        
    except SQLAlchemyError as e:
        db.rollback()
        print(f"❌ Database error deleting holiday {id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while deleting holiday"
        )
        
    except Exception as e:
        print(f"❌ Unexpected error deleting holiday {id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )