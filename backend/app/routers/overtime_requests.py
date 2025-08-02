# from fastapi import APIRouter, Depends, HTTPException, Request, status
# from sqlalchemy.orm import Session
# from typing import List

# from app import oauth2
# from app import schemas
# from app import database
# from app import models
# from app.models import OvertimeRequest, User
# from app.schemas import OvertimeRequestCreate, OvertimeRequestUpdate, OvertimeRequestOut
# from app.database import get_db
# from app.dependencies import get_current_user
# from app.utils import filter_overtime_requests, paginate_data

# router = APIRouter(prefix="/overtime", tags=["Overtime Requests"])

# # ✅ Get all overtime requests (admin or filtered per user)
# @router.get("/", response_model=schemas.OvertimeRequestListResponse)
# def get_overtime_requests(
#     request: Request,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     try:
#         query = db.query(models.OvertimeRequest)
#         query = filter_overtime_requests(request.query_params, query)

#         all_data = query.all()
#         paginated_data, count = paginate_data(all_data, request)

#         serialized_data = [schemas.OvertimeRequestOut.from_orm(overtime) for overtime in paginated_data]

#         response_data = {
#             "count": count,
#             "data": serialized_data
#         }

#         return {
#             "status": "SUCCESSFUL",
#             "result": response_data
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # ✅ Create a new overtime request
# @router.post("/", response_model=OvertimeRequestOut)
# def create_overtime_request(
#     request_data: OvertimeRequestCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     # Ensure user has linked employee
#     if not current_user.employee_id:
#         raise HTTPException(status_code=400, detail="User is not linked to an employee")

#     # Ensure employee_id in request matches user's employee
#     if request_data.employee_id != current_user.employee_id:
#         raise HTTPException(status_code=400, detail="Employee ID must match current user")

#     new_request = OvertimeRequest(
#         **request_data.dict(),
#         request_user_id=current_user.id,
#         created_by_user_id=current_user.id
#     )
#     db.add(new_request)
#     db.commit()
#     db.refresh(new_request)
#     return new_request

# # ✅ Update an existing overtime request
# @router.patch("/{request_id}", response_model=OvertimeRequestOut)
# def update_overtime_request(
#     request_id: int,
#     request_data: OvertimeRequestUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     request = db.query(OvertimeRequest).filter(OvertimeRequest.id == request_id).first()

#     if not request:
#         raise HTTPException(status_code=404, detail="Overtime request not found")

#     if request.request_user_id != current_user.id:
#         raise HTTPException(status_code=403, detail="Not allowed to update this request")

#     if request_data.employee_id and request_data.employee_id != current_user.employee_id:
#         raise HTTPException(status_code=400, detail="Employee ID must match current user")

#     for key, value in request_data.dict(exclude_unset=True).items():
#         setattr(request, key, value)

#     request.updated_by_user_id = current_user.id
#     db.commit()
#     db.refresh(request)
#     return request

# # ✅ Delete an overtime request
# @router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_overtime_request(
#     request_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     request = db.query(OvertimeRequest).filter(OvertimeRequest.id == request_id).first()

#     if not request:
#         raise HTTPException(status_code=404, detail="Request not found")

#     if request.request_user_id != current_user.id:
#         raise HTTPException(status_code=403, detail="Not allowed to delete this request")

#     db.delete(request)
#     db.commit()
#     return None







from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from app import oauth2
from app import schemas
from app import database
from app import models
from app.dependencies.permission import require
from app.models import OvertimeRequest, User, Employee, Department
from app.schemas import (
    OvertimeRequestCreate, OvertimeRequestUpdate, OvertimeRequestAdminUpdate,
    OvertimeRequestOut, OvertimeRequestDetailOut, OvertimeRequestCreateResponse,
    OvertimeRequestUpdateResponse, OvertimeRequestListResponse, OvertimeStatus,
    OvertimeRequestStats
)
from app.database import get_db
from app.oauth2 import get_current_user
from app.utils import filter_overtime_requests, paginate_data

router = APIRouter(prefix="/overtime", tags=["Overtime Requests"])

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
    return hasattr(user, 'role') and user.role in ['admin', 'manager', 'hr']

