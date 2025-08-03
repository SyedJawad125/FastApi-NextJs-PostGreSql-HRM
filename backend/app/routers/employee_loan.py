# import datetime
# from fastapi import APIRouter, Depends, Path, status, Request, HTTPException
# from sqlalchemy.orm import Session
# from typing import Any
# from app import schemas, models, database, oauth2
# from app.models.employee_loan import EmployeeLoan
# from app.models.user import User
# from app.schemas.employee_loan import EmployeeLoanOut
# from app.utils import filter_employee_loans, paginate_data

# router = APIRouter(
#     prefix="/employee-loans",
#     tags=["Employee Loans"]
# )

# # ✅ Get all loans with pagination
# @router.get("/", response_model=schemas.EmployeeLoanListResponse)
# def get_loans(
#     request: Request,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     try:
#         query = db.query(models.EmployeeLoan)
#         # ✅ Apply filters from query params
#         query = filter_employee_loans(request.query_params, query)

#         all_data = query.all()
#         paginated_data, count = paginate_data(all_data, request)

#         serialized_data = [schemas.EmployeeLoanOut.from_orm(loan) for loan in paginated_data]

#         return {
#             "status": "SUCCESSFUL",
#             "result": {
#                 "count": count,
#                 "data": serialized_data
#             }
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # ✅ Create new loan
# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.EmployeeLoanOut)
# def create_loan(
#     loan: schemas.EmployeeLoanCreate,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ) -> Any:
#     try:
#         loan_data = loan.dict(exclude_unset=True)
#         loan_data["created_by_user_id"] = current_user.id
#         loan_data["updated_by_user_id"] = None
#         loan_data["status"] = "pending"  # Always default to pending

#         new_loan = models.EmployeeLoan(**loan_data)
#         db.add(new_loan)
#         db.commit()
#         db.refresh(new_loan)

#         return new_loan

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # ✅ Get single loan by ID
# @router.get("/{id}", response_model=schemas.EmployeeLoanOut)
# def get_loan(
#     id: int,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     loan = db.query(models.EmployeeLoan).filter(models.EmployeeLoan.id == id).first()

#     if not loan:
#         raise HTTPException(status_code=404, detail=f"Loan with ID {id} not found")

#     return loan


# # ✅ Update loan
# @router.patch("/{id}", response_model=schemas.EmployeeLoanOut)
# def update_loan(
#     id: int,
#     updated_data: schemas.EmployeeLoanUpdate,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     try:
#         loan_instance = db.query(models.EmployeeLoan).filter(models.EmployeeLoan.id == id).first()

#         if not loan_instance:
#             raise HTTPException(status_code=404, detail=f"Loan with ID {id} not found")

#         update_dict = updated_data.dict(exclude_unset=True)

#         # ❌ Prevent anyone from manually approving via this API
#         if "status" in update_dict or "approved_by_user_id" in update_dict:
#             raise HTTPException(status_code=403, detail="You are not allowed to approve a loan from this endpoint")

#         update_dict["updated_by_user_id"] = current_user.id

#         for key, value in update_dict.items():
#             setattr(loan_instance, key, value)

#         db.commit()
#         db.refresh(loan_instance)

#         return loan_instance

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# from datetime import datetime


# @router.patch("/{loan_id}/approve", response_model=EmployeeLoanOut)
# def approve_employee_loan(
#     loan_id: int = Path(..., gt=0),
#     db: Session = Depends(database.get_db),
#     current_user: User = Depends(oauth2.get_current_user)
# ):
#     # ✅ Only superusers or CEOs can approve
#     if not current_user.is_superuser and getattr(current_user.role, "name", None) != "CEO":
#         raise HTTPException(status_code=403, detail="Only superuser or CEO can approve loans")



#     loan = db.query(EmployeeLoan).filter(EmployeeLoan.id == loan_id).first()
#     if not loan:
#         raise HTTPException(status_code=404, detail="Loan not found")
    
#     if loan.status == "approved":
#         raise HTTPException(status_code=400, detail="Loan is already approved")

