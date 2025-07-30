from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from app import database, schemas, models, oauth2
from app.utils import filter_promotion_histories, paginate_data
import traceback
from sqlalchemy import or_
from datetime import date

router = APIRouter(
    prefix="/promotion-histories",
    tags=["Promotion Histories"]
)

# ✅ Get all promotion histories
import traceback

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import date
import traceback





@router.get("/", response_model=schemas.PromotionHistoryListResponse)
def get_promotion_histories(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.PromotionHistory)

        # Extract and parse query parameters
        params = request.query_params
        employee_id = params.get("employee_id")
        previous_rank_id = params.get("previous_rank_id")
        new_rank_id = params.get("new_rank_id")
        promotion_date = params.get("promotion_date")
        search = params.get("search")

        # Apply filters inline
        if employee_id:
            query = query.filter(models.PromotionHistory.employee_id == int(employee_id))

        if previous_rank_id:
            query = query.filter(models.PromotionHistory.previous_rank_id == int(previous_rank_id))

        if new_rank_id:
            query = query.filter(models.PromotionHistory.new_rank_id == int(new_rank_id))

        if promotion_date:
            query = query.filter(models.PromotionHistory.promotion_date == date.fromisoformat(promotion_date))

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    models.PromotionHistory.remarks.ilike(search_pattern),
                    # Add more searchable fields here if needed
                )
            )

        # Get and paginate results
        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        response_data = {
            "count": count,
            "data": [schemas.PromotionHistoryOut.from_orm(ph) for ph in paginated_data]
        }

        return {"status": "SUCCESSFUL", "result": response_data}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



# ✅ Create new promotion history
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PromotionHistoryOut)
def create_promotion_history(
    promotion_data: schemas.PromotionHistoryCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        data = promotion_data.dict(exclude_unset=True)
        data["created_by_user_id"] = current_user.id
        new_record = models.PromotionHistory(**data)
        db.add(new_record)
        db.commit()
        db.refresh(new_record)

        return new_record

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Get single promotion history
@router.get("/{id}", response_model=schemas.PromotionHistoryOut)
def get_promotion_history(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    record = db.query(models.PromotionHistory).filter(models.PromotionHistory.id == id).first()

    if not record:
        raise HTTPException(status_code=404, detail=f"Promotion history with id {id} not found")

    return record


# ✅ Update promotion history
@router.patch("/{id}", response_model=schemas.PromotionHistoryOut)
def update_promotion_history(
    id: int,
    updates: schemas.PromotionHistoryUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    record = db.query(models.PromotionHistory).filter(models.PromotionHistory.id == id).first()

    if not record:
        raise HTTPException(status_code=404, detail=f"Promotion history with id {id} not found")

    update_data = updates.dict(exclude_unset=True)
    update_data["updated_by_user_id"] = current_user.id

    for key, value in update_data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record


# ✅ Delete promotion history
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_promotion_history(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    query = db.query(models.PromotionHistory).filter(models.PromotionHistory.id == id)
    record = query.first()

    if not record:
        raise HTTPException(status_code=404, detail=f"Promotion history with id {id} not found")

    query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Promotion history deleted successfully"}
