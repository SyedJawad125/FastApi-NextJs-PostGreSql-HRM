from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from .. import database, schemas, models, oauth2
from app.utils import filter_shifts, paginate_data

router = APIRouter(
    prefix="/shifts",
    tags=["Shifts"]
)


@router.get("/", response_model=schemas.ShiftListResponse)
def get_shifts(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    try:
        query = db.query(models.Shift)
        query = filter_shifts(request.query_params, query)
        data = query.all()
        paginated_data, count = paginate_data(data, request)

        serialized_data = [schemas.ShiftOut.from_orm(shift) for shift in paginated_data]

        return {
            "count": count,
            "data": serialized_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShiftOut)
def create_shift(
    shift: schemas.ShiftCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        # Create a dictionary from the input data
        shift_data = shift.dict()
        
        # Create the database model instance with all data at once
        new_shift = models.Shift(
            **shift_data,
            created_by_user_id=current_user.id
        )
        
        db.add(new_shift)
        db.commit()
        db.refresh(new_shift)
        return new_shift
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=schemas.ShiftOut)
def get_shift(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    shift = db.query(models.Shift).filter(models.Shift.id == id).first()
    if not shift:
        raise HTTPException(status_code=404, detail=f"Shift with id {id} not found")
    return shift


@router.patch("/{id}", response_model=schemas.ShiftOut)
def update_shift(
    id: int,
    shift_update: schemas.ShiftUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    shift = db.query(models.Shift).filter(models.Shift.id == id).first()
    if not shift:
        raise HTTPException(status_code=404, detail=f"Shift with id {id} not found")

    update_data = shift_update.dict(exclude_unset=True)
    update_data["updated_by_user_id"] = current_user.id

    for key, value in update_data.items():
        setattr(shift, key, value)

    db.commit()
    db.refresh(shift)
    return shift


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_shift(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    shift = db.query(models.Shift).filter(models.Shift.id == id).first()
    if not shift:
        raise HTTPException(status_code=404, detail=f"Shift with id {id} not found")

    db.delete(shift)
    db.commit()
    return {"message": "Shift deleted successfully"}