#     loan.status = "approved"
#     loan.approved_by_user_id = current_user.id
#     loan.updated_by_user_id = current_user.id
#     loan.updated_at = datetime.utcnow()


#     db.commit()
#     db.refresh(loan)
#     return loan



# # ✅ Delete loan
# @router.delete("/{id}", status_code=status.HTTP_200_OK)
# def delete_loan(
#     id: int,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     loan_query = db.query(models.EmployeeLoan).filter(models.EmployeeLoan.id == id)
#     loan = loan_query.first()

#     if not loan:
#         raise HTTPException(status_code=404, detail=f"Loan with ID {id} not found")

#     loan_query.delete(synchronize_session=False)
#     db.commit()

#     return {"message": "Loan deleted successfully"}





from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date, datetime

from app import oauth2
from app import schemas
from app import database
from app import models
from app.dependencies.permission import require
from app.models import EmployeeLoan, User, Employee, Department
from app.schemas import (
    EmployeeLoanCreate, EmployeeLoanUpdate, EmployeeLoanAdminUpdate,
    EmployeeLoanOut, EmployeeLoanDetailOut, EmployeeLoanCreateResponse,
    EmployeeLoanUpdateResponse, EmployeeLoanListResponse, LoanStatus,
    EmployeeLoanStats, LoanType
)
from app.database import get_db
from app.oauth2 import get_current_user
from app.schemas.employee_loan import EmployeeLoanAdminCreate, EmployeeLoanAdminPatch
from app.utils import filter_employee_loans, paginate_data

router = APIRouter(prefix="/employee-loans", tags=["Employee Loans"])

