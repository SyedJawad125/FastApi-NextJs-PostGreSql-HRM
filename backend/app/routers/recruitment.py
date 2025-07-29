# from fastapi import APIRouter, Depends, status, Request, HTTPException
# from sqlalchemy.orm import Session
# from typing import Any

# from .. import database, schemas, models, oauth2
# from app.utils import paginate_data, filter_recruitments
# from fastapi.responses import JSONResponse

# router = APIRouter(
#     prefix="/recruitments",
#     tags=["Recruitments"]
# )


# @router.get("/", response_model=schemas.RecruitmentListResponse)
# def get_recruitments(
#     request: Request,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     try:
#         query = db.query(models.Recruitment)
#         query = filter_recruitments(request.query_params, query)

#         all_data = query.all()
#         paginated_data, count = paginate_data(all_data, request)

#         serialized_data = [schemas.RecruitmentOut.from_orm(r) for r in paginated_data]

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


# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.RecruitmentOut)
# def create_recruitment(
#     payload: schemas.RecruitmentCreate,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ) -> Any:
#     try:
#         recruitment_data = payload.dict()
#         recruitment_data["created_by_user_id"] = current_user.id
#         recruitment_data["updated_by_user_id"] = None

#         new_recruitment = models.Recruitment(**recruitment_data)
#         db.add(new_recruitment)
#         db.commit()
#         db.refresh(new_recruitment)

#         return new_recruitment

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.get("/{id}", response_model=schemas.RecruitmentOut)
# def get_recruitment(
#     id: int,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     recruitment = db.query(models.Recruitment).filter(models.Recruitment.id == id).first()

#     if not recruitment:
#         raise HTTPException(status_code=404, detail=f"Recruitment with id {id} not found")

#     return recruitment


# @router.patch("/{id}", response_model=schemas.RecruitmentOut)
# def update_recruitment(
#     id: int,
#     updated_data: schemas.RecruitmentUpdate,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     try:
#         recruitment_instance = db.query(models.Recruitment).filter(models.Recruitment.id == id).first()

#         if not recruitment_instance:
#             raise HTTPException(status_code=404, detail=f"Recruitment with id {id} not found")

#         update_dict = updated_data.dict(exclude_unset=True)
#         update_dict["updated_by_user_id"] = current_user.id

#         for key, value in update_dict.items():
#             setattr(recruitment_instance, key, value)

#         db.commit()
#         db.refresh(recruitment_instance)

#         return recruitment_instance

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.delete("/{id}", status_code=status.HTTP_200_OK)
# def delete_recruitment(
#     id: int,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     recruitment_query = db.query(models.Recruitment).filter(models.Recruitment.id == id)
#     recruitment = recruitment_query.first()

#     if not recruitment:
#         raise HTTPException(status_code=404, detail=f"Recruitment with id {id} not found")

#     recruitment_query.delete(synchronize_session=False)
#     db.commit()

#     return {"message": "Recruitment deleted successfully"}



# import traceback  # Add at the top
# from fastapi import APIRouter, Depends, status, Request, HTTPException
# from sqlalchemy.orm import Session
# from typing import Any

# from .. import database, schemas, models, oauth2
# from app.utils import paginate_data, filter_recruitments
# from fastapi.responses import JSONResponse

# router = APIRouter(
#     prefix="/recruitments",
#     tags=["Recruitments"]
# )


# @router.get("/", response_model=schemas.RecruitmentListResponse)
# def get_recruitments(
#     request: Request,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     try:
#         query = db.query(models.Recruitment)
#         query = filter_recruitments(request.query_params, query)

#         all_data = query.all()
#         paginated_data, count = paginate_data(all_data, request)

#         serialized_data = [schemas.RecruitmentOut.from_orm(r) for r in paginated_data]

