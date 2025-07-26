from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from .. import database, schemas, models, oauth2
from app.utils import paginate_data, filter_audit_logs


router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)


@router.get("/", response_model=schemas.AuditLogListResponse)
def get_audit_logs(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.AuditLog)
        query = filter_audit_logs(request.query_params, query)

        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        serialized_data = [schemas.AuditLogOut.from_orm(a) for a in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized_data
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AuditLogOut)
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


@router.get("/{id}", response_model=schemas.AuditLogOut)
def get_audit_log_by_id(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    log = db.query(models.AuditLog).filter(models.AuditLog.id == id).first()

    if not log:
        raise HTTPException(status_code=404, detail=f"AuditLog with id {id} not found")

    return log


@router.patch("/{id}", response_model=schemas.AuditLogOut)
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



@router.delete("/{id}", status_code=status.HTTP_200_OK)
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