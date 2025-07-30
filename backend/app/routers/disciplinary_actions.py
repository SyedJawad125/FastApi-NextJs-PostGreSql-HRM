from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from .. import database, schemas, models, oauth2
from app.utils import paginate_data, filter_disciplinary_actions # You must have this utility

router = APIRouter(
    prefix="/disciplinary-actions",
    tags=["Disciplinary Actions"]
)

# ✅ Get all disciplinary actions with filters and pagination
@router.get("/", response_model=schemas.DisciplinaryActionListResponse)
def get_disciplinary_actions(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.DisciplinaryAction)

        # Apply filters
        query = filter_disciplinary_actions(request.query_params, query)

        all_data = query.all()

        # Apply pagination
        paginated_data, count = paginate_data(all_data, request)

        # Serialize response
        serialized = [schemas.DisciplinaryActionOut.from_orm(item) for item in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Create a new disciplinary action
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DisciplinaryActionOut)
def create_disciplinary_action(
    payload: schemas.DisciplinaryActionCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        data = payload.dict(exclude_unset=True)
        data["created_by_user_id"] = current_user.id
        data["updated_by_user_id"] = None

        new_action = models.DisciplinaryAction(**data)
        db.add(new_action)
        db.commit()
        db.refresh(new_action)

        return new_action

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Get by ID
@router.get("/{id}", response_model=schemas.DisciplinaryActionOut)
def get_disciplinary_action_by_id(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    item = db.query(models.DisciplinaryAction).filter(models.DisciplinaryAction.id == id).first()

    if not item:
        raise HTTPException(status_code=404, detail=f"Disciplinary action with id {id} not found")

    return item


# ✅ Update by ID
@router.patch("/{id}", response_model=schemas.DisciplinaryActionOut)
def update_disciplinary_action(
    id: int,
    payload: schemas.DisciplinaryActionUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        item = db.query(models.DisciplinaryAction).filter(models.DisciplinaryAction.id == id).first()

        if not item:
            raise HTTPException(status_code=404, detail=f"Disciplinary action with id {id} not found")

        updates = payload.dict(exclude_unset=True)
        updates["updated_by_user_id"] = current_user.id

        for key, value in updates.items():
            setattr(item, key, value)

        db.commit()
        db.refresh(item)

        return item

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Delete by ID
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_disciplinary_action(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    query = db.query(models.DisciplinaryAction).filter(models.DisciplinaryAction.id == id)
    item = query.first()

    if not item:
        raise HTTPException(status_code=404, detail=f"Disciplinary action with id {id} not found")

    query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Disciplinary action deleted successfully"}
