from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from app import database, schemas, models, oauth2
from app.utils import paginate_data
from fastapi.responses import JSONResponse
from datetime import datetime
from sqlalchemy.orm import joinedload  # ✅ Already imported

router = APIRouter(
    prefix="/employee_profiles",
    tags=["Employee Profiles"]
)

# -------------------- Helper: Convert comma-separated string to list --------------------
def split_string_fields(profile: models.EmployeeProfile) -> dict:
    data = profile.__dict__.copy()
    for field in ["professional_certifications", "skills", "languages", "hobbies"]:
        if data.get(field):
            data[field] = data[field].split(",")
        else:
            data[field] = []
    data["employee"] = profile.employee  # include nested employee relation
    return data
# -------------------- GET All Profiles (with Pagination) --------------------
# @router.get("/", response_model=schemas.EmployeeProfileListResponse)
# def get_all_profiles(
#     request: Request,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     try:
#         query = db.query(models.EmployeeProfile)
#         data = query.all()
#         paginated_data, count = paginate_data(data, request)

#         serialized = [
#             schemas.EmployeeProfileOut(**split_string_fields(profile))
#             for profile in paginated_data
#         ]

#         return {
#             "status": "SUCCESSFUL",
#             "result": {
#                 "count": count,
#                 "data": serialized
#             }
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=schemas.EmployeeProfileListResponse)
def get_all_profiles(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.EmployeeProfile).options(joinedload(models.EmployeeProfile.employee))
        data = query.all()

        paginated_data, count = paginate_data(data, request)

        # ✅ Convert comma-separated fields before model validation
        serialized = [
            schemas.EmployeeProfileOut.model_validate(split_string_fields(profile))
            for profile in paginated_data
        ]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------- GET One Profile by ID --------------------
@router.get("/{id}", response_model=schemas.EmployeeProfileOut)
def get_profile_by_id(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    profile = db.query(models.EmployeeProfile).filter(models.EmployeeProfile.id == id).first()

    if not profile:
        raise HTTPException(status_code=404, detail=f"EmployeeProfile with id {id} not found")

    return schemas.EmployeeProfileOut(**split_string_fields(profile))

# -------------------- CREATE New Profile --------------------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.EmployeeProfileOut)
def create_profile(
    profile: schemas.EmployeeProfileCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        profile_data = profile.dict()
        profile_data["created_by_user_id"] = current_user.id

        # Convert list fields to comma-separated strings
        for field in ["professional_certifications", "skills", "languages", "hobbies"]:
            profile_data[field] = ",".join(profile_data.get(field, []))

        # Ensure employee exists
        employee = db.query(models.Employee).filter(models.Employee.id == profile.employee_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        new_profile = models.EmployeeProfile(**profile_data)
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)

        # If you have a helper to split string fields back to lists
        return schemas.EmployeeProfileOut(**split_string_fields(new_profile))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------- UPDATE Existing Profile --------------------
@router.patch("/{id}", response_model=schemas.EmployeeProfileOut)
def update_profile(
    id: int,
    updated_data: schemas.EmployeeProfileUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        profile_instance = db.query(models.EmployeeProfile).filter(models.EmployeeProfile.id == id).first()

        if not profile_instance:
            raise HTTPException(status_code=404, detail=f"EmployeeProfile with id {id} not found")

        update_dict = updated_data.dict(exclude_unset=True)

        # Convert list fields to comma-separated strings
        for field in ["professional_certifications", "skills", "languages", "hobbies"]:
            if field in update_dict:
                update_dict[field] = ",".join(update_dict[field]) if update_dict[field] else ""

        # Update fields
        for key, value in update_dict.items():
            setattr(profile_instance, key, value)

        # Update system fields
        profile_instance.updated_by_user_id = current_user.id
        profile_instance.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(profile_instance)

        return schemas.EmployeeProfileOut(**split_string_fields(profile_instance))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------- DELETE Profile --------------------
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_profile(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    profile_query = db.query(models.EmployeeProfile).filter(models.EmployeeProfile.id == id)
    profile = profile_query.first()

    if not profile:
        raise HTTPException(status_code=404, detail=f"EmployeeProfile with id {id} not found")

    profile_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Employee profile deleted successfully"}