#         return {
#             "status": "SUCCESSFUL",
#             "result": {
#                 "count": count,
#                 "data": serialized_data
#             }
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.RecruitmentOut)
# def create_recruitment(
#     payload: schemas.RecruitmentCreate,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ) -> Any:
#     try:
#         recruitment_data = payload.dict()
#         recruitment_data["created_by_user_id"] = current_user.id
#         recruitment_data["updated_by_user_id"] = None
#         recruitment_data["created_by_employee_id"] = getattr(current_user, "employee_id", None)
#         recruitment_data["hiring_manager_id"] = None  # Optional logic

#         new_recruitment = models.Recruitment(**recruitment_data)
#         db.add(new_recruitment)
#         db.commit()
#         db.refresh(new_recruitment)

#         return new_recruitment

#     except Exception as e:
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail="Recruitment creation failed.")


# @router.get("/{id}", response_model=schemas.RecruitmentOut)
# def get_recruitment(
#     id: int,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     recruitment = db.query(models.Recruitment).filter(models.Recruitment.id == id).first()

#     if not recruitment:
#         raise HTTPException(status_code=404, detail=f"Recruitment with id {id} not found")

#     return recruitment


# @router.patch("/{id}", response_model=schemas.RecruitmentOut)
# def update_recruitment(
#     id: int,
#     updated_data: schemas.RecruitmentUpdate,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     try:
#         recruitment_instance = db.query(models.Recruitment).filter(models.Recruitment.id == id).first()

#         if not recruitment_instance:
#             raise HTTPException(status_code=404, detail=f"Recruitment with id {id} not found")

#         update_dict = updated_data.dict(exclude_unset=True)
#         update_dict["updated_by_user_id"] = current_user.id

#         for key, value in update_dict.items():
#             setattr(recruitment_instance, key, value)

#         db.commit()
#         db.refresh(recruitment_instance)

#         return recruitment_instance

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.delete("/{id}", status_code=status.HTTP_200_OK)
# def delete_recruitment(
#     id: int,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     recruitment_query = db.query(models.Recruitment).filter(models.Recruitment.id == id)
#     recruitment = recruitment_query.first()

#     if not recruitment:
#         raise HTTPException(status_code=404, detail=f"Recruitment with id {id} not found")

#     recruitment_query.delete(synchronize_session=False)
#     db.commit()

#     return {"message": "Recruitment deleted successfully"}





import logging
import traceback
from datetime import datetime, date
from typing import Any, List

from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError

from .. import database, schemas, models, oauth2
from app.utils import paginate_data, filter_recruitments

router = APIRouter(
    prefix="/recruitments",
    tags=["Recruitments"]
)

logger = logging.getLogger(__name__)

