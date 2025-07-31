from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from .. import database, schemas, models, oauth2
from app.utils import filter_grievances, paginate_data  # Optional: add your own filtering if needed

router = APIRouter(
    prefix="/grievances",
    tags=["Grievances"]
)

# ✅ Get all grievances (with optional pagination)
@router.get("/", response_model=schemas.GrievanceListResponse)
def get_grievances(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        # Apply base query
        query = db.query(models.Grievance)

        # Apply filters
        query = filter_grievances(request.query_params, query)

        # Fetch filtered results
        all_data = query.all()

        # Paginate results
        paginated_data, count = paginate_data(all_data, request)

        # Serialize response
        serialized_data = [schemas.GrievanceOut.from_orm(grievance) for grievance in paginated_data]

        # Final response
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

# ✅ Create a new grievance
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.GrievanceOut)
def create_grievance(
    grievance: schemas.GrievanceCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        grievance_data = grievance.dict(exclude_unset=True)
        grievance_data["created_by"] = current_user.id
        grievance_data["updated_by"] = None

        new_grievance = models.Grievance(**grievance_data)
        db.add(new_grievance)
        db.commit()
        db.refresh(new_grievance)

        return new_grievance

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Get a single grievance by ID
@router.get("/{id}", response_model=schemas.GrievanceOut)
def get_grievance(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    grievance = db.query(models.Grievance).filter(models.Grievance.id == id).first()

    if not grievance:
        raise HTTPException(status_code=404, detail=f"Grievance with id {id} not found")

    return grievance


# ✅ Update grievance
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

@router.patch("/{id}", response_model=schemas.GrievanceOut)
def update_grievance(
    id: int,
    updated_data: schemas.GrievanceUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        # Get the grievance instance
        grievance_instance = db.query(models.Grievance).filter(models.Grievance.id == id).first()
        if not grievance_instance:
            raise HTTPException(status_code=404, detail=f"Grievance with id {id} not found")

        # Convert update data to dict
        update_dict = updated_data.dict(exclude_unset=True)
        
        # Handle status changes
        if 'status' in update_dict:
            new_status = update_dict['status']
            current_status = grievance_instance.status
            
            # If changing to resolved and wasn't resolved before
            if new_status == "resolved" and current_status != "resolved":
                update_dict['resolved_at'] = datetime.utcnow()
            # If changing from resolved to another status
            elif current_status == "resolved" and new_status != "resolved":
                update_dict['resolved_at'] = None
        
        # Handle explicit resolved_at updates
        if 'resolved_at' in update_dict:
            # If setting to null but status is resolved, prevent it
            if update_dict['resolved_at'] is None and grievance_instance.status == "resolved":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot clear resolved_at when status is resolved"
                )
            # If setting a date but status isn't resolved, update status
            elif update_dict['resolved_at'] is not None and grievance_instance.status != "resolved":
                update_dict['status'] = "resolved"
        
        # Update the record
        update_dict["updated_by"] = current_user.id
        for key, value in update_dict.items():
            setattr(grievance_instance, key, value)

        db.commit()
        db.refresh(grievance_instance)

        return grievance_instance

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Delete grievance
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_grievance(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    grievance_query = db.query(models.Grievance).filter(models.Grievance.id == id)
    grievance = grievance_query.first()

    if not grievance:
        raise HTTPException(status_code=404, detail=f"Grievance with id {id} not found")

    grievance_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Grievance deleted successfully"}