def verify_employee_user_match(db: Session, employee_id: int, user: User) -> Employee:
    """Verify that the employee belongs to the current user"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Check if user has an associated employee_id
    if not user.employee_id:
        raise HTTPException(status_code=400, detail="User is not linked to an employee")
    
    # Verify the employee belongs to this user
    if employee.id != user.employee_id:
        raise HTTPException(status_code=403, detail="Access denied: Employee does not belong to current user")
    
    # Additional email verification if both have emails
    if employee.email and user.email and employee.email.lower() != user.email.lower():
        raise HTTPException(status_code=400, detail="Employee email must match user email")
    
    return employee

def check_admin_permissions(user: User) -> bool:
    """Check if user has admin permissions"""
    return user.is_superuser or (hasattr(user, 'role') and user.role in ['admin', 'manager', 'hr', 'ceo'])

# ✅ Get all employee loan requests (admin or filtered per user)
@router.get("/my-loans", 
           response_model=EmployeeLoanListResponse, 
           dependencies=[require("read_employee_loan")])
def get_my_employee_loans(
    request: Request,
    status_filter: Optional[LoanStatus] = Query(None, description="Filter by loan status"),
    loan_type: Optional[LoanType] = Query(None, description="Filter by loan type"),
    date_from: Optional[date] = Query(None, description="Filter loans from this date"),
    date_to: Optional[date] = Query(None, description="Filter loans until this date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's own employee loan requests"""
    
    # Validate user has employee association
    if not current_user.employee_id:
        raise HTTPException(
            status_code=400, 
            detail="User account is not associated with an employee record"
        )
    
    try:
        # Base query - only user's own loans
        query = db.query(EmployeeLoan).options(
            joinedload(EmployeeLoan.employee),
            joinedload(EmployeeLoan.department),
            joinedload(EmployeeLoan.approved_by)
        ).filter(EmployeeLoan.employee_id == current_user.employee_id)
        
        # Apply filters
        if status_filter:
            query = query.filter(EmployeeLoan.status == status_filter)
            
        if loan_type:
            query = query.filter(EmployeeLoan.loan_type == loan_type)
            
        if date_from:
            query = query.filter(EmployeeLoan.created_at >= date_from)
            
        if date_to:
            query = query.filter(EmployeeLoan.created_at <= date_to)
        
        # Order by most recent first
        query = query.order_by(EmployeeLoan.created_at.desc())
        
        # Execute query
        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)
        
        # Serialize data
        serialized_data = [EmployeeLoanOut.model_validate(loan) for loan in paginated_data]
        
        response_data = {
            "count": count,
            "data": serialized_data,
            "user_info": {
                "employee_id": current_user.employee_id,
                "can_view_others": False
            }
        }
        
        return EmployeeLoanListResponse(result=response_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# =============================================================================
# API 2: MANAGEMENT/ADMIN API  
# For managers, HR, admin users to view employee loan requests with broader access
# =============================================================================

@router.get(
    "/employee-loans",
    response_model=EmployeeLoanListResponse,
    dependencies=[require("read_all_employee_loan")]
)
def get_employee_loan_requests_admin(
    request: Request,
    status_filter: Optional[LoanStatus] = Query(None, description="Filter by loan status"),
    employee_id: Optional[int] = Query(None, description="Filter by employee ID"),
    department_id: Optional[int] = Query(None, description="Filter by department ID"),
    loan_type: Optional[LoanType] = Query(None, description="Filter by loan type"),
    date_from: Optional[date] = Query(None, description="Filter loans from this date"),
    date_to: Optional[date] = Query(None, description="Filter loans until this date"),
    amount_min: Optional[float] = Query(None, description="Minimum loan amount"),
    amount_max: Optional[float] = Query(None, description="Maximum loan amount"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all employee loan requests with filters (admin access)"""
    try:
        query = db.query(EmployeeLoan).options(
            joinedload(EmployeeLoan.employee),
            joinedload(EmployeeLoan.department),
            joinedload(EmployeeLoan.request_user),
            joinedload(EmployeeLoan.approved_by)
        )

        # Apply filters
        if status_filter:
            query = query.filter(EmployeeLoan.status == status_filter)
        if employee_id:
            query = query.filter(EmployeeLoan.employee_id == employee_id)
        if department_id:
            query = query.filter(EmployeeLoan.department_id == department_id)
        if loan_type:
            query = query.filter(EmployeeLoan.loan_type == loan_type)
        if date_from:
            query = query.filter(EmployeeLoan.created_at >= date_from)
        if date_to:
            query = query.filter(EmployeeLoan.created_at <= date_to)
        if amount_min:
            query = query.filter(EmployeeLoan.loan_amount >= amount_min)
        if amount_max:
            query = query.filter(EmployeeLoan.loan_amount <= amount_max)

        # Additional custom filters
        query = filter_employee_loans(request.query_params, query)

        # Order by latest created
        query = query.order_by(EmployeeLoan.created_at.desc())

        # Fetch and paginate
        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        # Serialize and respond
        serialized_data = [EmployeeLoanOut.model_validate(loan) for loan in paginated_data]
        # access_info = get_current_user(current_user, db)
        access_info = {
            "id": current_user.id,
            "username": current_user.username,
            # add any other fields you want to expose
}

        return EmployeeLoanListResponse(result={
            "count": count,
            "data": serialized_data,
            "access_info": access_info
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# ✅ Get specific employee loan request by ID
@router.get("/{request_id}", response_model=EmployeeLoanDetailOut, dependencies=[require("read_all_employee_loan")])
def get_employee_loan_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific employee loan request with detailed permissions"""
    
    loan_request = db.query(EmployeeLoan).options(
        joinedload(EmployeeLoan.employee),
        joinedload(EmployeeLoan.department),
        joinedload(EmployeeLoan.request_user),
        joinedload(EmployeeLoan.approved_by)
    ).filter(EmployeeLoan.id == request_id).first()
    
    if not loan_request:
        raise HTTPException(status_code=404, detail="Employee loan request not found")
    
    # Permission check
    is_admin = check_admin_permissions(current_user)
    is_owner = loan_request.request_user_id == current_user.id
    
    if not is_admin and not is_owner:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Convert to detailed output with permissions
    result = EmployeeLoanDetailOut.model_validate(loan_request)
    result.can_edit = is_owner and loan_request.status == LoanStatus.PENDING
    result.can_approve = is_admin
    result.is_owner = is_owner
    
    return result

# ✅ Create a new employee loan request
@router.post("/", response_model=EmployeeLoanCreateResponse, status_code=status.HTTP_201_CREATED)
def create_employee_loan_request(
    request_data: EmployeeLoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new employee loan request with proper validation"""
    
    # Check if user has employee_id
    if not current_user.employee_id:
        raise HTTPException(status_code=400, detail="User is not linked to an employee")
    
    # Verify user has linked employee and it matches
    employee = verify_employee_user_match(db, current_user.employee_id, current_user)
    
    # Verify department exists
    department = db.query(Department).filter(Department.id == request_data.department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    # Additional business logic: Check if employee belongs to the department
    if hasattr(employee, 'department_id') and employee.department_id != request_data.department_id:
        raise HTTPException(status_code=400, detail="Employee does not belong to specified department")
    
    # Check for duplicate pending requests (business rule) - optional, you might allow multiple pending loans
    existing_pending = db.query(EmployeeLoan).filter(
        EmployeeLoan.employee_id == employee.id,
        EmployeeLoan.status == LoanStatus.PENDING
    ).first()
    
    if existing_pending:
        raise HTTPException(
            status_code=400, 
            detail="You already have a pending loan request. Please wait for approval or update the existing one."
        )
    
    try:
        # Create new request
        new_request = EmployeeLoan(
            employee_id=employee.id,
            department_id=request_data.department_id,
            request_user_id=current_user.id,
            amount=request_data.amount,
            loan_type=request_data.loan_type,
            description=request_data.description,
            issue_date=request_data.issue_date,
            due_date=request_data.due_date,
            status=LoanStatus.PENDING,
            created_by_user_id=current_user.id
        )
        
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        
        # Load relationships for response
        new_request = db.query(EmployeeLoan).options(
            joinedload(EmployeeLoan.employee),
            joinedload(EmployeeLoan.department),
            joinedload(EmployeeLoan.request_user)
        ).filter(EmployeeLoan.id == new_request.id).first()
        
        return EmployeeLoanCreateResponse(
            data=EmployeeLoanOut.model_validate(new_request)
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create employee loan request: {str(e)}")

# ✅ Update an existing employee loan request (employee)
@router.patch("/{request_id}", response_model=EmployeeLoanUpdateResponse)
def update_employee_loan_request(
    request_id: int,
    request_data: EmployeeLoanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an employee loan request (employee can only update their own pending requests)"""
    
    loan_request = db.query(EmployeeLoan).filter(EmployeeLoan.id == request_id).first()
    
    if not loan_request:
        raise HTTPException(status_code=404, detail="Employee loan request not found")
    
    # Permission check - only owner can update
    if loan_request.request_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied: You can only update your own loan requests")
    
    # Business rule - can only update pending requests
    if loan_request.status != LoanStatus.PENDING:
        raise HTTPException(status_code=400, detail="Cannot update non-pending loan requests")
    
    try:
        # Update fields
        update_data = request_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(loan_request, field, value)
        
        loan_request.updated_by_user_id = current_user.id
        
        db.commit()
        db.refresh(loan_request)
        
        return EmployeeLoanUpdateResponse(
            data=EmployeeLoanOut.model_validate(loan_request)
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update employee loan request: {str(e)}")

# ✅ Admin approval/rejection endpoint
@router.patch("/{request_id}/admin-approve", response_model=EmployeeLoanUpdateResponse, dependencies=[require("update_employee_loan")])
def admin_update_employee_loan_request(
    request_id: int,
    request_data: EmployeeLoanAdminUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Admin endpoint to approve/reject employee loan requests"""
    
    # Check admin permissions
    if not check_admin_permissions(current_user):
        raise HTTPException(status_code=403, detail="Admin permissions required")
    
    loan_request = db.query(EmployeeLoan).filter(EmployeeLoan.id == request_id).first()
    
    if not loan_request:
        raise HTTPException(status_code=404, detail="Employee loan request not found")
    
    # Only allow admin actions on PENDING requests
    if loan_request.status != LoanStatus.PENDING:
        raise HTTPException(status_code=400, detail="Can only approve/reject pending loan requests")
    
    try:
        # Update fields
        update_data = request_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(loan_request, field, value)
        
        # Set approval user for both APPROVED and REJECTED status
        if request_data.status in [LoanStatus.APPROVED, LoanStatus.REJECTED]:
            loan_request.approved_by_user_id = current_user.id
        
        # Always set updated_by_user_id to current user
        loan_request.updated_by_user_id = current_user.id
        
        db.commit()
        db.refresh(loan_request)
        
        return EmployeeLoanUpdateResponse(
            message=f"Employee loan request {request_data.status.value if request_data.status else 'updated'} successfully",
            data=EmployeeLoanOut.model_validate(loan_request)
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update employee loan request: {str(e)}")

# ✅ Delete an employee loan request
@router.delete("/{request_id}", status_code=status.HTTP_200_OK, dependencies=[require("delete_employee_loan")])
def delete_employee_loan_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an employee loan request (users can delete their own; superusers can delete any pending request)"""
    
    loan_request = db.query(EmployeeLoan).filter(EmployeeLoan.id == request_id).first()
    
    if not loan_request:
        raise HTTPException(status_code=404, detail="Employee loan request not found")

    # Business rule: only allow deleting PENDING requests
    if loan_request.status != LoanStatus.PENDING:
        raise HTTPException(status_code=400, detail="Cannot delete non-pending loan requests")

    # Only the owner or a superuser can delete
    if loan_request.request_user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Access denied: You can only delete your own loan requests unless you're a superuser")
    
    try:
        db.delete(loan_request)
        db.commit()
        return {"message": "Employee loan request deleted successfully"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete employee loan request: {str(e)}")

# ✅ Get employee loan statistics
@router.get("/stats/summary", response_model=EmployeeLoanStats, dependencies=[require("read_employee_loan")])
def get_employee_loan_stats(
    employee_id: Optional[int] = Query(None, description="Filter stats by employee ID"),
    department_id: Optional[int] = Query(None, description="Filter stats by department ID"),
    loan_type: Optional[LoanType] = Query(None, description="Filter stats by loan type"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get employee loan request statistics"""
    
    query = db.query(EmployeeLoan)
    
    # Apply user-based filtering for non-admins
    if not current_user.is_superuser:
        if current_user.employee_id:
            query = query.filter(EmployeeLoan.employee_id == current_user.employee_id)
        else:
            # No stats for users without employee_id
            return EmployeeLoanStats(
                total_loans=0,
                pending_loans=0,
                approved_loans=0,
                rejected_loans=0,
                total_amount_requested=0.0,
                total_amount_approved=0.0,
                average_loan_amount=0.0
            )
    
    if employee_id:
        # Only allow if admin or own employee_id
        if not current_user.is_superuser and employee_id != current_user.employee_id:
            raise HTTPException(status_code=403, detail="Access denied")
        query = query.filter(EmployeeLoan.employee_id == employee_id)
        
    if department_id:
        query = query.filter(EmployeeLoan.department_id == department_id)
        
    if loan_type:
        query = query.filter(EmployeeLoan.loan_type == loan_type)
    
    all_requests = query.all()
    
    total_amount = sum(r.amount for r in all_requests)
    approved_amount = sum(r.amount for r in all_requests if r.status == LoanStatus.APPROVED)
    
    stats = {
        "total_loans": len(all_requests),
        "pending_loans": len([r for r in all_requests if r.status == LoanStatus.PENDING]),
        "approved_loans": len([r for r in all_requests if r.status == LoanStatus.APPROVED]),
        "rejected_loans": len([r for r in all_requests if r.status == LoanStatus.REJECTED]),
        "total_amount_requested": total_amount,
        "total_amount_approved": approved_amount,
        "average_loan_amount": total_amount / len(all_requests) if all_requests else 0.0
    }
    
    return EmployeeLoanStats(**stats)

# ✅ Admin edit employee loan request
@router.patch("/{request_id}/admin-edit", response_model=EmployeeLoanUpdateResponse, dependencies=[require("approved_employee_loan")])
def admin_edit_employee_loan_request(
    request_id: int,
    request_data: EmployeeLoanAdminPatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Admin can edit any field (employee, amount, loan_type, description, dates, department) of a pending loan request."""

    # Check admin permissions
    if not check_admin_permissions(current_user):
        raise HTTPException(status_code=403, detail="Admin permissions required")

    loan_request = db.query(EmployeeLoan).filter(EmployeeLoan.id == request_id).first()

    if not loan_request:
        raise HTTPException(status_code=404, detail="Employee loan request not found")

    # Only allow updates on PENDING requests
    if loan_request.status != LoanStatus.PENDING:
        raise HTTPException(status_code=400, detail="Only pending loan requests can be edited")

    # If updating employee_id, verify employee exists
    if request_data.employee_id:
        employee = db.query(Employee).filter(Employee.id == request_data.employee_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        loan_request.employee_id = request_data.employee_id

    # If updating department_id, verify department exists
    if request_data.department_id:
        department = db.query(Department).filter(Department.id == request_data.department_id).first()
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")
        loan_request.department_id = request_data.department_id

    # Apply other updatable fields
    update_data = request_data.model_dump(exclude_unset=True, exclude={"employee_id", "department_id"})
    for field, value in update_data.items():
        setattr(loan_request, field, value)

    loan_request.updated_by_user_id = current_user.id

    try:
        db.commit()
        db.refresh(loan_request)

        return EmployeeLoanUpdateResponse(
            message="Employee loan request updated successfully",
            data=EmployeeLoanOut.model_validate(loan_request)
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update loan request: {str(e)}")

# ✅ Admin create employee loan request
@router.post("/admin-create", response_model=EmployeeLoanCreateResponse, dependencies=[require("create_employee_loan")])
def create_employee_loan_request_as_admin(
    request_data: EmployeeLoanAdminCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Admin creates employee loan request on behalf of employee"""

    # Check admin permissions
    if not check_admin_permissions(current_user):
        raise HTTPException(status_code=403, detail="Admin permissions required")
   
    # Verify the employee exists
    employee = db.query(Employee).filter(Employee.id == request_data.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Verify the department exists
    department = db.query(Department).filter(Department.id == request_data.department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    # Optional: Ensure the employee is part of the department
    if hasattr(employee, 'department_id') and employee.department_id != request_data.department_id:
        raise HTTPException(status_code=400, detail="Employee does not belong to specified department")

    # Prevent duplicate pending requests for same employee (optional business rule)
    existing_pending = db.query(EmployeeLoan).filter(
        EmployeeLoan.employee_id == request_data.employee_id,
        EmployeeLoan.status == LoanStatus.PENDING
    ).first()
    if existing_pending:
        raise HTTPException(status_code=400, detail="Employee already has a pending loan request")

    try:
        new_request = EmployeeLoan(
            employee_id=request_data.employee_id,
            department_id=request_data.department_id,
            amount=request_data.amount,
            loan_type=request_data.loan_type,
            description=request_data.description,
            issue_date=request_data.issue_date,
            due_date=request_data.due_date,
            status=LoanStatus.PENDING,
            request_user_id=current_user.id,  # The admin submitting
            created_by_user_id=current_user.id
        )

        db.add(new_request)
        db.commit()
        db.refresh(new_request)

        # Load relationships for response
        new_request = db.query(EmployeeLoan).options(
            joinedload(EmployeeLoan.employee),
            joinedload(EmployeeLoan.department),
            joinedload(EmployeeLoan.request_user)
        ).filter(EmployeeLoan.id == new_request.id).first()

        return EmployeeLoanCreateResponse(
            data=EmployeeLoanOut.model_validate(new_request)
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create loan request: {str(e)}")