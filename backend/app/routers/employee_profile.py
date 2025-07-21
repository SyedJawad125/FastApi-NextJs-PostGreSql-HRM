# from fastapi import APIRouter, Depends, status, Request, HTTPException
# from sqlalchemy.orm import Session
# from typing import Any
# from app import database, schemas, models, oauth2
# from app.utils import paginate_data
# from fastapi.responses import JSONResponse
# from datetime import datetime

# router = APIRouter(
#     prefix="/employee_profiles",
#     tags=["Employee Profiles"]
# )

# # -------------------- GET ALL with Pagination --------------------

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

#         serialized = [schemas.EmployeeProfileOut.from_orm(profile) for profile in paginated_data]

#         return {
#             "status": "SUCCESSFUL",
#             "result": {
#                 "count": count,
#                 "data": serialized
#             }
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # -------------------- GET ONE by ID --------------------

# @router.get("/{id}", response_model=schemas.EmployeeProfileOut)
# def get_profile_by_id(
#     id: int,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     profile = db.query(models.EmployeeProfile).filter(models.EmployeeProfile.id == id).first()

#     if not profile:
#         raise HTTPException(status_code=404, detail=f"EmployeeProfile with id {id} not found")

#     return profile


# # -------------------- POST: Create --------------------

# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.EmployeeProfileOut)
# def create_profile(
#     profile: schemas.EmployeeProfileCreate,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     try:
#         profile_data = profile.dict()
#         profile_data["created_by_user_id"] = current_user.id

#         # Convert list fields to comma-separated strings
#         profile_data["professional_certifications"] = ",".join(profile.professional_certifications or [])
#         profile_data["skills"] = ",".join(profile.skills or [])
#         profile_data["languages"] = ",".join(profile.languages or [])
#         profile_data["hobbies"] = ",".join(profile.hobbies or [])

#         # Optional: check if employee exists
#         employee = db.query(models.Employee).filter(models.Employee.id == profile.employee_id).first()
#         if not employee:
#             raise HTTPException(status_code=404, detail="Employee not found")

#         new_profile = models.EmployeeProfile(**profile_data)
#         db.add(new_profile)
#         db.commit()
#         db.refresh(new_profile)

#         return new_profile

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # -------------------- PATCH: Update --------------------

# @router.patch("/{id}", response_model=schemas.EmployeeProfileOut)
# def update_profile(
#     id: int,
#     updated_data: schemas.EmployeeProfileUpdate,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     try:
#         profile_instance = db.query(models.EmployeeProfile).filter(models.EmployeeProfile.id == id).first()

#         if not profile_instance:
#             raise HTTPException(status_code=404, detail=f"EmployeeProfile with id {id} not found")

#         update_dict = updated_data.dict(exclude_unset=True)

#         # Convert list fields to strings if they are present
#         for key in ["professional_certifications", "skills", "languages", "hobbies"]:
#             if key in update_dict:
#                 update_dict[key] = ",".join(update_dict[key]) if update_dict[key] else ""

#         # Update the fields
#         for key, value in update_dict.items():
#             setattr(profile_instance, key, value)

#         # ✅ Inject system fields (NOT from request)
#         profile_instance.updated_by_user_id = current_user.id
#         profile_instance.updated_at = datetime.utcnow()  # Set current UTC time

#         db.commit()
#         db.refresh(profile_instance)

#         return profile_instance

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # -------------------- DELETE --------------------

# @router.delete("/{id}", status_code=status.HTTP_200_OK)
# def delete_profile(
#     id: int,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     profile_query = db.query(models.EmployeeProfile).filter(models.EmployeeProfile.id == id)
#     profile = profile_query.first()

#     if not profile:
#         raise HTTPException(status_code=404, detail=f"EmployeeProfile with id {id} not found")

#     profile_query.delete(synchronize_session=False)
#     db.commit()

#     return {"message": "Employee profile deleted successfully"}


# def split_string_fields(profile: models.EmployeeProfile) -> dict:
#     data = profile.__dict__.copy()
#     for field in ["professional_certifications", "skills", "languages", "hobbies"]:
#         if data.get(field):
#             data[field] = data[field].split(",")
#         else:
#             data[field] = []
#     return data




from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from app import database, schemas, models, oauth2
from app.utils import paginate_data
from fastapi.responses import JSONResponse
from datetime import datetime

router = APIRouter(
    prefix="/employee_profiles",
    tags=["Employee Profiles"]
)

# -------------------- Helper Function to Convert String to List --------------------

def split_string_fields(profile: models.EmployeeProfile) -> dict:
    data = profile.__dict__.copy()
    for field in ["professional_certifications", "skills", "languages", "hobbies"]:
        if data.get(field):
            data[field] = data[field].split(",")
        else:
            data[field] = []
    return data

# -------------------- GET ALL with Pagination --------------------

@router.get("/", response_model=schemas.EmployeeProfileListResponse)
def get_all_profiles(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.EmployeeProfile)
        data = query.all()
        paginated_data, count = paginate_data(data, request)

        serialized = [
            schemas.EmployeeProfileOut(**split_string_fields(profile))
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

# -------------------- GET ONE by ID --------------------

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

# -------------------- POST: Create --------------------

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
        profile_data["professional_certifications"] = ",".join(profile.professional_certifications or [])
        profile_data["skills"] = ",".join(profile.skills or [])
        profile_data["languages"] = ",".join(profile.languages or [])
        profile_data["hobbies"] = ",".join(profile.hobbies or [])

        # Optional: check if employee exists
        employee = db.query(models.Employee).filter(models.Employee.id == profile.employee_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        new_profile = models.EmployeeProfile(**profile_data)
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)

        return schemas.EmployeeProfileOut(**split_string_fields(new_profile))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------- PATCH: Update --------------------

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

        # Convert list fields to strings if they are present
        for key in ["professional_certifications", "skills", "languages", "hobbies"]:
            if key in update_dict:
                update_dict[key] = ",".join(update_dict[key]) if update_dict[key] else ""

        # Update the fields
        for key, value in update_dict.items():
            setattr(profile_instance, key, value)

        # ✅ Inject system fields (NOT from request)
        profile_instance.updated_by_user_id = current_user.id
        profile_instance.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(profile_instance)

        return schemas.EmployeeProfileOut(**split_string_fields(profile_instance))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------- DELETE --------------------

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