# ✅ Get all overtime requests (admin or filtered per user)
@router.get("/", response_model=OvertimeRequestListResponse)
def get_overtime_requests(
    request: Request,
    status_filter: Optional[OvertimeStatus] = Query(None, description="Filter by status"),
    employee_id: Optional[int] = Query(None, description="Filter by employee ID"),
    department_id: Optional[int] = Query(None, description="Filter by department ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get overtime requests with proper filtering based on user permissions
    """
    try:
        # Base query with eager loading for better performance
        query = db.query(OvertimeRequest).options(
            joinedload(OvertimeRequest.employee),
            joinedload(OvertimeRequest.department),
            joinedload(OvertimeRequest.request_user),
            joinedload(OvertimeRequest.approved_by)
        )
        
        # Apply user-based filtering (non-admins can only see their own requests)
        if not check_admin_permissions(current_user):
            if not current_user.employee_id:
                raise HTTPException(status_code=400, detail="User is not linked to an employee")
            query = query.filter(OvertimeRequest.employee_id == current_user.employee_id)
        
        # Apply filters
        if status_filter:
            query = query.filter(OvertimeRequest.status == status_filter)
        if employee_id:
            if not check_admin_permissions(current_user) and employee_id != current_user.employee_id:
                raise HTTPException(status_code=403, detail="Access denied")
            query = query.filter(OvertimeRequest.employee_id == employee_id)
        if department_id:
            query = query.filter(OvertimeRequest.department_id == department_id)
        
        # Apply additional filters from query params
        query = filter_overtime_requests(request.query_params, query)
        
        # Order by creation date (newest first)
        query = query.order_by(OvertimeRequest.created_at.desc())
        
        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)
        
        serialized_data = [OvertimeRequestOut.from_orm(overtime) for overtime in paginated_data]
        
        response_data = {
            "count": count,
            "data": serialized_data
        }
        
        return OvertimeRequestListResponse(result=response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# ✅ Get specific overtime request by ID
@router.get("/{request_id}", response_model=OvertimeRequestDetailOut)
def get_overtime_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific overtime request with detailed permissions"""
    
    overtime_request = db.query(OvertimeRequest).options(
        joinedload(OvertimeRequest.employee),
        joinedload(OvertimeRequest.department),
        joinedload(OvertimeRequest.request_user),
        joinedload(OvertimeRequest.approved_by)
    ).filter(OvertimeRequest.id == request_id).first()
    
    if not overtime_request:
        raise HTTPException(status_code=404, detail="Overtime request not found")
    
    # Permission check
    is_admin = check_admin_permissions(current_user)
    is_owner = overtime_request.request_user_id == current_user.id
    
    if not is_admin and not is_owner:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Convert to detailed output with permissions
    result = OvertimeRequestDetailOut.from_orm(overtime_request)
    result.can_edit = is_owner and overtime_request.status == OvertimeStatus.PENDING
    result.can_approve = is_admin
    result.is_owner = is_owner
    
    return result

# ✅ Create a new overtime request
@router.post("/", response_model=OvertimeRequestCreateResponse, status_code=status.HTTP_201_CREATED)
def create_overtime_request(
    request_data: OvertimeRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new overtime request with proper validation"""
    
    # Verify user has linked employee and it matches
    employee = verify_employee_user_match(db, current_user.employee_id, current_user)
    
    # Verify department exists and employee belongs to it
    department = db.query(Department).filter(Department.id == request_data.department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    # Additional business logic: Check if employee belongs to the department
    if hasattr(employee, 'department_id') and employee.department_id != request_data.department_id:
        raise HTTPException(status_code=400, detail="Employee does not belong to specified department")
    
    # Check for duplicate pending requests (business rule)
    existing_pending = db.query(OvertimeRequest).filter(
        OvertimeRequest.employee_id == employee.id,
        OvertimeRequest.status == OvertimeStatus.PENDING
    ).first()
    
    if existing_pending:
        raise HTTPException(
            status_code=400, 
            detail="You already have a pending overtime request. Please wait for approval or update the existing one."
        )
    
    try:
        # Create new request
        new_request = OvertimeRequest(
            employee_id=employee.id,
            department_id=request_data.department_id,
            request_user_id=current_user.id,
            reason=request_data.reason,
            hours_requested=request_data.hours_requested,
            status=OvertimeStatus.PENDING,
            created_by_user_id=current_user.id
        )
        
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        
        # Load relationships for response
        db.refresh(new_request)
        new_request = db.query(OvertimeRequest).options(
            joinedload(OvertimeRequest.employee),
            joinedload(OvertimeRequest.department),
            joinedload(OvertimeRequest.request_user)
        ).filter(OvertimeRequest.id == new_request.id).first()
        
        return OvertimeRequestCreateResponse(
            data=OvertimeRequestOut.from_orm(new_request)
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create overtime request: {str(e)}")

# ✅ Update an existing overtime request (employee)
@router.patch("/{request_id}", response_model=OvertimeRequestUpdateResponse)
def update_overtime_request(
    request_id: int,
    request_data: OvertimeRequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an overtime request (employee can only update their own pending requests)"""
    
    overtime_request = db.query(OvertimeRequest).filter(OvertimeRequest.id == request_id).first()
    
    if not overtime_request:
        raise HTTPException(status_code=404, detail="Overtime request not found")
    
    # Permission check - only owner can update
    if overtime_request.request_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied: You can only update your own requests")
    
    # Business rule - can only update pending requests
    if overtime_request.status != OvertimeStatus.PENDING:
        raise HTTPException(status_code=400, detail="Cannot update non-pending requests")
    
    try:
        # Update fields
        update_data = request_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(overtime_request, field, value)
        
        overtime_request.updated_by_user_id = current_user.id
        
        db.commit()
        db.refresh(overtime_request)
        
        return OvertimeRequestUpdateResponse(
            data=OvertimeRequestOut.from_orm(overtime_request)
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update overtime request: {str(e)}")

# ✅ Admin update endpoint (approve/reject requests)
# @router.patch("/{request_id}/admin", response_model=OvertimeRequestUpdateResponse, dependencies=[require("update_employee_overtime")])
# def admin_update_overtime_request(
#     request_id: int,
#     request_data: OvertimeRequestAdminUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     """Admin endpoint to approve/reject overtime requests"""
    
#     overtime_request = db.query(OvertimeRequest).filter(OvertimeRequest.id == request_id).first()
    
#     if not overtime_request:
#         raise HTTPException(status_code=404, detail="Overtime request not found")
    
#     try:
#         # Update fields
#         update_data = request_data.dict(exclude_unset=True)
#         for field, value in update_data.items():
#             setattr(overtime_request, field, value)
        
#         # Set approval user if status is being changed to approved
#         if request_data.status == OvertimeStatus.APPROVED:
#             overtime_request.approved_by_user_id = current_user.id
        
#         overtime_request.updated_by_user_id = current_user.id
        
#         db.commit()
#         db.refresh(overtime_request)
        
#         return OvertimeRequestUpdateResponse(
#             message=f"Overtime request {request_data.status.value if request_data.status else 'updated'} successfully",
#             data=OvertimeRequestOut.from_orm(overtime_request)
#         )
        
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=f"Failed to update overtime request: {str(e)}")

@router.patch("/{request_id}/admin", response_model=OvertimeRequestUpdateResponse, dependencies=[require("update_employee_overtime")])
def admin_update_overtime_request(
    request_id: int,
    request_data: OvertimeRequestAdminUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Admin endpoint to approve/reject overtime requests"""
    
    overtime_request = db.query(OvertimeRequest).filter(OvertimeRequest.id == request_id).first()
    
    if not overtime_request:
        raise HTTPException(status_code=404, detail="Overtime request not found")
    
    try:
        # Update fields
        update_data = request_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(overtime_request, field, value)
        
        # Set approval user for both APPROVED and REJECTED status
        # This tracks who made the decision (approved or rejected)
        if request_data.status in [OvertimeStatus.APPROVED, OvertimeStatus.REJECTED]:
            overtime_request.approved_by_user_id = current_user.id
        
        # Always set updated_by_user_id to current user
        overtime_request.updated_by_user_id = current_user.id
        
        db.commit()
        db.refresh(overtime_request)
        
        return OvertimeRequestUpdateResponse(
            message=f"Overtime request {request_data.status.value if request_data.status else 'updated'} successfully",
            data=OvertimeRequestOut.from_orm(overtime_request)
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update overtime request: {str(e)}")
# ✅ Delete an overtime request
@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_overtime_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an overtime request (only pending requests by owner)"""
    
    overtime_request = db.query(OvertimeRequest).filter(OvertimeRequest.id == request_id).first()
    
    if not overtime_request:
        raise HTTPException(status_code=404, detail="Overtime request not found")
    
    # Permission check
    if overtime_request.request_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied: You can only delete your own requests")
    
    # Business rule - can only delete pending requests
    if overtime_request.status != OvertimeStatus.PENDING:
        raise HTTPException(status_code=400, detail="Cannot delete non-pending requests")
    
    try:
        db.delete(overtime_request)
        db.commit()
        return None
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete overtime request: {str(e)}")

# ✅ Get overtime statistics (admin only)
@router.get("/stats/summary", response_model=OvertimeRequestStats)
def get_overtime_stats(
    employee_id: Optional[int] = Query(None, description="Filter stats by employee ID"),
    department_id: Optional[int] = Query(None, description="Filter stats by department ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get overtime request statistics"""
    
    if not check_admin_permissions(current_user):
        raise HTTPException(status_code=403, detail="Admin permissions required")
    
    query = db.query(OvertimeRequest)
    
    if employee_id:
        query = query.filter(OvertimeRequest.employee_id == employee_id)
    if department_id:
        query = query.filter(OvertimeRequest.department_id == department_id)
    
    all_requests = query.all()
    
    stats = {
        "total_requests": len(all_requests),
        "pending_requests": len([r for r in all_requests if r.status == OvertimeStatus.PENDING]),
        "approved_requests": len([r for r in all_requests if r.status == OvertimeStatus.APPROVED]),
        "rejected_requests": len([r for r in all_requests if r.status == OvertimeStatus.REJECTED]),
        "total_hours_requested": sum(r.hours_requested for r in all_requests),
        "total_hours_approved": sum(r.hours_requested for r in all_requests if r.status == OvertimeStatus.APPROVED)
    }
    
    return OvertimeRequestStats(**stats)