@router.get("/", response_model=schemas.RecruitmentListResponse)
def get_recruitments(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """
    Get all recruitments with pagination and filtering
    """
    try:
        # Base query
        query = db.query(models.Recruitment)
        
        # Apply filters from query parameters
        query = filter_recruitments(request.query_params, query)
        
        # Eager load relationships to prevent N+1 queries
        query = query.options(
            joinedload(models.Recruitment.department),
            joinedload(models.Recruitment.creator),
            joinedload(models.Recruitment.updater),
            joinedload(models.Recruitment.created_by_employee),
            joinedload(models.Recruitment.hiring_manager)
        )
        
        # Get total count before pagination
        total_count = query.count()
        
        # Apply pagination
        paginated_query = paginate_data(query, request)
        recruitments = paginated_query.all()
        
        # Serialize data
        serialized_data = [
            schemas.RecruitmentOut.model_validate(recruitment) 
            for recruitment in recruitments
        ]

        return {
            "status": "SUCCESS",
            "result": {
                "count": total_count,
                "data": serialized_data
            }
        }

    except SQLAlchemyError as e:
        logger.error(f"Database error fetching recruitments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        logger.error(f"Unexpected error fetching recruitments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch recruitments"
        )


@router.post("/", 
             status_code=status.HTTP_201_CREATED, 
             response_model=schemas.RecruitmentOut)
def create_recruitment(
    payload: schemas.RecruitmentCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    """
    Create a new recruitment
    """
    try:
        # Validate payload
        if payload.deadline and payload.deadline < date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Deadline cannot be in the past"
            )
        
        if payload.salary_min and payload.salary_max and payload.salary_min > payload.salary_max:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum salary cannot be greater than maximum salary"
            )

        # Prepare data
        recruitment_data = payload.model_dump()
        recruitment_data.update({
            "created_by_user_id": current_user.id,
            "created_by_employee_id": getattr(current_user, "employee_id", None),
            "created_at": datetime.utcnow()
        })

        # Create new recruitment
        new_recruitment = models.Recruitment(**recruitment_data)
        db.add(new_recruitment)
        db.commit()
        db.refresh(new_recruitment)

        return new_recruitment

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating recruitment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create recruitment"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error creating recruitment: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.get("/{id}", response_model=schemas.RecruitmentOut)
def get_recruitment(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """
    Get a single recruitment by ID
    """
    try:
        recruitment = db.query(models.Recruitment)\
            .options(
                joinedload(models.Recruitment.department),
                joinedload(models.Recruitment.creator),
                joinedload(models.Recruitment.updater),
                joinedload(models.Recruitment.created_by_employee),
                joinedload(models.Recruitment.hiring_manager)
            )\
            .filter(models.Recruitment.id == id)\
            .first()

        if not recruitment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Recruitment with id {id} not found"
            )

        return recruitment

    except SQLAlchemyError as e:
        logger.error(f"Database error fetching recruitment {id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        logger.error(f"Unexpected error fetching recruitment {id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch recruitment"
        )


@router.patch("/{id}", response_model=schemas.RecruitmentOut)
def update_recruitment(
    id: int,
    updated_data: schemas.RecruitmentUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """
    Update a recruitment
    """
    try:
        # Get existing recruitment
        recruitment = db.query(models.Recruitment)\
            .filter(models.Recruitment.id == id)\
            .first()

        if not recruitment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Recruitment with id {id} not found"
            )

        # Validate update data
        update_dict = updated_data.model_dump(exclude_unset=True)
        
        if 'deadline' in update_dict and update_dict['deadline'] < date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Deadline cannot be in the past"
            )
            
        if ('salary_min' in update_dict or 'salary_max' in update_dict):
            new_min = update_dict.get('salary_min', recruitment.salary_min)
            new_max = update_dict.get('salary_max', recruitment.salary_max)
            if new_min and new_max and new_min > new_max:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Minimum salary cannot be greater than maximum salary"
                )

        # Handle status changes
        if 'status' in update_dict:
            if update_dict['status'] == 'active' and not recruitment.posted_date:
                update_dict['posted_date'] = date.today()
                update_dict['published_at'] = datetime.utcnow()
            elif update_dict['status'] == 'closed':
                update_dict['closed_at'] = datetime.utcnow()

        # Apply updates
        for field, value in update_dict.items():
            setattr(recruitment, field, value)
            
        recruitment.updated_by_user_id = current_user.id
        recruitment.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(recruitment)

        return recruitment

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error updating recruitment {id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update recruitment"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error updating recruitment {id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_recruitment(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """
    Delete a recruitment
    
    Returns:
        Successful deletion: {"message": "Recruitment deleted successfully"}
        Not found: {"detail": "Recruitment with id {id} not found"}
        Database error: {"detail": "Database error: [specific error]"}
        Other errors: {"detail": "Error deleting recruitment: [specific error]"}
    """
    try:
        # First check if recruitment exists
        recruitment = db.query(models.Recruitment).get(id)
        if not recruitment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Recruitment with id {id} not found"
            )

        try:
            # Perform the deletion
            db.delete(recruitment)
            db.commit()
            
            return {"message": "Recruitment deleted successfully"}
            
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error deleting recruitment {id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
            
    except HTTPException:
        # Re-raise HTTPExceptions (like our 404) unchanged
        raise
    except Exception as e:
        logger.error(f"Unexpected error deleting recruitment {id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting recruitment: {str(e)}"
        )