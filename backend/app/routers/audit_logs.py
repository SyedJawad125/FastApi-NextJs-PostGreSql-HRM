import datetime
from fastapi import APIRouter, Depends, Query, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any, Optional

from app.models.audit_logs import AuditLog
from .. import database, schemas, models, oauth2
from app.utils import paginate_data, filter_audit_logs
from app.dependencies.permission import require
from datetime import datetime
from typing import Optional

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)


# @router.get("/", response_model=schemas.AuditLogListResponse, dependencies=[require("read_auditlog")])
# def get_audit_logs(
#     request: Request,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     try:
#         query = db.query(models.AuditLog)
#         query = filter_audit_logs(request.query_params, query)

#         all_data = query.all()
#         paginated_data, count = paginate_data(all_data, request)

#         serialized_data = [schemas.AuditLogOut.from_orm(a) for a in paginated_data]

#         return {
#             "status": "SUCCESSFUL",
#             "result": {
#                 "count": count,
#                 "data": serialized_data
#             }
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.get("/", response_model=schemas.AuditLogListResponse, dependencies=[require("read_auditlog")])
# def get_audit_logs(
#     request: Request,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user),
#     page: int = Query(1, gt=0),
#     limit: int = Query(10, gt=0)
# ):
#     try:
#         query = db.query(models.AuditLog)
#         query = filter_audit_logs(request.query_params, query)

#         # Calculate offset for pagination
#         offset = (page - 1) * limit
        
#         # Get paginated results directly from database
#         paginated_data = query.offset(offset).limit(limit).all()
        
#         # Get total count (without applying limit/offset)
#         total_count = query.count()

#         serialized_data = [schemas.AuditLogOut.from_orm(a) for a in paginated_data]

#         return {
#             "status": "SUCCESSFUL",
#             "result": {
#                 "count": total_count,
#                 "data": serialized_data
#             }
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.get("/", response_model=schemas.AuditLogListResponse, dependencies=[require("read_auditlog")])
# def get_audit_logs(
#     request: Request,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user),
#     page: int = Query(1, gt=0),
#     limit: int = Query(10, gt=0)
# ):
#     try:
#         query = db.query(models.AuditLog).order_by(models.AuditLog.timestamp.desc())
#         query = filter_audit_logs(request.query_params, query)

#         # Get total count (without applying limit/offset)
#         total_count = query.count()
        
#         # Calculate total pages
#         total_pages = (total_count + limit - 1) // limit  # Ceiling division
        
#         # Calculate offset for pagination
#         offset = (page - 1) * limit
        
#         # Get paginated results
#         paginated_data = query.offset(offset).limit(limit).all()
        
#         serialized_data = [schemas.AuditLogOut.from_orm(a) for a in paginated_data]

#         return {
#             "status": "SUCCESSFUL",
#             "result": {
#                 "count": total_count,
#                 "total_pages": total_pages,
#                 "current_page": page,
#                 "limit": limit,
#                 "next": page < total_pages,
#                 "previous": page > 1,
#                 "data": serialized_data
#             }
#         }

#     except Exception as e:
#         database.logger.error(f"Error fetching audit logs: {str(e)}")
#         raise HTTPException(
#             status_code=500,
#             detail={
#                 "status": "ERROR",
#                 "message": "Failed to fetch audit logs",
#                 "error": str(e)
#             }
#         )









@router.get("/", response_model=schemas.AuditLogListResponse, dependencies=[require("read_auditlog")])
def get_audit_logs(
    db: Session = Depends(database.get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    performed_by_user_id: Optional[int] = None,
    action: Optional[str] = None,
    table_name: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    try:
        query = db.query(AuditLog)

        # Apply filters
        if performed_by_user_id:
            query = query.filter(AuditLog.performed_by_user_id == performed_by_user_id)
        if action:
            query = query.filter(AuditLog.action.ilike(f"%{action}%"))
        if table_name:
            query = query.filter(AuditLog.table_name.ilike(f"%{table_name}%"))
        if start_date:
            query = query.filter(AuditLog.created_at >= start_date)
        if end_date:
            query = query.filter(AuditLog.created_at <= end_date)

        # Get total count
        total = query.count()
        total_pages = (total + limit - 1) // limit
        offset = (page - 1) * limit

        # Get paginated results
        logs = (
            query
            .order_by(AuditLog.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        # Convert logs to schema
        log_out_list = [schemas.AuditLogOut.from_orm(log) for log in logs]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": total,
                "data": log_out_list
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AuditLogOut, dependencies=[require("create_auditlog")])
def create_audit_log(
    log: schemas.AuditLogCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        log_data = log.dict()
        log_data["created_by_user_id"] = current_user.id
        log_data["updated_by_user_id"] = None

        new_log = models.AuditLog(**log_data)
        db.add(new_log)
        db.commit()
        db.refresh(new_log)

        return new_log

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=schemas.AuditLogOut, dependencies=[require("read_auditlog")])
def get_audit_log_by_id(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    log = db.query(models.AuditLog).filter(models.AuditLog.id == id).first()

    if not log:
        raise HTTPException(status_code=404, detail=f"AuditLog with id {id} not found")

    return log


@router.patch("/{id}", response_model=schemas.AuditLogOut, dependencies=[require("update_auditlog")])
def update_audit_log(
    id: int,
    updated_data: schemas.AuditLogUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        log_instance = db.query(models.AuditLog).filter(models.AuditLog.id == id).first()

        if not log_instance:
            raise HTTPException(status_code=404, detail=f"AuditLog with id {id} not found")

        update_dict = updated_data.dict(exclude_unset=True)
        update_dict["updated_by_user_id"] = current_user.id

        for key, value in update_dict.items():
            setattr(log_instance, key, value)

        db.commit()
        db.refresh(log_instance)

        return log_instance

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.delete("/{id}", status_code=status.HTTP_200_OK, dependencies=[require("delete_auditlog")])
def delete_audit_log(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    audit_log_query = db.query(models.AuditLog).filter(models.AuditLog.id == id)
    audit_log = audit_log_query.first()

    if not audit_log:
        raise HTTPException(status_code=404, detail=f"AuditLog with id {id} not found")

    audit_log_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "AuditLog deleted successfully"}