from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from .. import database, schemas, models, oauth2
from app.utils import paginate_data, filter_training_participants

router = APIRouter(
    prefix="/training-participants",
    tags=["Training Participants"]
)


@router.get("/", response_model=schemas.TrainingParticipantListResponse)
def get_training_participants(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.TrainingParticipant)
        query = filter_training_participants(request.query_params, query)

        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        serialized_data = [
            schemas.TrainingParticipantOut.from_orm(record) for record in paginated_data
        ]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized_data
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TrainingParticipantOut)
def create_training_participant(
    participant: schemas.TrainingParticipantCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        participant_data = participant.dict()
        participant_data["created_by_user_id"] = current_user.id
        participant_data["updated_by_user_id"] = None

        new_participant = models.TrainingParticipant(**participant_data)
        db.add(new_participant)
        db.commit()
        db.refresh(new_participant)

        return new_participant

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=schemas.TrainingParticipantOut)
def get_training_participant(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    record = db.query(models.TrainingParticipant).filter(models.TrainingParticipant.id == id).first()

    if not record:
        raise HTTPException(status_code=404, detail=f"Training participant with id {id} not found")

    return record


@router.patch("/{id}", response_model=schemas.TrainingParticipantOut)
def update_training_participant(
    id: int,
    updated_data: schemas.TrainingParticipantUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        instance = db.query(models.TrainingParticipant).filter(models.TrainingParticipant.id == id).first()

        if not instance:
            raise HTTPException(status_code=404, detail=f"Training participant with id {id} not found")

        update_dict = updated_data.dict(exclude_unset=True)
        update_dict["updated_by_user_id"] = current_user.id

        for key, value in update_dict.items():
            setattr(instance, key, value)

        db.commit()
        db.refresh(instance)

        return instance

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_training_participant(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    query = db.query(models.TrainingParticipant).filter(models.TrainingParticipant.id == id)
    record = query.first()

    if not record:
        raise HTTPException(status_code=404, detail=f"Training participant with id {id} not found")

    query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Training participant deleted successfully"}
