import datetime
from fastapi import APIRouter, Depends, Path, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from app import schemas, models, database, oauth2
from app.models.employee_loan import EmployeeLoan
from app.models.user import User
from app.schemas.employee_loan import EmployeeLoanOut
from app.utils import filter_employee_loans, paginate_data

router = APIRouter(
    prefix="/employee-loans",
    tags=["Employee Loans"]
)

# ✅ Get all loans with pagination
@router.get("/", response_model=schemas.EmployeeLoanListResponse)
def get_loans(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.EmployeeLoan)
        # ✅ Apply filters from query params
        query = filter_employee_loans(request.query_params, query)

        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        serialized_data = [schemas.EmployeeLoanOut.from_orm(loan) for loan in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized_data
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Create new loan
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.EmployeeLoanOut)
def create_loan(
    loan: schemas.EmployeeLoanCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        loan_data = loan.dict(exclude_unset=True)
        loan_data["created_by_user_id"] = current_user.id
        loan_data["updated_by_user_id"] = None
        loan_data["status"] = "pending"  # Always default to pending

        new_loan = models.EmployeeLoan(**loan_data)
        db.add(new_loan)
        db.commit()
        db.refresh(new_loan)

        return new_loan

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Get single loan by ID
@router.get("/{id}", response_model=schemas.EmployeeLoanOut)
def get_loan(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    loan = db.query(models.EmployeeLoan).filter(models.EmployeeLoan.id == id).first()

    if not loan:
        raise HTTPException(status_code=404, detail=f"Loan with ID {id} not found")

    return loan


# ✅ Update loan
@router.patch("/{id}", response_model=schemas.EmployeeLoanOut)
def update_loan(
    id: int,
    updated_data: schemas.EmployeeLoanUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        loan_instance = db.query(models.EmployeeLoan).filter(models.EmployeeLoan.id == id).first()

        if not loan_instance:
            raise HTTPException(status_code=404, detail=f"Loan with ID {id} not found")

        update_dict = updated_data.dict(exclude_unset=True)

        # ❌ Prevent anyone from manually approving via this API
        if "status" in update_dict or "approved_by_user_id" in update_dict:
            raise HTTPException(status_code=403, detail="You are not allowed to approve a loan from this endpoint")

        update_dict["updated_by_user_id"] = current_user.id

        for key, value in update_dict.items():
            setattr(loan_instance, key, value)

        db.commit()
        db.refresh(loan_instance)

        return loan_instance

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from datetime import datetime


@router.patch("/{loan_id}/approve", response_model=EmployeeLoanOut)
def approve_employee_loan(
    loan_id: int = Path(..., gt=0),
    db: Session = Depends(database.get_db),
    current_user: User = Depends(oauth2.get_current_user)
):
    # ✅ Only superusers or CEOs can approve
    if not current_user.is_superuser and getattr(current_user.role, "name", None) != "CEO":
        raise HTTPException(status_code=403, detail="Only superuser or CEO can approve loans")



    loan = db.query(EmployeeLoan).filter(EmployeeLoan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    if loan.status == "approved":
        raise HTTPException(status_code=400, detail="Loan is already approved")

    loan.status = "approved"
    loan.approved_by_user_id = current_user.id
    loan.updated_by_user_id = current_user.id
    loan.updated_at = datetime.utcnow()


    db.commit()
    db.refresh(loan)
    return loan



# ✅ Delete loan
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_loan(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    loan_query = db.query(models.EmployeeLoan).filter(models.EmployeeLoan.id == id)
    loan = loan_query.first()

    if not loan:
        raise HTTPException(status_code=404, detail=f"Loan with ID {id} not found")

    loan_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Loan deleted successfully"}
