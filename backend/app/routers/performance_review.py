from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from app import database, schemas, models, oauth2
from app.utils import paginate_data
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/performance-reviews",
    tags=["Performance Reviews"]
)


@router.get("/", response_model=schemas.PerformanceReviewListResponse)
def get_performance_reviews(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.PerformanceReview)

        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        serialized_data = [schemas.PerformanceReviewOut.from_orm(review) for review in paginated_data]

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


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PerformanceReviewOut)
def create_performance_review(
    review: schemas.PerformanceReviewCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        review_data = review.dict()
        review_data["created_by_user_id"] = current_user.id
        review_data["updated_by_user_id"] = None

        new_review = models.PerformanceReview(**review_data)
        db.add(new_review)
        db.commit()
        db.refresh(new_review)

        return new_review

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=schemas.PerformanceReviewOut)
def get_performance_review(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    review = db.query(models.PerformanceReview).filter(models.PerformanceReview.id == id).first()

    if not review:
        raise HTTPException(status_code=404, detail=f"Performance review with id {id} not found")

    return review


@router.patch("/{id}", response_model=schemas.PerformanceReviewOut)
def update_performance_review(
    id: int,
    updated_data: schemas.PerformanceReviewUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        review_instance = db.query(models.PerformanceReview).filter(models.PerformanceReview.id == id).first()

        if not review_instance:
            raise HTTPException(status_code=404, detail=f"Performance review with id {id} not found")

        update_dict = updated_data.dict(exclude_unset=True)
        update_dict["updated_by_user_id"] = current_user.id

        for key, value in update_dict.items():
            setattr(review_instance, key, value)

        db.commit()
        db.refresh(review_instance)

        return review_instance

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_performance_review(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    review_query = db.query(models.PerformanceReview).filter(models.PerformanceReview.id == id)
    review = review_query.first()

    if not review:
        raise HTTPException(status_code=404, detail=f"Performance review with id {id} not found")

    review_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Performance review deleted successfully"}
