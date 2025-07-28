from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from .. import database, schemas, models, oauth2
from app.utils import filter_health_checkups, paginate_data  # Assume this paginates based on offset/limit
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/health-checkups",
    tags=["HealthCheckUps"]
)


# --- 📄 GET All with Filtering + Pagination ---
@router.get("/", response_model=schemas.HealthCheckUpListResponse)
def get_health_checkups(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.HealthCheckUp)
        query = filter_health_checkups(request.query_params, query)

        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        serialized_data = [schemas.HealthCheckUpOut.from_orm(item) for item in paginated_data]

        response_data = {
            "count": count,
            "data": serialized_data
        }

        return {
            "status": "SUCCESSFUL",
            "result": response_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- 🆕 CREATE ---
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.HealthCheckUpOut)
def create_health_checkup(
    health_data: schemas.HealthCheckUpCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        data_dict = health_data.dict()
        data_dict["created_by_user_id"] = current_user.id
        data_dict["updated_by_user_id"] = None

        new_entry = models.HealthCheckUp(**data_dict)
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)

        return new_entry

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- 🔍 GET by ID ---
@router.get("/{id}", response_model=schemas.HealthCheckUpOut)
def get_health_checkup_by_id(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    item = db.query(models.HealthCheckUp).filter(models.HealthCheckUp.id == id).first()

    if not item:
        raise HTTPException(status_code=404, detail=f"HealthCheckUp with id {id} not found")

    return item


# --- ✏️ UPDATE (PATCH) ---
@router.patch("/{id}", response_model=schemas.HealthCheckUpOut)
def update_health_checkup(
    id: int,
    updated_data: schemas.HealthCheckUpUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        instance = db.query(models.HealthCheckUp).filter(models.HealthCheckUp.id == id).first()

        if not instance:
            raise HTTPException(status_code=404, detail=f"HealthCheckUp with id {id} not found")

        update_dict = updated_data.dict(exclude_unset=True)
        update_dict["updated_by_user_id"] = current_user.id

        for key, value in update_dict.items():
            setattr(instance, key, value)

        db.commit()
        db.refresh(instance)

        return instance

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- ❌ DELETE ---
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_health_checkup(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    query = db.query(models.HealthCheckUp).filter(models.HealthCheckUp.id == id)
    instance = query.first()

    if not instance:
        raise HTTPException(status_code=404, detail=f"HealthCheckUp with id {id} not found")

    query.delete(synchronize_session=False)
    db.commit()

    return {"message": "HealthCheckUp deleted successfully"}
