from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from .. import database, schemas, models, oauth2
from app.utils import filter_trainings, paginate_data  # optional: if you use pagination
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/trainings",
    tags=["Trainings"]
)


@router.get("/", response_model=schemas.TrainingListResponse)
def get_trainings(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.Training)
        query = filter_trainings(request.query_params, query)

        # Optional: Add filters if needed
        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        serialized_data = [schemas.TrainingOut.from_orm(training) for training in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized_data
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TrainingOut)
def create_training(
    training: schemas.TrainingCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        training_data = training.dict()
        training_data["created_by_user_id"] = current_user.id
        training_data["updated_by_user_id"] = None

        new_training = models.Training(**training_data)
        db.add(new_training)
        db.commit()
        db.refresh(new_training)

        return new_training

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=schemas.TrainingOut)
def get_training(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    training = db.query(models.Training).filter(models.Training.id == id).first()

    if not training:
        raise HTTPException(status_code=404, detail=f"Training with id {id} not found")

    return training


@router.patch("/{id}", response_model=schemas.TrainingOut)
def update_training(
    id: int,
    updated_data: schemas.TrainingUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        training_instance = db.query(models.Training).filter(models.Training.id == id).first()

        if not training_instance:
            raise HTTPException(status_code=404, detail=f"Training with id {id} not found")

        update_dict = updated_data.dict(exclude_unset=True)
        update_dict["updated_by_user_id"] = current_user.id

        for key, value in update_dict.items():
            setattr(training_instance, key, value)

        db.commit()
        db.refresh(training_instance)

        return training_instance

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_training(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    training_query = db.query(models.Training).filter(models.Training.id == id)
    training = training_query.first()

    if not training:
        raise HTTPException(status_code=404, detail=f"Training with id {id} not found")

    training_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Training deleted successfully"}
