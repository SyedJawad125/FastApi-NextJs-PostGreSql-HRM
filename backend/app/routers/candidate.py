from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from .. import database, schemas, models, oauth2
from app.utils import filter_candidates, paginate_data
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/candidates",
    tags=["Candidates"]
)

# ✅ Get all candidates with filtering + pagination
@router.get("/", response_model=schemas.CandidateListResponse)
def get_candidates(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.Candidate)
        query = filter_candidates(request.query_params, query)

        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        serialized_data = [schemas.CandidateOut.from_orm(candidate) for candidate in paginated_data]

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

# ✅ Create new candidate
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CandidateOut)
def create_candidate(
    candidate: schemas.CandidateCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        candidate_data = candidate.dict(exclude_unset=True)
        candidate_data["created_by_user_id"] = current_user.id
        candidate_data["updated_by_user_id"] = None

        new_candidate = models.Candidate(**candidate_data)
        db.add(new_candidate)
        db.commit()
        db.refresh(new_candidate)

        return new_candidate

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Get single candidate by ID
@router.get("/{id}", response_model=schemas.CandidateOut)
def get_candidate(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    candidate = db.query(models.Candidate).filter(models.Candidate.id == id).first()

    if not candidate:
        raise HTTPException(status_code=404, detail=f"Candidate with id {id} not found")

    return candidate

# ✅ Update candidate
@router.patch("/{id}", response_model=schemas.CandidateOut)
def update_candidate(
    id: int,
    updated_data: schemas.CandidateUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        candidate_instance = db.query(models.Candidate).filter(models.Candidate.id == id).first()

        if not candidate_instance:
            raise HTTPException(status_code=404, detail=f"Candidate with id {id} not found")

        update_dict = updated_data.dict(exclude_unset=True)
        update_dict["updated_by_user_id"] = current_user.id

        for key, value in update_dict.items():
            setattr(candidate_instance, key, value)

        db.commit()
        db.refresh(candidate_instance)

        return candidate_instance

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Delete candidate
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_candidate(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    candidate_query = db.query(models.Candidate).filter(models.Candidate.id == id)
    candidate = candidate_query.first()

    if not candidate:
        raise HTTPException(status_code=404, detail=f"Candidate with id {id} not found")

    candidate_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Candidate deleted successfully"}
