from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from app import models, schemas, database, oauth2
from app.utils import filter_travel_expenses, paginate_data  # Optional utility if you use it

router = APIRouter(
    prefix="/travel-expenses",
    tags=["Travel Expenses"]
)


# ✅ Get all travel expenses (with pagination)
@router.get("/", response_model=schemas.TravelExpenseListResponse)
def get_travel_expenses(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.TravelExpense)
        query = filter_travel_expenses(request.query_params, query)
        # Apply pagination (if any)
        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        serialized = [schemas.TravelExpenseOut.from_orm(item) for item in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Create a new travel expense
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TravelExpenseOut)
def create_travel_expense(
    expense: schemas.TravelExpenseCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        data = expense.dict(exclude_unset=True)
        data["created_by_user_id"] = current_user.id

        new_expense = models.TravelExpense(**data)
        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)

        return new_expense

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Get a single travel expense by ID
@router.get("/{id}", response_model=schemas.TravelExpenseOut)
def get_travel_expense(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    expense = db.query(models.TravelExpense).filter(models.TravelExpense.id == id).first()

    if not expense:
        raise HTTPException(status_code=404, detail=f"Travel expense with id {id} not found")

    return expense


# ✅ Update travel expense
@router.patch("/{id}", response_model=schemas.TravelExpenseOut)
def update_travel_expense(
    id: int,
    updated_data: schemas.TravelExpenseUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        expense = db.query(models.TravelExpense).filter(models.TravelExpense.id == id).first()

        if not expense:
            raise HTTPException(status_code=404, detail=f"Travel expense with id {id} not found")

        update_dict = updated_data.dict(exclude_unset=True)
        update_dict["updated_by_user_id"] = current_user.id

        for key, value in update_dict.items():
            setattr(expense, key, value)

        db.commit()
        db.refresh(expense)

        return expense

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Delete travel expense
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_travel_expense(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    expense_query = db.query(models.TravelExpense).filter(models.TravelExpense.id == id)
    expense = expense_query.first()

    if not expense:
        raise HTTPException(status_code=404, detail=f"Travel expense with id {id} not found")

    expense_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Travel expense deleted successfully"}
