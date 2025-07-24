from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from .. import database, schemas, models, oauth2
from app.utils import filter_shift_assignments, paginate_data

router = APIRouter(
    prefix="/shift-assignments",
    tags=["Shift Assignments"]
)


@router.get("/", response_model=schemas.ShiftAssignmentListResponse)
def get_shift_assignments(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    try:
        query = db.query(models.ShiftAssignment)
        query = filter_shift_assignments(request.query_params, query)
        data = query.all()
        paginated_data, count = paginate_data(data, request)

        serialized_data = [schemas.ShiftAssignmentOut.from_orm(sa) for sa in paginated_data]

        return {
            "count": count,
            "data": serialized_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShiftAssignmentOut)
def create_shift_assignment(
    shift_assignment: schemas.ShiftAssignmentCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        data = shift_assignment.dict()
        new_item = models.ShiftAssignment(
            **data,
            created_by_user_id=current_user.id,
            updated_by_user_id=current_user.id  # Optional initial update
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=schemas.ShiftAssignmentOut)
def get_shift_assignment(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    item = db.query(models.ShiftAssignment).filter(models.ShiftAssignment.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"ShiftAssignment with id {id} not found")
    return item


@router.patch("/{id}", response_model=schemas.ShiftAssignmentOut)
def update_shift_assignment(
    id: int,
    shift_assignment_update: schemas.ShiftAssignmentUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    item = db.query(models.ShiftAssignment).filter(models.ShiftAssignment.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"ShiftAssignment with id {id} not found")

    update_data = shift_assignment_update.dict(exclude_unset=True)
    update_data["updated_by_user_id"] = current_user.id

    for key, value in update_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_shift_assignment(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    item = db.query(models.ShiftAssignment).filter(models.ShiftAssignment.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"ShiftAssignment with id {id} not found")

    db.delete(item)
    db.commit()
    return {"message": "ShiftAssignment deleted successfully"}
