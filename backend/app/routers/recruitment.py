from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from .. import database, schemas, models, oauth2
from app.utils import paginate_data, filter_recruitments
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/recruitments",
    tags=["Recruitments"]
)


@router.get("/", response_model=schemas.RecruitmentListResponse)
def get_recruitments(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.Recruitment)
        query = filter_recruitments(request.query_params, query)

        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        serialized_data = [schemas.RecruitmentOut.from_orm(r) for r in paginated_data]

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


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.RecruitmentOut)
def create_recruitment(
    payload: schemas.RecruitmentCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        recruitment_data = payload.dict()
        recruitment_data["created_by_user_id"] = current_user.id
        recruitment_data["updated_by_user_id"] = None

        new_recruitment = models.Recruitment(**recruitment_data)
        db.add(new_recruitment)
        db.commit()
        db.refresh(new_recruitment)

        return new_recruitment

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=schemas.RecruitmentOut)
def get_recruitment(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    recruitment = db.query(models.Recruitment).filter(models.Recruitment.id == id).first()

    if not recruitment:
        raise HTTPException(status_code=404, detail=f"Recruitment with id {id} not found")

    return recruitment


@router.patch("/{id}", response_model=schemas.RecruitmentOut)
def update_recruitment(
    id: int,
    updated_data: schemas.RecruitmentUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        recruitment_instance = db.query(models.Recruitment).filter(models.Recruitment.id == id).first()

        if not recruitment_instance:
            raise HTTPException(status_code=404, detail=f"Recruitment with id {id} not found")

        update_dict = updated_data.dict(exclude_unset=True)
        update_dict["updated_by_user_id"] = current_user.id

        for key, value in update_dict.items():
            setattr(recruitment_instance, key, value)

        db.commit()
        db.refresh(recruitment_instance)

        return recruitment_instance

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_recruitment(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    recruitment_query = db.query(models.Recruitment).filter(models.Recruitment.id == id)
    recruitment = recruitment_query.first()

    if not recruitment:
        raise HTTPException(status_code=404, detail=f"Recruitment with id {id} not found")

    recruitment_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Recruitment deleted successfully"}
